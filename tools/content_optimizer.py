"""
Content Optimization & SEO Scoring
====================================
Analyzes content for SEO quality: TF-IDF keyword coverage, entity extraction,
readability scoring, and structural analysis.

Usage:
    python content_optimizer.py --url https://example.com/page --target-keyword "project management tools"
    python content_optimizer.py --file article.html --target-keyword "cloud hosting" --competitors comp1.html comp2.html
    python content_optimizer.py --text "Your content here..." --target-keyword "best crm software"
"""

import argparse
import re
import math
import sys
from collections import Counter


def fetch_url(url):
    """Fetch and parse HTML from a URL."""
    import requests
    from bs4 import BeautifulSoup

    headers = {"User-Agent": "Mozilla/5.0 (compatible; SEO-Analyzer/1.0)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.text


def extract_text_and_structure(html):
    """Extract text, headings, links, and structure from HTML."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # Headings
    headings = {}
    for level in range(1, 7):
        tags = soup.find_all(f"h{level}")
        if tags:
            headings[f"h{level}"] = [t.get_text(strip=True) for t in tags]

    # Links
    links = {"internal": [], "external": []}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            links["external"].append(href)
        elif href.startswith("/") or href.startswith("#"):
            links["internal"].append(href)

    # Title & meta description
    title = soup.title.get_text(strip=True) if soup.title else ""
    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"]

    # Body text
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)

    return {
        "text": text,
        "title": title,
        "meta_description": meta_desc,
        "headings": headings,
        "links": links,
        "html": str(soup),
    }


def count_syllables(word):
    """Rough syllable count for English words."""
    word = word.lower().strip()
    if len(word) <= 2:
        return 1
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e"):
        count -= 1
    return max(count, 1)


def readability_scores(text):
    """Compute Flesch-Kincaid and Gunning Fog readability scores."""
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
    words = re.findall(r"\b[a-zA-Z]+\b", text)

    if not sentences or not words:
        return {"flesch_kincaid_grade": 0, "gunning_fog": 0, "avg_sentence_length": 0}

    num_sentences = len(sentences)
    num_words = len(words)
    num_syllables = sum(count_syllables(w) for w in words)
    complex_words = sum(1 for w in words if count_syllables(w) >= 3)

    asl = num_words / num_sentences
    asw = num_syllables / num_words

    fk_grade = 0.39 * asl + 11.8 * asw - 15.59
    gunning_fog = 0.4 * (asl + 100 * (complex_words / num_words))

    return {
        "flesch_kincaid_grade": round(fk_grade, 1),
        "gunning_fog": round(gunning_fog, 1),
        "avg_sentence_length": round(asl, 1),
        "total_words": num_words,
        "total_sentences": num_sentences,
    }


def tfidf_keyword_analysis(text, target_keyword, top_n=30):
    """Analyze keyword coverage using TF-IDF."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Treat paragraphs as documents
    paragraphs = re.split(r"\n{2,}|\. {2,}", text)
    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 20]
    if not paragraphs:
        paragraphs = [text]

    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words="english", max_features=500)
    tfidf_matrix = vectorizer.fit_transform(paragraphs)
    feature_names = vectorizer.get_feature_names_out()
    avg_scores = tfidf_matrix.mean(axis=0).A1

    # Top terms by TF-IDF
    term_scores = sorted(zip(feature_names, avg_scores), key=lambda x: -x[1])[:top_n]

    # Check target keyword presence
    target_lower = target_keyword.lower()
    target_words = target_lower.split()
    text_lower = text.lower()

    keyword_freq = text_lower.count(target_lower)
    word_count = len(re.findall(r"\b\w+\b", text))
    keyword_density = (keyword_freq * len(target_words)) / word_count * 100 if word_count else 0

    return {
        "top_tfidf_terms": term_scores,
        "target_keyword_frequency": keyword_freq,
        "keyword_density_pct": round(keyword_density, 2),
    }


def extract_entities(text):
    """Extract named entities using spaCy."""
    import spacy

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import subprocess
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        nlp = spacy.load("en_core_web_sm")

    # Process in chunks if text is long
    max_len = 100000
    doc = nlp(text[:max_len])

    entities = []
    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})

    entity_counts = Counter((e["text"], e["label"]) for e in entities)
    entity_summary = [
        {"entity": text, "type": label, "count": count}
        for (text, label), count in entity_counts.most_common(50)
    ]
    return entity_summary


def compute_seo_score(structure, readability, tfidf_data, entities, target_keyword):
    """Compute a weighted SEO score (0-100)."""
    score = 0
    details = []

    # Title contains keyword (15 pts)
    if target_keyword.lower() in structure["title"].lower():
        score += 15
        details.append(("Title contains keyword", 15, 15))
    else:
        details.append(("Title contains keyword", 0, 15))

    # Meta description contains keyword (10 pts)
    if target_keyword.lower() in structure["meta_description"].lower():
        score += 10
        details.append(("Meta description contains keyword", 10, 10))
    else:
        details.append(("Meta description contains keyword", 0, 10))

    # H1 contains keyword (10 pts)
    h1s = structure["headings"].get("h1", [])
    if any(target_keyword.lower() in h.lower() for h in h1s):
        score += 10
        details.append(("H1 contains keyword", 10, 10))
    else:
        details.append(("H1 contains keyword", 0, 10))

    # Keyword density 0.5-2.5% (10 pts)
    density = tfidf_data["keyword_density_pct"]
    if 0.5 <= density <= 2.5:
        score += 10
        details.append((f"Keyword density {density}% (ideal 0.5-2.5%)", 10, 10))
    elif density > 0:
        score += 5
        details.append((f"Keyword density {density}% (ideal 0.5-2.5%)", 5, 10))
    else:
        details.append((f"Keyword density {density}% (ideal 0.5-2.5%)", 0, 10))

    # Word count (15 pts) — 1000+ ideal
    wc = readability["total_words"]
    if wc >= 1500:
        score += 15
        details.append((f"Word count: {wc} (1500+ ideal)", 15, 15))
    elif wc >= 800:
        score += 10
        details.append((f"Word count: {wc} (1500+ ideal)", 10, 15))
    elif wc >= 300:
        score += 5
        details.append((f"Word count: {wc} (1500+ ideal)", 5, 15))
    else:
        details.append((f"Word count: {wc} (1500+ ideal)", 0, 15))

    # Readability (10 pts) — FK grade 6-12 ideal
    fk = readability["flesch_kincaid_grade"]
    if 6 <= fk <= 12:
        score += 10
        details.append((f"Readability FK grade: {fk} (6-12 ideal)", 10, 10))
    elif 4 <= fk <= 14:
        score += 5
        details.append((f"Readability FK grade: {fk} (6-12 ideal)", 5, 10))
    else:
        details.append((f"Readability FK grade: {fk} (6-12 ideal)", 0, 10))

    # Heading structure (10 pts)
    has_h2 = len(structure["headings"].get("h2", [])) >= 2
    has_h3 = len(structure["headings"].get("h3", [])) >= 1
    heading_pts = (5 if has_h2 else 0) + (5 if has_h3 else 0)
    score += heading_pts
    details.append((f"Heading structure (H2s: {len(structure['headings'].get('h2', []))}, H3s: {len(structure['headings'].get('h3', []))})", heading_pts, 10))

    # Internal links (10 pts)
    int_links = len(structure["links"]["internal"])
    if int_links >= 3:
        score += 10
        details.append((f"Internal links: {int_links}", 10, 10))
    elif int_links >= 1:
        score += 5
        details.append((f"Internal links: {int_links}", 5, 10))
    else:
        details.append((f"Internal links: {int_links}", 0, 10))

    # Entity richness (10 pts)
    unique_entities = len(set(e["entity"] for e in entities))
    if unique_entities >= 10:
        score += 10
        details.append((f"Unique entities: {unique_entities}", 10, 10))
    elif unique_entities >= 5:
        score += 5
        details.append((f"Unique entities: {unique_entities}", 5, 10))
    else:
        details.append((f"Unique entities: {unique_entities}", 0, 10))

    return score, details


def print_report(structure, readability, tfidf_data, entities, score, score_details, target_keyword):
    """Print the SEO analysis report."""
    print("\n" + "=" * 60)
    print(f"  SEO CONTENT ANALYSIS: '{target_keyword}'")
    print("=" * 60)

    print(f"\n{'OVERALL SCORE':>20}: {score}/100")
    print("-" * 60)
    for desc, pts, max_pts in score_details:
        bar = "█" * pts + "░" * (max_pts - pts)
        print(f"  {desc:<45} {bar} {pts}/{max_pts}")

    print(f"\n--- Structure ---")
    print(f"  Title: {structure['title'][:80]}")
    print(f"  Meta desc: {structure['meta_description'][:100]}")
    for level, texts in structure["headings"].items():
        print(f"  {level.upper()}: {len(texts)} found")
    print(f"  Internal links: {len(structure['links']['internal'])}")
    print(f"  External links: {len(structure['links']['external'])}")

    print(f"\n--- Readability ---")
    for k, v in readability.items():
        print(f"  {k}: {v}")

    print(f"\n--- Keyword Analysis ---")
    print(f"  Target: '{target_keyword}'")
    print(f"  Frequency: {tfidf_data['target_keyword_frequency']}")
    print(f"  Density: {tfidf_data['keyword_density_pct']}%")
    print(f"\n  Top TF-IDF terms:")
    for term, score_val in tfidf_data["top_tfidf_terms"][:15]:
        print(f"    {term:<30} {score_val:.4f}")

    print(f"\n--- Entities (top 15) ---")
    for e in entities[:15]:
        print(f"  {e['entity']:<30} {e['type']:<12} (x{e['count']})")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="SEO Content Optimizer & Scorer")
    parser.add_argument("--url", help="URL to analyze")
    parser.add_argument("--file", help="Local HTML/text file to analyze")
    parser.add_argument("--text", help="Raw text to analyze")
    parser.add_argument("--target-keyword", required=True, help="Primary target keyword")
    parser.add_argument("--output", help="Save report as HTML (optional)")
    args = parser.parse_args()

    # Load content
    if args.url:
        html = fetch_url(args.url)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            html = f.read()
    elif args.text:
        html = f"<html><body><p>{args.text}</p></body></html>"
    else:
        print("Provide --url, --file, or --text")
        sys.exit(1)

    structure = extract_text_and_structure(html)
    readability = readability_scores(structure["text"])
    tfidf_data = tfidf_keyword_analysis(structure["text"], args.target_keyword)
    entities = extract_entities(structure["text"])
    score, score_details = compute_seo_score(structure, readability, tfidf_data, entities, args.target_keyword)

    print_report(structure, readability, tfidf_data, entities, score, score_details, args.target_keyword)


if __name__ == "__main__":
    main()
