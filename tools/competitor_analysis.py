"""
SERP & Competitor Content Analysis
====================================
Fetches and analyzes multiple competitor pages using NLP to find
content gaps, common terms, entity coverage, and semantic similarity.

Usage:
    python competitor_analysis.py --urls https://comp1.com https://comp2.com --target-keyword "cloud hosting"
    python competitor_analysis.py --files comp1.html comp2.html comp3.html --target-keyword "crm software" --my-content my_page.html
    python competitor_analysis.py --urls https://a.com https://b.com --target-keyword "seo tools" --output report.xlsx
"""

import argparse
import re
import sys
import time
import pandas as pd
import numpy as np
from collections import Counter


def fetch_url(url):
    """Fetch page HTML with polite delay."""
    import requests
    from bs4 import BeautifulSoup

    headers = {"User-Agent": "Mozilla/5.0 (compatible; SEO-Analyzer/1.0)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  Warning: Failed to fetch {url}: {e}")
        return None


def extract_text(html):
    """Extract clean text and metadata from HTML."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""
    headings = {}
    for lvl in range(1, 7):
        tags = soup.find_all(f"h{lvl}")
        if tags:
            headings[f"h{lvl}"] = [t.get_text(strip=True) for t in tags]

    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    word_count = len(re.findall(r"\b\w+\b", text))

    return {
        "text": text,
        "title": title,
        "headings": headings,
        "word_count": word_count,
    }


def tfidf_across_pages(pages, top_n=50):
    """Run TF-IDF across all pages and return top terms per page + common terms."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    texts = [p["text"] for p in pages]
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words="english", max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    per_page_terms = []
    for i in range(len(texts)):
        row = tfidf_matrix[i].toarray().flatten()
        top_idx = row.argsort()[-top_n:][::-1]
        terms = [(feature_names[j], round(row[j], 4)) for j in top_idx if row[j] > 0]
        per_page_terms.append(terms)

    # Common high-value terms (appear in 50%+ of pages with decent score)
    avg_scores = tfidf_matrix.mean(axis=0).A1
    doc_freq = (tfidf_matrix > 0).sum(axis=0).A1
    threshold = len(texts) * 0.5
    common_terms = [
        (feature_names[i], round(avg_scores[i], 4), int(doc_freq[i]))
        for i in avg_scores.argsort()[::-1]
        if doc_freq[i] >= threshold and avg_scores[i] > 0.01
    ][:top_n]

    return per_page_terms, common_terms, vectorizer, tfidf_matrix


def entity_analysis(pages):
    """Extract entities across all pages and build frequency matrix."""
    import spacy

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import subprocess
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        nlp = spacy.load("en_core_web_sm")

    all_entities = []
    per_page_entities = []

    for page in pages:
        doc = nlp(page["text"][:100000])
        ents = Counter(ent.text.strip() for ent in doc.ents if len(ent.text.strip()) > 1)
        per_page_entities.append(ents)
        all_entities.extend(ents.keys())

    # Entity frequency across pages
    entity_freq = Counter(all_entities)
    top_entities = entity_freq.most_common(40)

    # Build matrix
    entity_matrix = []
    for ent, _ in top_entities:
        row = {"entity": ent}
        for i, page_ents in enumerate(per_page_entities):
            row[f"page_{i+1}"] = page_ents.get(ent, 0)
        row["total"] = sum(row[f"page_{j+1}"] for j in range(len(pages)))
        entity_matrix.append(row)

    return entity_matrix, per_page_entities


def semantic_similarity(pages, model_name="all-MiniLM-L6-v2"):
    """Compute pairwise semantic similarity between pages."""
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    model = SentenceTransformer(model_name)

    # Use first 512 words per page for embedding
    summaries = [" ".join(p["text"].split()[:512]) for p in pages]
    embeddings = model.encode(summaries)
    sim_matrix = cosine_similarity(embeddings)
    return sim_matrix


def gap_analysis(my_page, competitor_pages, common_terms, entity_matrix):
    """Find terms and entities competitors have but my content lacks."""
    my_text_lower = my_page["text"].lower()
    my_words = set(re.findall(r"\b\w+\b", my_text_lower))

    # Term gaps
    term_gaps = []
    for term, score, doc_count in common_terms:
        if term.lower() not in my_text_lower:
            term_gaps.append({"term": term, "avg_tfidf": score, "competitor_pages": doc_count})

    # Entity gaps
    entity_gaps = []
    for row in entity_matrix:
        ent = row["entity"]
        if ent.lower() not in my_text_lower and row["total"] >= 2:
            entity_gaps.append({"entity": ent, "competitor_mentions": row["total"]})

    # Structural gaps
    comp_word_counts = [p["word_count"] for p in competitor_pages]
    avg_comp_wc = int(np.mean(comp_word_counts)) if comp_word_counts else 0
    comp_h2_counts = [len(p["headings"].get("h2", [])) for p in competitor_pages]
    avg_comp_h2 = round(np.mean(comp_h2_counts), 1) if comp_h2_counts else 0

    structural = {
        "your_word_count": my_page["word_count"],
        "avg_competitor_word_count": avg_comp_wc,
        "your_h2_count": len(my_page["headings"].get("h2", [])),
        "avg_competitor_h2_count": avg_comp_h2,
    }

    return term_gaps, entity_gaps, structural


def print_report(labels, pages, common_terms, entity_matrix, sim_matrix, gap_data=None):
    """Print analysis report."""
    print("\n" + "=" * 70)
    print("  COMPETITOR CONTENT ANALYSIS")
    print("=" * 70)

    # Page overview
    print("\n--- Page Overview ---")
    for i, (label, page) in enumerate(zip(labels, pages)):
        h2_count = len(page["headings"].get("h2", []))
        print(f"  [{i+1}] {label[:50]:<50} {page['word_count']:>6} words  {h2_count} H2s")

    # Common terms
    print(f"\n--- Common High-Value Terms (top 20) ---")
    print(f"  {'Term':<30} {'Avg TF-IDF':>10} {'In # Pages':>10}")
    for term, score, count in common_terms[:20]:
        print(f"  {term:<30} {score:>10.4f} {count:>10}")

    # Entity matrix
    print(f"\n--- Entity Coverage (top 15) ---")
    df_ent = pd.DataFrame(entity_matrix[:15])
    print(df_ent.to_string(index=False))

    # Similarity matrix
    if sim_matrix is not None:
        print(f"\n--- Semantic Similarity Matrix ---")
        sim_df = pd.DataFrame(sim_matrix, index=labels, columns=labels)
        print(sim_df.round(3).to_string())

    # Gap analysis
    if gap_data:
        term_gaps, entity_gaps, structural = gap_data
        print(f"\n--- Gap Analysis (Your Content vs Competitors) ---")
        print(f"  Word count: You={structural['your_word_count']} vs Avg={structural['avg_competitor_word_count']}")
        print(f"  H2 count:   You={structural['your_h2_count']} vs Avg={structural['avg_competitor_h2_count']}")

        if term_gaps:
            print(f"\n  Missing terms (top 15):")
            for g in term_gaps[:15]:
                print(f"    {g['term']:<30} (TF-IDF: {g['avg_tfidf']}, in {g['competitor_pages']} pages)")

        if entity_gaps:
            print(f"\n  Missing entities (top 10):")
            for g in entity_gaps[:10]:
                print(f"    {g['entity']:<30} ({g['competitor_mentions']} competitor mentions)")

    print("=" * 70)


def save_xlsx(output_path, labels, pages, common_terms, entity_matrix, gap_data=None):
    """Save full report to XLSX."""
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Overview
        overview = [{"page": labels[i], "word_count": pages[i]["word_count"],
                      "h2_count": len(pages[i]["headings"].get("h2", []))} for i in range(len(pages))]
        pd.DataFrame(overview).to_excel(writer, sheet_name="Overview", index=False)

        # Common terms
        ct_df = pd.DataFrame(common_terms, columns=["term", "avg_tfidf", "doc_count"])
        ct_df.to_excel(writer, sheet_name="Common Terms", index=False)

        # Entities
        pd.DataFrame(entity_matrix).to_excel(writer, sheet_name="Entities", index=False)

        # Gaps
        if gap_data:
            term_gaps, entity_gaps, structural = gap_data
            if term_gaps:
                pd.DataFrame(term_gaps).to_excel(writer, sheet_name="Term Gaps", index=False)
            if entity_gaps:
                pd.DataFrame(entity_gaps).to_excel(writer, sheet_name="Entity Gaps", index=False)

    print(f"\nReport saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="SERP & Competitor Content Analysis")
    parser.add_argument("--urls", nargs="+", help="Competitor URLs to fetch")
    parser.add_argument("--files", nargs="+", help="Local HTML files for competitor pages")
    parser.add_argument("--my-content", help="Your page (URL or file) for gap analysis")
    parser.add_argument("--target-keyword", required=True, help="Primary keyword")
    parser.add_argument("--output", help="Save report as XLSX")
    parser.add_argument("--skip-similarity", action="store_true", help="Skip semantic similarity (faster)")
    args = parser.parse_args()

    # Load competitor pages
    pages = []
    labels = []

    if args.urls:
        for url in args.urls:
            print(f"Fetching {url}...")
            html = fetch_url(url)
            if html:
                pages.append(extract_text(html))
                labels.append(url.split("//")[-1][:40])
                time.sleep(1)

    if args.files:
        for fpath in args.files:
            with open(fpath, "r", encoding="utf-8") as f:
                html = f.read()
            pages.append(extract_text(html))
            labels.append(fpath)

    if len(pages) < 2:
        print("Need at least 2 competitor pages to analyze.")
        sys.exit(1)

    print(f"\nAnalyzing {len(pages)} pages...")

    # TF-IDF
    per_page_terms, common_terms, vectorizer, tfidf_matrix = tfidf_across_pages(pages)

    # Entities
    entity_matrix, per_page_entities = entity_analysis(pages)

    # Similarity
    sim_matrix = None
    if not args.skip_similarity:
        print("Computing semantic similarity...")
        sim_matrix = semantic_similarity(pages)

    # Gap analysis if user provided their content
    gap_data = None
    if args.my_content:
        if args.my_content.startswith("http"):
            my_html = fetch_url(args.my_content)
        else:
            with open(args.my_content, "r", encoding="utf-8") as f:
                my_html = f.read()
        if my_html:
            my_page = extract_text(my_html)
            gap_data = gap_analysis(my_page, pages, common_terms, entity_matrix)

    print_report(labels, pages, common_terms, entity_matrix, sim_matrix, gap_data)

    if args.output:
        save_xlsx(args.output, labels, pages, common_terms, entity_matrix, gap_data)


if __name__ == "__main__":
    main()
