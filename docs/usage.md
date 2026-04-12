# Usage Guide

How to use Axle CLI v1.3.0 effectively.

---

## The Two Ways to Run Tools

Axle gives you two equally good ways to run tools:

### 1. Interactive mode (recommended for exploration)

```bash
axle
```

Run with no arguments on a real terminal. A scrollable arrow-key menu appears — pick a tool, type your arguments, and Axle runs it.

### 2. Direct mode (recommended for scripting / daily use)

```bash
axle <tool_name> [flags or prompt]
axle <N> [flags or prompt]
```

No subcommand needed. Flags pass straight through to the tool.

---

## Understanding Tool Types

Axle works with any Python script. There are three types:

### Argparse-based tools
These have their own CLI flags. Run them like any CLI tool:

```bash
axle competitor_analysis --urls https://rival.com --target-keyword "web developer"
axle content_optimizer --file article.html --target-keyword "SaaS"
```

### Contract-based tools
These accept a free-text prompt:

```bash
axle seo_keyword_checker "python is a great language for data science"
axle daily_life_hack_generator "morning routine tips"
```

### Multi-function tools
These expose multiple callable functions. Call them directly:

```bash
axle my_tool                    # runs main()
axle my_tool analyze            # runs analyze()
axle my_tool export output.csv  # runs export("output.csv")
```

---

## Discovering What a Tool Expects

### See examples for any tool

```bash
axle competitor_analysis     # shows tool's own examples
axle 4                       # same, by number
```

Output:
```
Tool: competitor_analysis
============================================================

SERP & Competitor Content Analysis

📌 Examples:
  axle competitor_analysis  --urls https://comp1.com https://comp2.com --target-keyword "cloud hosting"
  axle competitor_analysis  --files comp1.html comp2.html --target-keyword "crm software"

  axle help competitor_analysis --details   # full options & function list
```

### See full options

```bash
axle help content_optimizer --details
```

Shows the complete argparse options list and all functions in the module.

---

## Real-World Examples

### SEO competitor analysis

```bash
# Analyze competitor URLs
axle competitor_analysis --urls https://rival1.com https://rival2.com --target-keyword "web developer"

# By number (same tool)
axle 4 --urls https://rival1.com https://rival2.com --target-keyword "web developer"

# With local HTML files
axle competitor_analysis --files comp1.html comp2.html --target-keyword "crm software"

# Including your own content for gap analysis
axle competitor_analysis --urls https://rival.com --my-content my_page.html --target-keyword "seo tools"

# Save results to Excel
axle competitor_analysis --urls https://rival.com --target-keyword "keyword" --output report.xlsx
```

### Content optimization

```bash
# Analyze a live URL
axle content_optimizer --url https://mysite.com/blog --target-keyword "cloud hosting"
axle 5 --url https://mysite.com/blog --target-keyword "cloud hosting"

# Analyze a local file (with competitor files)
axle content_optimizer --file article.html --target-keyword "SaaS" --competitors c1.html c2.html

# Analyze raw text
axle content_optimizer --text "Your content here..." --target-keyword "best crm software"

# Save HTML report
axle content_optimizer --url https://mysite.com --target-keyword "keyword" --output report.html
```

### Keyword & meta analysis (prompt-based tools)

```bash
axle seo_keyword_checker "python is a great language for data science and machine learning"
axle meta_tag_auditor "https://example.com"
axle meta_tag_auditor "./page.html"
```

---

## Using `axle list`

Shows all tools with their number, type, and description:

```bash
axle list
```

```
🔧 Available tools
============================================================

Found 8 tool(s):

  1. ✅ 01_seo_keyword_checker    SEO Keyword Checker
  2. ✅ 02_meta_tag_auditor        Meta Tag Auditor
  3. ✅ 03_daily_life_hack_generator  Daily Life Hack Generator
  4. 📜 competitor_analysis       SERP & Competitor Content Analysis
  5. 📜 content_optimizer         Content Optimization & SEO Scoring
  ...
```

Badge legend:
- ✅ — contract-based tool (`get_description` + `main(prompt)`)
- 📜 — standalone script (argparse or multi-function)

---

## Interactive Mode in Detail

```bash
axle
```

```
  Axle CLI  —  Choose a tool to run
  ──────────────────────────────────────────────────────────
  ↑ ↓  navigate    Enter  select    q  quit

▶  4.  📜  competitor_analysis            SERP & Competitor Content...
   5.  📜  content_optimizer              Content Optimization & SE...
   1.  ✅  01_seo_keyword_checker         SEO Keyword Checker - Ana...
   ...
```

After selection (argparse tool):
```
  ▶ competitor_analysis  —  SERP & Competitor Content Analysis

  Argparse-based tool — pass flags directly.
  Press Enter with no input to show --help.

  e.g.  axle competitor_analysis --flag value
  ▸ --urls https://rival.com --target-keyword "web developer"

  Running:  axle competitor_analysis --urls https://rival.com --target-keyword "web developer"
```

---

## Security & Code Review

Both are **disabled by default** for speed.

Enable per-run:
```bash
axle run seo_keyword_checker "keyword" --security
axle run seo_keyword_checker "keyword" --code-review
```

Enable globally:
```bash
axle security --enable
axle review --enable
```

Check current settings:
```bash
axle security --show
axle review --show
```

---

## Adding Your Own Tools

Find your tools directory:
```bash
axle path
```

### Argparse tool (for flag-driven tools)

```python
"""
My Custom Tool
==============
Does something useful.

Usage:
    python my_tool.py --input data.csv --output results.json
    python my_tool.py --url https://example.com --verbose
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description="My Custom Tool")
    parser.add_argument("--input", help="Input file")
    parser.add_argument("--output", default="out.json", help="Output file")
    args = parser.parse_args()
    # your logic here

if __name__ == "__main__":
    main()
```

Run immediately:
```bash
axle my_tool --input data.csv
axle my_tool                    # shows your Usage: examples
```

### Contract tool (for prompt-driven tools)

```python
def get_description() -> str:
    return "Brief description of what this tool does"

def main(prompt: str) -> None:
    print(f"Processing: {prompt}")
```

```bash
axle my_tool "your prompt here"
```

### Tool numbering

Prefix files with `XX_` for consistent ordering:
```
tools/
  01_seo_keyword_checker.py
  04_my_tool.py
  05_another_tool.py
```

---

## Tips

1. **Add `Usage:` to your docstrings** — Axle extracts these as `axle`-prefixed examples automatically.
2. **Use numbers for quick access** — `axle 4 --args` is faster to type than the full name.
3. **`--details` for deep dives** — `axle help tool --details` shows every argparse flag and every function.
4. **Interactive mode for discovery** — use `axle` when you're not sure which tool to use.
5. **Chain commands** — `axle scan && axle list && axle seo_keyword_checker "keyword"`
