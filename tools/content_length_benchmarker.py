"""
Content Length Benchmarker
============================
Benchmarks content length, depth, and structure against competitor pages.
Recommends optimal word count, heading count, and media usage.

Usage:
    python content_length_benchmarker.py --my-url https://mysite.com/page --competitor-urls https://a.com https://b.com
    python content_length_benchmarker.py --competitor-urls https://a.com https://b.com https://c.com --keyword "best vpn"
"""

import argparse, re, sys, time
import numpy as np, pandas as pd

def analyze_page(url):
    import requests
    from bs4 import BeautifulSoup
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        for t in soup(["script","style","nav","footer"]): t.decompose()
        text = re.sub(r"\s+"," ",soup.get_text(" ",strip=True))
        words = re.findall(r"\b\w+\b", text)
        sentences = [s for s in re.split(r"[.!?]+", text) if len(s.strip())>5]
        h2s = len(soup.find_all("h2"))
        h3s = len(soup.find_all("h3"))
        images = len(soup.find_all("img"))
        lists = len(soup.find_all(["ul","ol"]))
        tables = len(soup.find_all("table"))
        paras = len([p for p in soup.find_all("p") if len(p.get_text(strip=True))>20])
        return {
            "url": url[:60], "word_count": len(words), "sentence_count": len(sentences),
            "paragraph_count": paras, "h2_count": h2s, "h3_count": h3s,
            "image_count": images, "list_count": lists, "table_count": tables,
            "avg_sent_length": round(len(words)/max(len(sentences),1),1),
        }
    except Exception as e:
        print(f"  Failed: {url} — {e}"); return None

def main():
    parser = argparse.ArgumentParser(description="Content Length Benchmarker")
    parser.add_argument("--my-url", help="Your page URL")
    parser.add_argument("--competitor-urls", nargs="+", required=True)
    parser.add_argument("--keyword", help="Target keyword")
    parser.add_argument("--output", help="Save as XLSX")
    args = parser.parse_args()

    comp_pages = []
    for u in args.competitor_urls:
        print(f"Analyzing {u}...")
        p = analyze_page(u)
        if p: comp_pages.append(p)
        time.sleep(0.5)

    my_page = None
    if args.my_url:
        print(f"Analyzing your page: {args.my_url}...")
        my_page = analyze_page(args.my_url)

    if not comp_pages: print("No competitor pages loaded"); sys.exit(1)

    # Compute benchmarks
    metrics = ["word_count","sentence_count","paragraph_count","h2_count","h3_count","image_count","list_count","table_count"]
    benchmarks = {}
    for m in metrics:
        vals = [p[m] for p in comp_pages]
        benchmarks[m] = {"min": min(vals), "max": max(vals), "avg": round(np.mean(vals),1),
                         "median": round(np.median(vals),1), "p75": round(np.percentile(vals,75),1)}

    print(f"\n{'='*70}")
    print(f"  CONTENT LENGTH BENCHMARK ({len(comp_pages)} competitors)")
    if args.keyword: print(f"  Keyword: '{args.keyword}'")
    print(f"{'='*70}")

    print(f"\n  {'Metric':<20} {'Min':>6} {'Avg':>8} {'Median':>8} {'P75':>8} {'Max':>6}", end="")
    if my_page: print(f" {'Yours':>8} {'Gap':>8}")
    else: print()

    for m in metrics:
        b = benchmarks[m]
        line = f"  {m:<20} {b['min']:>6} {b['avg']:>8} {b['median']:>8} {b['p75']:>8} {b['max']:>6}"
        if my_page:
            val = my_page[m]
            gap = val - b["avg"]
            icon = "✅" if gap >= 0 else "⚠️"
            line += f" {val:>8} {icon}{gap:>+6}"
        print(line)

    # Recommendations
    if my_page:
        print(f"\n  Recommendations:")
        if my_page["word_count"] < benchmarks["word_count"]["avg"]:
            target = int(benchmarks["word_count"]["p75"])
            print(f"    📝 Increase word count to ~{target} words (+{target - my_page['word_count']})")
        if my_page["h2_count"] < benchmarks["h2_count"]["avg"]:
            print(f"    📋 Add more H2 subheadings (target: {int(benchmarks['h2_count']['avg'])})")
        if my_page["image_count"] < benchmarks["image_count"]["avg"]:
            print(f"    🖼️  Add more images (target: {int(benchmarks['image_count']['avg'])})")
        if my_page["list_count"] < benchmarks["list_count"]["avg"]:
            print(f"    📌 Add lists for scannability (target: {int(benchmarks['list_count']['avg'])})")

    if args.output:
        rows = comp_pages + ([my_page] if my_page else [])
        pd.DataFrame(rows).to_excel(args.output, index=False)
        print(f"\nSaved to {args.output}")

if __name__ == "__main__":
    main()
