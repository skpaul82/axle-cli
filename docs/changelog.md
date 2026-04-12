# Changelog

All notable changes to Axle CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.0] - 2026-04-12

### ✨ Major Features

#### Interactive Arrow-Key Menu
- **`axle` (no arguments)** on a real terminal now launches a full interactive tool picker
- Arrow-key navigation (↑↓ / j k), Enter to select, q to cancel
- Scrollable list — works with any number of tools
- After selection: context-aware argument prompt based on tool type
  - Argparse tools: prompts for CLI flags
  - Contract tools: prompts for free-text prompt
  - Multi-function tools: shows available functions + prompts for args
- Echoes the resolved `axle tool_name [args]` command before running
- Gracefully falls back to standard help if terminal is not interactive

#### Direct Tool Execution (No `axle run` Required)
- `axle <tool_name> [flags]` runs the tool directly — same as `axle run`
- `axle <N> [flags]` runs by tool number — flags pass through to the tool
- Examples that now work natively:
  ```bash
  axle competitor_analysis --urls https://site.com --target-keyword "keyword"
  axle 4 --urls https://site.com --target-keyword "keyword"
  axle content_optimizer --file article.html --target-keyword "SaaS"
  ```

#### Per-Tool Usage Examples on Help
- `axle <tool_name>` (no args) now shows the tool's own examples instead of erroring
- `axle help <tool_name>` shows the same clean summary + examples
- Examples are extracted from each tool's `Usage:` docstring automatically
- `python tool_name.py --args` lines are rewritten to `axle tool_name --args`
- Works for all tool types: argparse, contract, and multi-function

#### Simplified Help Output
- Default `axle help <tool>` shows only: **name → summary → examples**
- New `--details` / `-d` flag shows full argparse options + function list:
  ```bash
  axle help content_optimizer            # summary + examples only
  axle help content_optimizer --details  # full options + all functions
  ```

#### Function-Name Detection for Multi-Function Tools
- `axle <tool_name> <function_name> [args]` intelligently detects if the first
  argument is a valid function name in the tool and routes to it directly
- Works for both `axle tool_name func` and `axle run tool_name func` syntax

### 🔧 Technical Changes
- New `axle/interactive.py` module — arrow-key selector and argument prompt UI
- `tool_discoverer.py`: added `get_docstring_examples()`, `get_argparse_help()` methods
- `tool_discoverer.py`: `get_help_text()` refactored — default = name/summary/examples only
- `axle.py`: interactive mode entry in `main()` when no args + TTY detected
- `axle.py`: all tool branches (`argparse`, `contract`, `multi-fn`) show help on no args
- `axle.py`: `--verbose` renamed to `--details` on `axle help` subparser
- `axle.py`: argparse epilog updated with real-world command examples

### 📚 Documentation
- README updated to v1.3.0 with direct-execution examples
- All docs updated: usage guide, command reference, index
- Website updated with new features and examples
- CLAUDE.md updated with new command patterns
- Internal .docs/ updated

---

## [1.2.0] - 2026-04-12

### ✨ Major Features

#### Optional Security & Code Review (Breaking Change)
- Security validation now **DISABLED by default** (was "warn" policy)
- Code review now **DISABLED by default** (was "auto" policy)
- New `--security` flag: enable security validation per-run
- New `--code-review` flag: enable code review per-run
- `axle security --enable/--disable/--show`
- `axle review --enable/--disable/--show`
- Configuration stored in `~/.axle/config.json`

#### Built-in Update Command
- `axle update` — update to latest via git pull + pip install
- `axle update --check` — check without installing

#### Tool Metadata System
- `axle metadata scan` — scan all tools and build metadata cache
- `axle metadata show <tool>` — detailed tool information
- `axle metadata search <query>` — search by name, function, description
- `axle metadata list` — list all tools with summaries

#### Intelligent Tool Discovery
- Axle now works with ANY Python script — no contract required
- Auto-detects argparse tools, contract tools, multi-function scripts
- Extracts functions, classes, docstrings automatically
- Direct execution: `axle tool_name [args]` without `axle run`

### 🔧 Technical Changes
- New `axle/config.py` — persistent configuration
- New `axle/tool_metadata.py` — AST-based metadata extraction
- New `axle/tool_discoverer.py` — intelligent tool discovery engine
- Updated `axle/tool_validator.py` — default policy: permissive
- Updated `axle/code_reviewer.py` — default policy: never

---

## [1.1.1] - 2026-04-09

### Added
- Version command: `axle -V`, `axle --version`
- Auto-creation of tools directory on package installation

### Updated
- Community links updated across all documentation
- Help documentation enhanced

### Fixed
- `pyproject.toml` configuration (classifiers, dependencies)
- Tools directory path handling

---

## [1.1.0] - 2026-04-08

### Added
- `axle uninstall` command (preserves tools directory by default)

### Enhanced
- Environment checking in interactive installer
- Comprehensive validation at startup

### Fixed
- Package structure: `scripts/` → `axle/` for standard Python packaging
- Entry point: `axle.axle:main`

---

## [1.0.0] - 2026-04-08

### Added
- Initial production release of Axle CLI platform
- Core CLI: list, run, info, scan, doctor, path, help, security, uninstall
- Tool numbering system
- Dynamic tool loading and discovery
- Community footer in all outputs
- SEO Keyword Checker, Meta Tag Auditor, Daily Life Hack Generator
- Pre-execution security validation (mandatory at launch)
- Dependency vulnerability scanner (pip-audit)
- Interactive installer
- GitHub Actions CI/CD

---

## Versioning Policy

[Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New backwards-compatible features
- **PATCH**: Bug fixes

## Links

- ⭐ **GitHub:** [skpaul82/axle-cli](https://github.com/skpaul82/axle-cli)
- 🐦 **X/Twitter:** [@_skpaul82](https://x.com/_skpaul82)
- 🌐 **Website:** [www.axle.sanjoypaul.com](https://www.axle.sanjoypaul.com)
