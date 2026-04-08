# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

**Axle** is a **production-ready v0.1.0** Python CLI platform for running Python microtools from a shared tools directory. The project has been fully implemented and rebranded from the original "Buddy CLI" concept to "Axle" with platform positioning.

## Project Overview

Axle is a modular CLI platform that allows users to drop Python scripts into a `tools/` directory and run them consistently through a unified interface. It's designed as a platform for tools (not a toolkit), with the philosophy that anyone can add tools without modifying core code.

```
axle/
├── pyproject.toml           # Package metadata, dependencies, CLI entry point
├── requirements.txt         # Pinned dependencies
├── README.md               # Public landing page
├── LICENSE                 # MIT license
├── scripts/
│   ├── axle.py             # Main CLI router with argparse (7 commands)
│   ├── install_axle.py     # Interactive setup script
│   └── security_scan.py    # Dependency vulnerability scanner
├── tools/                  # Modular tool scripts (numbered)
│   ├── 01_seo_keyword_checker.py
│   ├── 02_meta_tag_auditor.py
│   └── 03_daily_life_hack_generator.py
├── docs/                   # User documentation
└── .github/workflows/      # CI/CD configuration
```

## Core Commands

The CLI interface (`axle` command):

- `axle list` - List all available tools in the tools directory
- `axle run <number_or_name> <prompt>` - Execute a tool by number or filename
- `axle info <tool_name>` - Show tool description
- `axle scan` - Run dependency vulnerability checks
- `axle doctor` - Environment and setup diagnostics
- `axle path` - Show tools folder location
- `axle help` - Display command help

## Architecture Principles

**Tool Contract**: All tools MUST implement two functions:

```python
def get_description() -> str:
    """Return one-line description of the tool."""
    return "Brief description"

def main(prompt: str) -> None:
    """Main entry point. Called by CLI router."""
    # Tool logic here
    pass
```

**Dynamic Tool Loading**: Tools are discovered automatically from the `tools/` directory using importlib. Tools can be invoked by number (as displayed by `axle list`) or by filename without the `.py` extension (with or without numeric prefix).

**Numbered Tool System**: Tools use `XX_tool_name.py` format for clear ordering. This prevents naming conflicts and sorts naturally in file listings.

**CLI Router**: The main `scripts/axle.py` uses argparse with subcommands. The entry point is defined in `pyproject.toml` as `axle = "scripts.axle:main"`.

**Platform Positioning**: Axle is positioned as a platform for running ANY Python tool consistently, not just the built-in SEO/productivity tools. Users can add their own tools by dropping `.py` files in the `tools/` directory.

## Development Workflow

**Installation**:

```bash
pip install -r requirements.txt
pip install -e .
```

**Running commands**:

```bash
axle list              # See available tools
axle run 1 "prompt"    # Run tool #1 with prompt
axle run seo_keyword_checker "prompt"  # Run by name
```

**Adding a new tool**:

1. Create `tools/04_my_tool.py` (numbered for ordering)
2. Implement `get_description()` and `main(prompt)` functions
3. Tool automatically appears in `axle list`
4. No changes to core code required

**Package metadata**: The project uses `pyproject.toml` with setuptools. Package name is `axle`, version `0.1.0`. Entry point: `axle = "scripts.axle:main"`.

## Dependencies

Core requirements (Python 3.10+):

- **Data Processing**: pandas, numpy, openpyxl
- **ML/NLP**: scikit-learn, spacy, sentence-transformers, nltk
- **Web**: beautifulsoup4, requests, lxml
- **Security**: pip-audit

**Heavy Dependencies**: ML/NLP packages require ~5-8GB disk space. Minimum 8GB RAM (16GB preferred).

**spaCy Model**: Installation script downloads `en_core_web_sm` model automatically.

## Key Files

- **scripts/axle.py**: Main CLI router (~376 lines). Implements all 7 commands, dynamic tool loading, error handling, community footer.
- **scripts/install_axle.py**: Interactive installer with system checks, guided setup, spaCy model download.
- **scripts/security_scan.py**: Vulnerability scanner using pip-audit and static analysis.
- **tools/*.py**: Tool implementations following the tool contract.

## Branding & URLs

- **Product Name**: Axle (not Buddy CLI, not Buddy Tools)
- **Command**: axle (not buddy)
- **Repository**: https://github.com/skpaul82/axle-py
- **Documentation**: axle.sanjoypaul.com/agent-aio
- **Email**: hello@skpaul.me

**Rebranding Complete**: All references to "Buddy CLI" have been replaced with "Axle" platform positioning. Historical context preserved in `.docs/` directory.

## Community & Support

All tool outputs include community footer:

- GitHub: https://github.com/skpaul82/axle-py
- X/Twitter: @_skpaul82
- Instagram: @skpaul82
- Newsletter: axle.sanjoypaul.com/agent-aio

## Platform Philosophy

**Key Positioning**: Axle is a platform for tools, not a toolkit. Users can drop any Python script into the `tools/` directory and run it with `axle run <tool_name>`.

**Value Prop**: Run ANY Python tool consistently without remembering individual script locations or interfaces.

**Extensibility**: Zero code changes required to add new tools. Just drop a `.py` file in `tools/` that implements the contract.

## License

MIT License - see LICENSE file.

## Internal Documentation

Planning and historical documentation in `.docs/`:

- **PRD.md**: Product Requirements Document
- **IMPLEMENTATION_PLAN.md**: Implementation phases
- **CONTEXT.md**: Architecture and technical decisions
- **2nd-note.md**: Original platform pivot discussion (historical)
- **2nd-thoughts.md**: Strategic analysis (historical)
- **INTERNAL_DOCS_UPDATE.md**: Rebranding documentation
