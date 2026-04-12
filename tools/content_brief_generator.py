"""
Content Brief Generator
=========================
Generates data-driven content briefs by analyzing top-ranking competitor pages.
Produces recommended word count, headings, entities, terms, and structure.

Usage:
    python content_brief_generator.py --urls https://comp1.com https://comp2.com https://comp3.com --keyword "best crm software" --output brief.xlsx
"""

import argparse
import re
import sys
import time
import numpy as np
import pandas as pd
from collections import Counter


def fetch_text(url):
    import requests
    from bs4 import BeautifulSoup
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        for t in soup(["script", "style", "nav", "footer"]):
            t.decompose()
        headings = {}
        for lvl in range(1, 7):
            tags = soup.find_all(f"h{lvl}")
            if tags:
                headings[f"h{lvl}"] = [t.get_text(strip=True) for t in tags]
        text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
        return {"text": text, "headings": headings, "word_count": len(re.findall(r"\b\w+\b", text))}
    except Exception as e:
        print(f"  Failed: {url} — {e}")
        return None


def generate_brief(pages, keyword):
    from sklearn.feature_extraction.text import TfidfVectorizer

    texts = [p["text"] for p in pages]
    word_counts = [p["word_count"] for p in pages]

    # TF-IDF terms
    vec = TfidfVectorizer(ngram_range=(1, 3), stop_words="english", max_features=500)
    matrix = vec.fit_transform(texts)
    features = vec.get_feature_names_out()
    avg_scores = matrix.mean(axis=0).A1
    doc_freq = (matrix > 0).sum(axis=0).A1
    threshold = len(texts) * 0.4

    must_include = [(features[i], round(avg_scores[i], 4), int(doc_freq[i]))
                    for i in avg_scores.argsort()[::-1]
                    if doc_freq[i] >= threshold and avg_scores[i] > 0.01][:40]

    # Heading patterns
    all_h2s = []
    for p in pages:
        all_h2s.extend(p["headings"].get("h2", []))
    h2_freq = Counter(h.lower().strip() for h in all_h2s).most_common(20)

    # Entity extraction
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
            nlp = spacy.load("en_core_web_sm")
        all_ents = []
        for p in pages:
            doc = nlp(p["text"][:50000])
            all_ents.extend(ent.text.strip() for ent in doc.ents if len(ent.text.strip()) > 1)
        ent_freq = Counter(all_ents).most_common(25)
    except ImportError:
        ent_freq = []

    brief = {
        "keyword": keyword,
        "recommended_word_count": f"{int(np.percentile(word_counts, 25))}-{int(np.percentile(word_counts, 75))}",
        "avg_competitor_words": int(np.mean(word_counts)),
        "median_competitor_words": int(np.median(word_counts)),
        "must_include_terms": must_include,
        "suggested_h2s": h2_freq,
        "key_entities": ent_freq,
        "competitor_count": len(pages),
    }
    return brief


def main():
    parser = argparse.ArgumentParser(description="Content Brief Generator")
    parser.add_argument("--urls", nargs="+", required=True, help="Competitor URLs")
    parser.add_argument("--keyword", required=True, help="Target keyword")
    parser.add_argument("--output", help="Save brief as XLSX")
    args = parser.parse_args()

    pages = []
    for url in args.urls:
        print(f"Fetching {url}...")
        p = fetch_text(url)
        if p:
            pages.append(p)
        time.sleep(1)

    if len(pages) < 2:
        print("Need at least 2 competitor pages"); sys.exit(1)

    brief = generate_brief(pages, args.keyword)

    print(f"\n{'=' * 60}")
    print(f"  CONTENT BRIEF: '{args.keyword}'")
    print(f"{'=' * 60}")
    print(f"  Based on {brief['competitor_count']} competitors")
    print(f"  Recommended word count: {brief['recommended_word_count']}")
    print(f"  Avg competitor: {brief['avg_competitor_words']} words")

    print(f"\n  Must-Include Terms (top 20):")
    for term, score, count in brief["must_include_terms"][:20]:
        print(f"    {term:<35} (score: {score}, in {count}/{brief['competitor_count']} pages)")

    print(f"\n  Suggested H2 Headings:")
    for h, count in brief["suggested_h2s"][:10]:
        print(f"    [{count}x] {h[:60]}")

    if brief["key_entities"]:
        print(f"\n  Key Entities to Mention:")
        for ent, count in brief["key_entities"][:15]:
            print(f"    {ent:<30} ({count} mentions)")

    if args.output:
        with pd.ExcelWriter(args.output, engine="openpyxl") as w:
            pd.DataFrame(brief["must_include_terms"], columns=["term", "tfidf", "doc_count"]).to_excel(w, sheet_name="Terms", index=False)
            pd.DataFrame(brief["suggested_h2s"], columns=["heading", "count"]).to_excel(w, sheet_name="H2 Suggestions", index=False)
            if brief["key_entities"]:
                pd.DataFrame(brief["key_entities"], columns=["entity", "count"]).to_excel(w, sheet_name="Entities", index=False)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
