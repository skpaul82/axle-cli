# Command Reference

Complete reference for all Axle CLI commands.

## Commands Overview

| Command | Description |
|---------|-------------|
| `axle list` | List all available tools |
| `axle run` | Execute a tool by number or name |
| `axle info` | Show detailed tool information |
| `axle scan` | Run security vulnerability scan |
| `axle doctor` | Run environment diagnostics |
| `axle path` | Show tools folder location |
| `axle help` | Display help message |
| `axle security` | Show or configure security policy |
| `axle uninstall` | Uninstall Axle CLI |

---

## axle list

List all available tools in the tools directory.

### Syntax

```bash
buddy list
```

### Description

Displays all available tools with their numbers, names, and descriptions. Tools are shown in alphabetical order.

### Examples

```bash
$ buddy list

Hey buddy, let me know how I can help you. Choose a tool from the list or enter a number.

  1. daily_life_hack_generator - Generate personalized productivity and life optimization tips
  2. meta_tag_auditor - Analyze HTML/webpage for meta tag completeness and SEO best practices
  3. seo_keyword_checker - Analyze text for SEO keyword density and optimization suggestions

---
🌐 Community & Support
⭐ Star the GitHub repo: https://github.com/skpaul82/axle-cli
...
```

### Notes

- Tool numbers are based on alphabetical order
- Each tool must have a `get_description()` function
- Shows tools from the configured tools directory

---

## axle run

Execute a tool by number or name.

### Syntax

```bash
buddy run <tool_identifier> [prompt]
```

### Arguments

- `tool_identifier` (required): Tool number (from `buddy list`) or tool name (without .py)
- `prompt` (optional): Text input for the tool

### Options

None

### Examples

**By Number:**

```bash
buddy run 1 "python is a great programming language"
```

**By Name:**

```bash
buddy run seo_keyword_checker "python is a great programming language"
```

**Without Prompt:**

```bash
buddy run 3
# Tool will prompt for input or use default behavior
```

**Multi-word Prompt:**

```bash
buddy run 1 "analyze this content for keyword density and SEO optimization"
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid tool number | Number out of range | Run `buddy list` to see valid numbers |
| Tool not found | Tool name doesn't exist | Check spelling or use number |
| Tool failed | Tool execution error | Check tool-specific requirements |

### Notes

- Tools are invoked dynamically using Python's importlib
- Each tool must implement a `main(prompt)` function
- The prompt is passed as a string (may be empty)
- Community footer is displayed after tool execution

---

## buddy info

Show detailed information about a specific tool.

### Syntax

```bash
buddy info <tool_name>
```

### Arguments

- `tool_name` (required): Name of the tool (without .py extension)

### Options

None

### Examples

```bash
$ buddy info seo_keyword_checker

📋 Tool: seo_keyword_checker
📍 Location: /path/to/tools/01_seo_keyword_checker.py
📝 Description: Analyze text for SEO keyword density and optimization suggestions

---
🌐 Community & Support
⭐ Star the GitHub repo: https://github.com/skpaul82/axle-cli
...
```

### What It Shows

- Tool name
- File location (absolute path)
- Tool description (from `get_description()`)
- Tool docstring (if available)

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Tool not found | Tool name doesn't exist | Run `buddy list` to see available tools |

---

## buddy scan

Run security vulnerability scan on dependencies and scripts.

### Syntax

```bash
buddy scan
```

### Description

Scans for security vulnerabilities using pip-audit and basic static analysis of Python scripts.

### What It Checks

1. **Dependencies**: Uses pip-audit to check for known vulnerabilities
2. **Scripts**: Basic static analysis for:
   - Hardcoded passwords/API keys
   - Dangerous function usage (eval, exec)
   - Unsafe imports (pickle, marshal)
   - Shell command injection risks

### Examples

```bash
$ buddy scan

🔒 Buddy Tools Security Scan
============================================================

📦 Dependency Scan
------------------------------------------------------------
✅ No critical vulnerabilities found in dependencies.

🔍 Script Security Scan
------------------------------------------------------------
✅ No obvious security issues found in scripts!

💡 Recommendations
------------------------------------------------------------
LOW Priority:
   • [General] Run security scan regularly: buddy scan
   • [General] Keep dependencies updated regularly
```

### Output Sections

1. **Dependency Scan**: Results from pip-audit
2. **Script Security Scan**: Static analysis findings
3. **Recommendations**: Prioritized action items

### Notes

- Requires pip-audit to be installed
- May produce false positives
- Review all findings before taking action
- Critical issues should be addressed immediately

---

## buddy doctor

Run environment diagnostics to check system setup.

### Syntax

```bash
buddy doctor
```

### Description

Checks your environment to ensure Buddy Tools is properly configured and can run efficiently.

### What It Checks

1. **Python Version**: Verifies 3.10+
2. **Platform**: Operating system and architecture
3. **Disk Space**: At least 5GB free
4. **RAM**: At least 8GB (requires psutil)
5. **Dependencies**: Key Python packages
6. **Tools Directory**: Exists and contains tools
7. **CLI Installation**: buddy command works

### Examples

```bash
$ buddy doctor

🏥 Buddy Tools Environment Check
============================================================

🐍 Python Version: 3.10.12
   ✓ Python version OK

💻 Platform: Darwin arm64

💾 Disk Space:
   Free: 25.3 GB
   ✓ Disk space OK

🧠 RAM: 16.0 GB
   ✓ RAM OK

📦 Key Dependencies:
   ✓ pandas
   ✓ numpy
   ✓ requests
   ✓ bs4
   ✓ nltk
   ✓ sklearn
   ✓ spacy
   ✓ sentence_transformers

🔧 Tools Directory:
   ✓ Found at: /path/to/tools
   ✓ Contains 3 tools

⚙️ CLI Installation:
   ✓ CLI command 'buddy' is working
```

### Notes

- RAM check requires psutil (optional dependency)
- Warnings don't prevent usage but indicate potential issues
- Run after installation to verify setup
- Use when troubleshooting issues

---

## buddy path

Show the current tools folder location.

### Syntax

```bash
buddy path
```

### Description

Displays the absolute path to the tools directory and lists its contents.

### Examples

```bash
$ buddy path

📁 Tools folder path: /absolute/path/to/tools

Contains 3 file(s):
  - 01_seo_keyword_checker.py
  - 02_meta_tag_auditor.py
  - 03_daily_life_hack_generator.py

---
🌐 Community & Support
⭐ Star the GitHub repo: https://github.com/skpaul82/axle-cli
...
```

### Use Cases

- Verify tools directory location
- Check which tools are installed
- Troubleshoot missing tools
- Confirm custom tools directory

---

## buddy help

Display help message and command reference.

### Syntax

```bash
buddy help
```

### Description

Shows comprehensive help information including all available commands and their usage.

### Examples

```bash
$ buddy help

usage: buddy [-h] {list,run,info,scan,doctor,path,help} ...

Buddy Tools: microtools for SEO and daily-life hacks.

options:
  -h, --help  show this help message and exit

commands:
  {list,run,info,scan,doctor,path,help}
    list       List all available tools
    run        Run a tool by number or name
    info       Show tool information
    scan       Scan dependencies for vulnerabilities
    doctor     Run environment diagnostics
    path       Show tools folder location
    help       Show this help message
```

### Notes

- Also available with `-h` or `--help`
- Shows all subcommands
- Displays command syntax and options

---

## Global Options

These options apply to all commands:

### `-h, --help`

Show help message and exit.

```bash
buddy -h
buddy --help
buddy run -h
```

### Version Information

To check the package version:

```bash
pip show buddy-tools
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error occurred |
| 2 | Invalid command or arguments |

---

## Configuration Files

Buddy Tools uses these configuration files:

- `pyproject.toml` - Package metadata and dependencies
- `requirements.txt` - Pinned dependency versions
- `.buddyrc` (optional) - User configuration (not yet implemented)

---

## Environment Variables

These environment variables affect Buddy Tools behavior:

| Variable | Purpose | Default |
|----------|---------|---------|
| `BUDDY_TOOLS_DIR` | Custom tools directory | `tools/` |
| `PYTHONPATH` | Python module search path | (system default) |

---

## See Also

- [Usage Guide](usage.md) - How to use tools effectively
- [Installation Guide](installation.md) - Setup instructions
- [Troubleshooting](troubleshooting.md) - Solve common problems
