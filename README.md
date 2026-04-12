# Axle v1.2.0

A modular CLI platform for running Python microtools from a shared tools directory.

---

## 🚀 Quick install

### Method 1: Install from GitHub (Recommended)

```bash
pip install git+https://github.com/skpaul82/axle-cli.git
```

That's it! You can now run:

```bash
axle list
axle run 1 "your prompt"
axle scan
```

### Method 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/skpaul82/axle-cli.git
cd axle-cli

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install the package
pip install -e .
```

> **Note**: PyPI installation (`pip install axle-cli`) is planned for future releases. For v1.2.0, please use the GitHub installation method above.

---

## 🎉 What's New in v1.2.0

### ✨ Optional Security & Code Review
- **Security and code review are now DISABLED by default** for faster execution
- Use `--security` and `--code-review` flags to enable per-run
- Use `axle security enable` and `axle review enable` to enable persistently
- Configuration stored in `~/.axle/config.json`

### 🔄 Built-in Update Command
- **`axle update`** - Update Axle CLI to the latest version
- **`axle update --check`** - Check for updates without installing
- Automatic dependency updates and package reinstallation

### 📊 Tool Metadata System
- **`axle metadata scan`** - Scan all tools and build metadata cache
- **`axle metadata show <tool>`** - Show detailed tool information
- **`axle metadata search <query>`** - Search tools by name, functions, or description
- **`axle metadata list`** - List all tools with summaries
- View tool functions, parameters, documentation, and imports

### 📚 Improved Documentation
- Updated command reference with all new commands
- Better inline help and error messages
- Enhanced user experience

---

## 📦 Features

### 🔒 Built-in Security (Optional)

- **Pre-execution validation**: Tools can be scanned for security issues before running (optional)
- **Dangerous pattern detection**: Blocks eval(), exec(), shell=True, and more
- **Hardcoded secret detection**: Finds passwords, API keys, tokens in code
- **Configurable security policies**: strict, warn, permissive modes
- **On-demand validation**: Enable per-run with `--security` flag or persistently with `axle security enable`
- **Dependency vulnerability scanning**: Integrated pip-audit for package security

### 🔍 Automatic Code Review (Optional)

- **Pre-execution code quality checks**: Automatic review before running tools (optional)
- **Auto-fixing**: Fixes formatting (Black) and import sorting (isort) issues
- **Clear feedback**: Shows exactly what's wrong and how to fix it
- **Non-blocking**: Won't stop your workflow by default
- **Manual review**: Run `axle review` anytime for comprehensive checks
- **CI/CD integration**: Catch issues locally before they reach CI
- **On-demand review**: Enable per-run with `--code-review` flag or persistently with `axle review enable`

### Core Features

- Modular platform for running ANY Python tool consistently
- SEO-focused microtools (keyword checker, meta-tag auditor, etc.)
- Daily-life automation helpers from the terminal
- `axle list` shows all tools with numbers
- `axle run <tool_number_or_name> <prompt>` executes a tool
- Configurable tools folder path

---

## 🛠️ Commands

| Command                    | Purpose                                      |
| -------------------------- | -------------------------------------------- |
| `axle -V, --version`   | Show Axle version.                           |
| `axle list`            | List all tools in the `tools/` directory.  |
| `axle run 1 "prompt"`   | Run tool by number and pass a prompt.        |
| `axle run tool_name ...`| Run by filename (without `.py`).           |
| `axle run 1 "prompt" --security` | Run tool with security validation enabled. |
| `axle run 1 "prompt" --code-review` | Run tool with code review enabled. |
| `axle info tool_name`   | Show tool description.                       |
| `axle scan`             | Scan dependencies for known vulnerabilities. |
| `axle doctor`           | Check Python, disk, and required modules.    |
| `axle path`             | Show current tools folder location.          |
| `axle review <tool>`    | Run code review on a specific tool.          |
| `axle review --all`     | Run code review on all tools.                |
| `axle review --fix`     | Apply automatic fixes to issues found.       |
| `axle review --enable`  | Enable code review by default.               |
| `axle review --disable` | Disable code review by default.              |
| `axle review --show`    | Show current code review configuration.      |
| `axle security`         | Show or configure security policy.           |
| `axle security --enable` | Enable security validation by default.      |
| `axle security --disable` | Disable security validation by default.     |
| `axle security --show`  | Show current security configuration.         |
| `axle update`           | Update Axle CLI to the latest version.       |
| `axle update --check`   | Check for updates without installing.        |
| `axle metadata scan`    | Scan tools and build metadata cache.          |
| `axle metadata show <tool>` | Show detailed metadata for a tool.       |
| `axle metadata search <query>` | Search tools by name, functions, etc.  |
| `axle metadata list`    | List all tools with summaries.               |
| `axle help`             | Show all commands.                           |

---

## 🧱 Requirements

- Python 3.10+
- RAM: 8 GB minimum, 16 GB preferred
- Disk: 5–8 GB free for models and caches
- CPU: 2 cores minimum, 4 cores preferred

Install via `pip install -r requirements.txt` and `pip install -e .`

---

## 📝 Docs

See:

- `docs/index.md` – overview
- `docs/security.md` – **security validation (MANDATORY)**
- `docs/installation.md` – step-by-step setup
- `docs/usage.md` – how to use tools
- `docs/commands.md` – detailed command reference

---

## 🔧 Adding Your Own Tools

Axle is designed as a platform for tools - you can easily add your own Python scripts!

### Tools Directory

Run `axle path` to see your tools directory location. By default, it's created at:

```
<axle_install_location>/tools/
```

### How to Add Tools

1. **Find your tools directory**:

   ```bash
   axle path
   ```
2. **Create a new Python file** in the tools directory:

   ```bash
   # Example: tools/04_my_tool.py
   ```
3. **Implement the required functions**:

   ```python
   def get_description() -> str:
       """Return one-line description of the tool."""
       return "Brief description of what your tool does"

   def main(prompt: str) -> None:
       """Main entry point. Called by CLI router."""
       # Your tool logic here
       print(f"Processing: {prompt}")
   ```
4. **Run your tool**:

   ```bash
   axle list              # Your tool appears in the list
   axle run 4 "your prompt"  # Run by number
   axle run my_tool "your prompt"  # Run by name
   ```

### Tool Requirements

- ✅ Must implement `get_description()` function (returns string)
- ✅ Must implement `main(prompt: str)` function (no return value)
- ✅ File must be valid Python 3.10+
- ✅ Optional: Use numeric prefix for ordering (e.g., `04_my_tool.py`)

**Learn more**: [www.axle.sanjoypaul.com](https://www.axle.sanjoypaul.com)

---

## 🌐 Community & Support

If this helps your workflow:

- ⭐ **Star on GitHub**: [skpaul82/axle-cli](https://github.com/skpaul82/axle-cli)
- 🐦 **Follow on X**: [@_skpaul82](https://x.com/_skpaul82)
- 🌐 **Website**: [www.axle.sanjoypaul.com](https://www.axle.sanjoypaul.com)
- 🌐 ***FB Group***: [Agentic AIO](https://www.facebook.com/groups/agenticaio/)
- 🌐 ***More Tools and Documentation***: Visit [Agentic AIO](#) website.

---

## 📄 License

MIT License – see `LICENSE` for details.

---

## 🤝 Contributing

Contributions are welcome! Please see `docs/contributing.md` for guidelines.

---

## 📚 Troubleshooting

Having issues? Check `docs/troubleshooting.md` for common problems and solutions.

---

♥ Built for the community.
♥ Shared with love for creators, builders, and learners.
