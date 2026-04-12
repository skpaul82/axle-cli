# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

**Axle** is a **production-ready v1.3.0** Python CLI platform for running Python microtools from a shared tools directory.

## Project Overview

Axle is a modular CLI platform. Users drop Python scripts into a `tools/` directory and run them through a unified interface. v1.3.0 adds an interactive arrow-key menu, direct tool execution by name or number, and per-tool usage examples.

```
axle/
├── pyproject.toml              # Package metadata, dependencies, entry point
├── requirements.txt            # Pinned dependencies
├── README.md                   # Public landing page
├── LICENSE                     # MIT license
├── axle/
│   ├── axle.py                 # Main CLI router (~1500 lines)
│   ├── interactive.py          # Arrow-key menu and argument prompt UI (NEW v1.3.0)
│   ├── tool_discoverer.py      # Intelligent tool discovery + execution
│   ├── tool_validator.py       # Optional security validation
│   ├── code_reviewer.py        # Optional code review
│   ├── tool_metadata.py        # AST-based metadata extraction
│   ├── config.py               # Persistent configuration (~/.axle/config.json)
│   ├── install_axle.py         # Interactive setup script
│   └── security_scan.py        # Dependency vulnerability scanner
├── tools/                      # Modular tool scripts
│   ├── 01_seo_keyword_checker.py
│   ├── 02_meta_tag_auditor.py
│   ├── 03_daily_life_hack_generator.py
│   ├── competitor_analysis.py
│   ├── content_optimizer.py
│   └── ...
├── docs/                       # User documentation
├── website/                    # Static website (Cloudflare Pages)
└── .github/workflows/          # CI/CD
```

## Core Commands (v1.3.0)

### Direct execution (new preferred syntax)
- `axle` — interactive arrow-key tool picker (no args + TTY)
- `axle <tool_name>` — show tool examples (no extra args) OR run tool (with args)
- `axle <N>` — same, by tool number
- `axle <tool_name> [--flags]` — run tool with flags passed through
- `axle <N> [--flags]` — same, by number
- `axle <tool_name> <function> [args]` — call specific function in multi-function tools

### Classic run syntax (still works)
- `axle run <tool> [args]` — run a tool
- `axle run <tool> --security` — run with security validation
- `axle run <tool> --code-review` — run with code review

### Help
- `axle help <tool>` — show tool name, summary, and examples (clean default)
- `axle help <tool> --details` — full argparse options + function list
- `axle help <tool> -d` — same

### Tool management
- `axle list` — list all tools
- `axle info <tool>` — show tool description
- `axle scan` — dependency vulnerability scan
- `axle doctor` — environment diagnostics
- `axle path` — show tools folder location

### Configuration
- `axle security --enable/--disable/--show`
- `axle review --enable/--disable/--show`
- `axle update` / `axle update --check`
- `axle metadata scan/show/search/list`

## Real-World Examples (v1.3.0)

```bash
axle competitor_analysis --urls https://rival.com --target-keyword "web developer"
axle 4 --urls https://rival.com --target-keyword "web developer"

axle content_optimizer --url https://mysite.com/blog --target-keyword "cloud hosting"
axle content_optimizer --file article.html --target-keyword "SaaS" --competitors c1.html c2.html
axle content_optimizer --text "Your content..." --target-keyword "best crm software"

axle seo_keyword_checker "python is great for data science"
```

## Architecture Principles

### Tool Types (v1.3.0)
Axle auto-detects three types — no contract required:

1. **Argparse-based** — `main()` takes 0 args, uses argparse internally. Flags pass through directly.
2. **Contract-based** — implements `get_description()` + `main(prompt: str)`. Takes free-text prompt.
3. **Multi-function** — any other Python script. Functions called by name.

### Interactive Mode (NEW v1.3.0)
`axle/interactive.py` provides:
- `arrow_select(items, title, format_item, max_visible)` — reusable arrow-key list selector
- `run_interactive(tools_dir)` — full interactive launch flow, returns `(DiscoveredTool, args_list)`

Triggered in `main()` when `len(sys.argv) == 1` and `sys.stdin.isatty() and sys.stdout.isatty()`.

### Per-Tool Examples (NEW v1.3.0)
`DiscoveredTool.get_docstring_examples()` parses the `Usage:` block from a tool's module docstring and converts `python tool_name.py --args` → `axle tool_name  --args`.

`DiscoveredTool.get_argparse_help()` captures the tool's `--help` output (via stdout redirect + SystemExit catch) and rewrites `usage: tool_name` → `usage: axle tool_name`.

### Show-help-on-no-args (NEW v1.3.0)
All three tool-type branches in `main()` now check `if not tool_args:` and show `get_help_text()` instead of running (which would error on missing required args).

### Help Verbosity (NEW v1.3.0)
`get_help_text(verbose=False)`:
- Default: name + summary + `📌 Examples` (from docstring) + hint for `--details`
- `verbose=True`: also shows full argparse `--help` output + all functions

`axle help` parser uses `--details` / `-d` (renamed from `--verbose`).

### Dynamic Tool Loading
Tools discovered from `tools/` via `ToolDiscoverer`. Can invoke by name (with or without numeric prefix) or by number.

## Key Files

- **axle/axle.py**: Main CLI router. `main()` handles interactive mode, early tool dispatch (before argparse), and all built-in commands.
- **axle/interactive.py**: Arrow-key terminal UI. No external dependencies (`tty`, `termios`, `select` are all stdlib).
- **axle/tool_discoverer.py**: `DiscoveredTool` + `ToolDiscoverer`. Handles discovery, help generation, and execution.

## Branding & URLs

- **Product Name**: Axle
- **Command**: `axle`
- **Version**: 1.3.0
- **Repository**: https://github.com/skpaul82/axle-cli
- **Website**: https://www.axle.sanjoypaul.com
- **Email**: hello@skpaul.me

## Community Footer

All tool outputs include:
```
⭐ Star on GitHub: https://github.com/skpaul82/axle-cli
🐦 Follow on X: @_skpaul82
🌐 Website: https://www.axle.sanjoypaul.com
```

## Platform Philosophy

Axle is a **platform for tools**, not a toolkit. Drop any `.py` file in `tools/` and run it with `axle tool_name`. No contract required in v1.3.0.

## License

MIT — see LICENSE file.

## Internal Documentation

Planning and historical docs in `.docs/`:
- **PRD.md** — Product Requirements Document
- **CONTEXT.md** — Architecture and technical decisions
- **IMPLEMENTATION_PLAN.md** — Implementation phases
- **VERSION_1.3.0_RELEASE_NOTES.md** — v1.3.0 release notes
