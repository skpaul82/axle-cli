# Command Reference

Complete reference for all Axle CLI commands — v1.3.0.

---

## Quick Command Map

| Command | Description |
|---------|-------------|
| `axle` | Interactive arrow-key tool picker |
| `axle list` | List all available tools |
| `axle <tool_name>` | Show tool examples (no args) or run tool |
| `axle <N>` | Same, by tool number |
| `axle <tool_name> [--flags]` | Run tool — flags pass to the tool |
| `axle <N> [--flags]` | Same, by number |
| `axle run <tool> [args]` | Classic run syntax |
| `axle run <tool> --security` | Run with security validation |
| `axle run <tool> --code-review` | Run with code review |
| `axle help <tool>` | Show tool summary + examples |
| `axle help <tool> --details` | Show full options + function list |
| `axle info <tool>` | Show tool description |
| `axle scan` | Dependency vulnerability scan |
| `axle doctor` | Environment diagnostics |
| `axle path` | Show tools folder location |
| `axle security --enable/--disable/--show` | Configure security |
| `axle review --enable/--disable/--show` | Configure code review |
| `axle update` | Update to latest version |
| `axle update --check` | Check for updates |
| `axle metadata scan/show/search/list` | Tool metadata |
| `axle uninstall` | Uninstall Axle |
| `axle -V` | Show version |

---

## axle (no arguments)

Launch the interactive tool picker.

```bash
axle
```

Only activates when running in a real terminal (TTY). If stdout is piped or non-interactive, falls back to showing the standard help.

**Navigation:**
- `↑` / `k` — move up
- `↓` / `j` — move down
- `Enter` — select tool
- `q` / `Esc` / `Ctrl+C` — cancel

After selecting a tool, Axle shows a context-aware argument prompt:
- **Argparse tools** — prompts for CLI flags (shows example)
- **Contract tools** — prompts for free-text prompt
- **Multi-function tools** — shows available functions, prompts for `[function] [args]`

Then echoes the resolved command and runs:
```
  Running:  axle competitor_analysis --urls https://rival.com --target-keyword "seo"
```

---

## axle list

List all tools in the tools directory.

```bash
axle list
```

Shows each tool's number, name, type badge, and description. If running in a terminal, also shows the interactive mode tip.

---

## axle \<tool_name\> / axle \<N\>

Run a tool directly by name or number.

### With no arguments — shows examples

```bash
axle competitor_analysis        # shows this tool's Usage: examples
axle 4                          # same, by number
axle content_optimizer          # shows examples for content_optimizer
```

Output:
```
============================================================
Tool: competitor_analysis
============================================================

SERP & Competitor Content Analysis

📌 Examples:
  axle competitor_analysis  --urls https://comp1.com https://comp2.com --target-keyword "cloud hosting"
  axle competitor_analysis  --files comp1.html comp2.html --target-keyword "crm software"
  axle competitor_analysis  --urls https://a.com --target-keyword "seo tools" --output report.xlsx

  axle help competitor_analysis --details   # full options & function list
```

### With arguments — runs the tool

```bash
# Run by name with flags
axle competitor_analysis --urls https://rival.com --target-keyword "web developer"

# Run by number with flags
axle 4 --urls https://rival.com --target-keyword "web developer"

# Content optimizer examples
axle content_optimizer --url https://mysite.com/page --target-keyword "cloud hosting"
axle content_optimizer --file article.html --target-keyword "SaaS" --competitors c1.html c2.html
axle content_optimizer --text "Your article content..." --target-keyword "best crm software"

# Contract-based tool (takes a prompt)
axle seo_keyword_checker "python is a great language for data science"
axle 1 "python is a great language for data science"

# Multi-function tool — call a specific function
axle my_tool analyze --input data.csv
axle my_tool export --output results.json
```

### With --help / -h

Shows the tool's own help instead of running:
```bash
axle competitor_analysis --help
axle 4 -h
```

---

## axle run

Classic run syntax — equivalent to `axle <tool_name> [args]`.

```bash
axle run <tool_identifier> [func] [args...] [--security] [--code-review]
```

**Arguments:**
- `tool_identifier` — tool number or name (without `.py`)
- `func` *(optional)* — specific function to call (for multi-function tools)
- `args` *(optional)* — arguments passed to the tool

**Options:**
- `--security` — enable security validation for this run
- `--code-review` — enable code review for this run

```bash
axle run 1 "keyword to check"
axle run seo_keyword_checker "keyword to check"
axle run competitor_analysis --urls https://site.com --target-keyword "seo"
axle run 1 "test" --security --code-review
```

---

## axle help

Show help for a specific tool or general help.

```bash
axle help                          # general help (all commands + examples)
axle help <tool_name>              # tool summary + examples
axle help <tool_name> --details    # full options + function list
axle help <tool_name> -d           # same
```

### Default output (no `--details`)

Shows: **name → one-line summary → 📌 Examples → hint for --details**

```
============================================================
Tool: content_optimizer
============================================================

Content Optimization & SEO Scoring

📌 Examples:
  axle content_optimizer  --url https://example.com/page --target-keyword "project management tools"
  axle content_optimizer  --file article.html --target-keyword "cloud hosting" --competitors comp1.html comp2.html
  axle content_optimizer  --text "Your content here..." --target-keyword "best crm software"

  axle help content_optimizer --details   # full options & function list
```

### With `--details`

Adds:
- **📋 Options** — full argparse `--help` output (reformatted with `axle` prefix)
- **🔧 Functions** — all functions in the module with signatures and docstrings

---

## axle info

Show file location and description for a tool.

```bash
axle info <tool_name>
```

---

## axle scan

Dependency vulnerability scan using pip-audit and static analysis.

```bash
axle scan
```

Checks:
1. Dependencies — pip-audit for CVEs
2. Scripts — basic static analysis (eval, exec, hardcoded secrets)

---

## axle doctor

Environment diagnostics.

```bash
axle doctor
```

Checks Python version, disk space, RAM, key dependencies, tools directory, and CLI installation.

---

## axle path

Show tools folder location and contents.

```bash
axle path
```

---

## axle security

Configure security validation.

```bash
axle security --enable    # enable by default for all runs
axle security --disable   # disable (default)
axle security --show      # show current setting
axle security --policy <strict|warn|permissive>
```

---

## axle review

Run code review or configure it.

```bash
axle review <tool_name>          # review a specific tool
axle review --all                # review all tools
axle review --all --fix          # review + apply auto-fixes
axle review --all --dry-run      # preview fixes without applying
axle review --enable             # enable by default for all runs
axle review --disable            # disable (default)
axle review --show               # show current setting
```

---

## axle update

Update Axle to the latest version.

```bash
axle update           # pull latest + reinstall
axle update --check   # check for updates without installing
```

---

## axle metadata

Tool metadata commands.

```bash
axle metadata scan               # scan all tools, build cache
axle metadata list               # list all tools with summaries
axle metadata show <tool>        # detailed metadata for one tool
axle metadata search <query>     # search by name, function, description
```

---

## axle uninstall

Uninstall Axle (tools directory preserved by default).

```bash
axle uninstall               # preserves tools/
axle uninstall --remove-tools  # also removes tools/
```

---

## Global Options

```bash
axle -h / --help     # general help
axle -V / --version  # show version
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error |
| 2 | Invalid argument |

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `AXLE_SECURITY_POLICY` | Security policy (strict/warn/permissive) | `permissive` |
| `AXLE_CODE_REVIEW` | Code review policy | `never` |
| `AXLE_AUTO_FIX` | Auto-fix policy | `false` |

---

## See Also

- [Usage Guide](usage.md)
- [Installation Guide](installation.md)
- [Troubleshooting](troubleshooting.md)
