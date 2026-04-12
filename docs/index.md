# Axle Documentation

Welcome to Axle CLI v1.3.0 — your guide to running Python microtools from the terminal.

## What is Axle?

Axle is a modular CLI platform. Drop any Python script into your `tools/` directory and run it consistently with a unified interface. No need to remember individual script locations or argument patterns.

## Quick Links

- [Installation Guide](installation.md) — Get Axle up and running
- [Usage Guide](usage.md) — How to run tools effectively
- [Command Reference](commands.md) — Complete command documentation
- [Security Guide](security.md) — Optional security validation
- [Troubleshooting](troubleshooting.md) — Solve common problems
- [Contributing](contributing.md) — Contribute to the project
- [Changelog](changelog.md) — Version history

---

## Getting Started

### 1. Install

```bash
pip install git+https://github.com/skpaul82/axle-cli.git
```

### 2. Launch Interactive Mode

```bash
axle
```

Navigate tools with ↑↓ arrows, press Enter to select, then type your arguments.

### 3. Or Run Directly

```bash
axle list                           # see all tools
axle competitor_analysis            # see examples for this tool
axle competitor_analysis --urls https://site.com --target-keyword "keyword"
axle 4 --urls https://site.com --target-keyword "keyword"
```

---

## Key Features (v1.3.0)

### 🖱️ Interactive Mode
Run `axle` with no arguments to get an arrow-key tool picker. After selecting a tool, Axle prompts you for the right type of input and echoes the constructed command before running.

### ⚡ Direct Execution
`axle <tool_name> [flags]` and `axle <N> [flags]` — tools run directly without going through `axle run`. Flags pass straight through to the tool's own argparse.

### 📌 Per-Tool Examples
`axle <tool_name>` with no args shows that tool's own examples (extracted from its `Usage:` docstring, converted to `axle` syntax). Never errors on missing args.

### 🔍 Smart Help
`axle help <tool>` — clean summary + examples.
`axle help <tool> --details` — full argparse options + function list.

### 🧠 Works with Any Python Script
No tool contract required. Axle auto-detects argparse tools, prompt-driven tools, and multi-function scripts.

### 🔒 Optional Security & Code Review
Both disabled by default. Enable per-run with `--security` / `--code-review`, or globally with `axle security --enable` / `axle review --enable`.

---

## System Requirements

- Python 3.10+
- RAM: 8 GB minimum (16 GB recommended)
- Disk: 5–8 GB free (ML models and caches)
- macOS, Linux, or Windows

## Support & Community

- ⭐ **GitHub**: [skpaul82/axle-cli](https://github.com/skpaul82/axle-cli)
- 🐦 **X/Twitter**: [@_skpaul82](https://x.com/_skpaul82)
- 🌐 **Website**: [www.axle.sanjoypaul.com](https://www.axle.sanjoypaul.com)
- 🌐 **FB Group**: [Agentic AIO](https://www.facebook.com/groups/agenticaio/)

## License

MIT License — see [LICENSE](../LICENSE) for details.
