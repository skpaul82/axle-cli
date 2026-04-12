# Axle v1.3.0

A modular CLI platform for running Python microtools from a shared tools directory.

---

## 🚀 Quick Install

```bash
pip install git+https://github.com/skpaul82/axle-cli.git
```

Or clone manually:

```bash
git clone https://github.com/skpaul82/axle-cli.git
cd axle-cli
pip install -r requirements.txt
pip install -e .
```

> **Note**: PyPI installation (`pip install axle-cli`) is planned for a future release.

---

## 🎉 What's New in v1.3.0

### 🖱️ Interactive Arrow-Key Menu
Run `axle` with no arguments to get a full interactive tool picker — navigate with ↑↓ arrow keys, press Enter to select, then type your arguments:

```bash
axle       # opens interactive menu
```

### ⚡ Direct Tool Execution (No `axle run` needed)
Run any tool directly by name **or number** — flags pass straight through to the tool:

```bash
axle competitor_analysis --urls https://rival.com --target-keyword "web developer"
axle 4 --urls https://rival.com --target-keyword "web developer"

axle content_optimizer --url https://mysite.com --target-keyword "cloud hosting"
axle 5 --url https://mysite.com --target-keyword "cloud hosting"

axle content_optimizer --file article.html --target-keyword "SaaS" --competitors c1.html c2.html
axle content_optimizer --text "Your content here..." --target-keyword "best crm software"

axle seo_keyword_checker "target keyword to analyse"
```

### 📌 Per-Tool Example Commands
Running `axle tool_name` or `axle N` with no extra args now shows that tool's own usage examples (pulled from its `Usage:` docstring, automatically converted to `axle` syntax):

```bash
axle competitor_analysis     # shows examples for this tool
axle 4                       # same — works by number too
axle help content_optimizer  # same, via help command
```

### 🔍 Simplified `axle help`
`axle help <tool>` now shows only: **name → summary → examples**. Use `--details` for the full options list and function inventory:

```bash
axle help content_optimizer            # clean summary + examples
axle help content_optimizer --details  # full argparse options + functions
```

---

## 📦 Features

### 🖱️ Interactive Mode
- Launch `axle` with no arguments on a real terminal to get an arrow-key tool picker
- Navigates with ↑↓ / j k, Enter to select, q to quit
- After selection: context-aware argument prompt (flags / prompt / function)
- Echoes the resolved command before running

### ⚡ Direct Execution
- `axle <tool_name> [flags]` — run without going through `axle run`
- `axle <N> [flags]` — run by tool number
- `axle <tool_name> <function> [args]` — call specific function in multi-function tools
- `axle <tool_name>` alone → shows tool examples, never errors

### 📌 Smart Per-Tool Help
- Examples extracted automatically from each tool's `Usage:` docstring
- `python tool.py --args` → shown as `axle tool_name --args`
- `axle help <tool> --details` for full argparse options + function list

### 🔒 Optional Security Validation
- Pre-execution security scan (disabled by default)
- Enable per-run: `axle run <tool> --security`
- Enable globally: `axle security --enable`
- Policies: strict / warn / permissive

### 🔍 Optional Code Review
- Automatic code quality checks before running (disabled by default)
- Enable per-run: `axle run <tool> --code-review`
- Enable globally: `axle review --enable`
- Auto-fixes formatting and import issues

### 🧠 Intelligent Tool Discovery
- Works with **any** Python script — no contract required
- Auto-detects argparse-based tools, contract tools, and multi-function scripts
- Extracts functions, docstrings, and usage examples automatically

---

## 🛠️ Commands

### Running Tools

| Command | Description |
|---------|-------------|
| `axle` | Interactive arrow-key tool picker |
| `axle <tool_name>` | Show tool examples (no args) or run directly |
| `axle <N>` | Same, by tool number |
| `axle <tool_name> [--flags]` | Run tool with flags passed through |
| `axle <N> [--flags]` | Same, by number |

### Built-in Commands

| Command | Description |
|---------|-------------|
| `axle list` | List all available tools |
| `axle run <tool> [args]` | Run a tool (classic syntax) |
| `axle run <tool> --security` | Run with security validation |
| `axle run <tool> --code-review` | Run with code review |
| `axle help <tool>` | Show tool examples |
| `axle help <tool> --details` | Show full options + function list |
| `axle info <tool>` | Show tool description |
| `axle scan` | Dependency vulnerability scan |
| `axle doctor` | Environment diagnostics |
| `axle path` | Show tools folder location |
| `axle security --enable/--disable/--show` | Configure security |
| `axle review --enable/--disable/--show` | Configure code review |
| `axle update` | Update to latest version |
| `axle update --check` | Check for updates |
| `axle metadata scan/show/search/list` | Tool metadata system |
| `axle -V` | Show version |

---

## 💡 Real-World Examples

```bash
# SEO competitor analysis
axle competitor_analysis --urls https://rival1.com https://rival2.com --target-keyword "web developer"
axle 4 --urls https://rival1.com https://rival2.com --target-keyword "web developer"

# Content optimization
axle content_optimizer --url https://mysite.com/blog --target-keyword "cloud hosting"
axle content_optimizer --file article.html --target-keyword "SaaS" --competitors c1.html c2.html
axle content_optimizer --text "Your content here..." --target-keyword "best crm software"

# SEO keyword analysis (prompt-based)
axle seo_keyword_checker "python is great for data science"

# See all tools interactively
axle

# Get help for a specific tool
axle help competitor_analysis
axle help competitor_analysis --details
```

---

## 🧱 Requirements

- Python 3.10+
- RAM: 8 GB minimum, 16 GB preferred
- Disk: 5–8 GB free (for ML models and caches)

---

## 🔧 Adding Your Own Tools

Axle works with **any** Python script. Just drop it in your `tools/` directory.

### Argparse-based tool (recommended for flag-driven tools)

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="My Tool")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="out.json")
    args = parser.parse_args()
    # your logic here

if __name__ == "__main__":
    main()
```

Run it as:
```bash
axle my_tool --input data.csv
```

### Contract-based tool (for prompt-driven tools)

```python
def get_description() -> str:
    return "Brief description of what this tool does"

def main(prompt: str) -> None:
    print(f"Processing: {prompt}")
```

Run it as:
```bash
axle my_tool "your prompt here"
```

### Tool numbering

Use `XX_tool_name.py` for ordering:
```
tools/
  01_seo_keyword_checker.py
  02_meta_tag_auditor.py
  04_my_tool.py
```

Find your tools directory: `axle path`

---

## 📝 Docs

- `docs/index.md` — overview
- `docs/usage.md` — how to use tools
- `docs/commands.md` — complete command reference
- `docs/security.md` — security validation
- `docs/installation.md` — step-by-step setup
- `docs/changelog.md` — version history

---

## 🌐 Community & Support

- ⭐ **Star on GitHub**: [skpaul82/axle-cli](https://github.com/skpaul82/axle-cli)
- 🐦 **Follow on X**: [@_skpaul82](https://x.com/_skpaul82)
- 🌐 **Website**: [www.axle.sanjoypaul.com](https://www.axle.sanjoypaul.com)
- 🌐 **FB Group**: [Agentic AIO](https://www.facebook.com/groups/agenticaio/)

---

## 📄 License

MIT License – see `LICENSE` for details.

---

♥ Built for the community.
♥ Shared with love for creators, builders, and learners.
