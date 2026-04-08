# Axle Documentation

Welcome to the Axle documentation! This is your comprehensive guide to using and getting the most out of Axle.

## What is Axle?

Axle is a modular CLI platform for running Python microtools from a shared tools directory. It provides built-in security validation, automatic tool discovery, and a simple command structure for consistent tool execution.

## Quick Links

- [Installation Guide](installation.md) - Get Axle up and running
- [Security Guide](security.md) - **MANDATORY**: Learn about built-in security validation
- [Usage Guide](usage.md) - Learn how to use the tools effectively
- [Command Reference](commands.md) - Complete command documentation
- [Troubleshooting](troubleshooting.md) - Solve common problems
- [Contributing](contributing.md) - Contribute to the project

## Features

### 🔒 Built-in Security (MANDATORY)
- **Pre-execution validation**: All tools scanned for security issues before running
- **Dangerous pattern detection**: Blocks eval(), exec(), shell=True, and more
- **Hardcoded secret detection**: Finds passwords, API keys, tokens in code
- **Configurable policies**: strict, warn (default), permissive modes
- **Real-time protection**: Automatic validation on every tool execution

### Core Features
- **Modular Platform**: Drop any Python script in tools/, run with `axle run <tool>`
- **SEO Tools**: Analyze keywords, audit meta tags, optimize content
- **Productivity Hacks**: Get personalized tips for daily life improvement
- **Dependency Scanning**: Integrated pip-audit for package security
- **Easy CLI**: Simple command structure with numbered tools
- **Extensible**: Add your own tools without modifying core code

## Getting Started

### 1. Install

```bash
pip install -r requirements.txt
pip install -e .
```

### 2. Check Security Policy

```bash
axle security
```

### 3. List Tools

```bash
axle list
```

### 4. Run a Tool

```bash
axle run 1 "your text here"
```

## System Requirements

- Python 3.10 or higher
- 8GB RAM minimum (16GB recommended)
- 5-8GB free disk space
- macOS, Linux, or Windows

## Support & Community

- **GitHub**: https://github.com/skpaul82/axle-cli
- **X/Twitter**: [@_skpaul82](https://x.com/_skpaul82)
- **Instagram**: [skpaul82](https://instagram.com/skpaul82)
- **Newsletter**: [axle.sanjoypaul.com/agent-aio](https://axle.sanjoypaul.com/agent-aio)

## License

MIT License - see [LICENSE](../LICENSE) for details.
