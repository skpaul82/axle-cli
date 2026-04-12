# Command Reference

Complete reference for all Axle CLI commands.

## Commands Overview

| Command | Description |
|---------|-------------|
| `axle -V, --version` | Show Axle version |
| `axle list` | List all available tools |
| `axle run` | Execute a tool by number or name |
| `axle run --security` | Execute tool with security validation |
| `axle run --code-review` | Execute tool with code review |
| `axle info` | Show detailed tool information |
| `axle scan` | Run security vulnerability scan |
| `axle doctor` | Run environment diagnostics |
| `axle path` | Show tools folder location |
| `axle help` | Display help message |
| `axle security` | Show or configure security policy |
| `axle security --enable` | Enable security by default |
| `axle security --disable` | Disable security by default |
| `axle security --show` | Show security configuration |
| `axle review` | Run code review on tools |
| `axle review --enable` | Enable code review by default |
| `axle review --disable` | Disable code review by default |
| `axle review --show` | Show code review configuration |
| `axle update` | Update Axle CLI to latest version |
| `axle update --check` | Check for updates without installing |
| `axle metadata scan` | Scan tools and build metadata cache |
| `axle metadata list` | List all tools with summaries |
| `axle metadata show` | Show detailed tool metadata |
| `axle metadata search` | Search tools by name/function/description |
| `axle uninstall` | Uninstall Axle CLI |

---

## axle list

List all available tools in the tools directory.

### Syntax

```bash
axle list
```

### Description

Displays all available tools with their numbers, names, and descriptions. Tools are shown in alphabetical order.

### Examples

```bash
$ axle list

Hey axle, let me know how I can help you. Choose a tool from the list or enter a number.

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

Execute a tool by number or name. Optionally enable security validation or code review for this execution.

### Syntax

```bash
axle run <tool_identifier> [prompt] [--security] [--code-review]
```

### Arguments

- `tool_identifier` (required): Tool number (from `axle list`) or tool name (without .py)
- `prompt` (optional): Text input for the tool

### Options

- `--security`: Enable security validation for this run (disabled by default)
- `--code-review`: Enable code review for this run (disabled by default)

### Examples

**By Number:**

```bash
axle run 1 "python is a great programming language"
```

**By Name:**

```bash
axle run seo_keyword_checker "python is a great programming language"
```

**With Security Validation:**

```bash
axle run 1 "test" --security
```

**With Code Review:**

```bash
axle run 1 "test" --code-review
```

**With Both:**

```bash
axle run 1 "test" --security --code-review
```

**Without Prompt:**

```bash
axle run 3
# Tool will prompt for input or use default behavior
```

### Notes

- Security and code review are **disabled by default** in v1.2.0
- Use `--security` flag to enable security validation for one execution
- Use `--code-review` flag to enable code review for one execution
- For persistent enablement, use `axle security --enable` or `axle review --enable`
- Configuration stored in `~/.axle/config.json`

**Multi-word Prompt:**

```bash
axle run 1 "analyze this content for keyword density and SEO optimization"
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid tool number | Number out of range | Run `axle list` to see valid numbers |
| Tool not found | Tool name doesn't exist | Check spelling or use number |
| Tool failed | Tool execution error | Check tool-specific requirements |

### Notes

- Tools are invoked dynamically using Python's importlib
- Each tool must implement a `main(prompt)` function
- The prompt is passed as a string (may be empty)
- Community footer is displayed after tool execution

---

## axle info

Show detailed information about a specific tool.

### Syntax

```bash
axle info <tool_name>
```

### Arguments

- `tool_name` (required): Name of the tool (without .py extension)

### Options

None

### Examples

```bash
$ axle info seo_keyword_checker

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
| Tool not found | Tool name doesn't exist | Run `axle list` to see available tools |

---

## axle scan

Run security vulnerability scan on dependencies and scripts.

### Syntax

```bash
axle scan
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
$ axle scan

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
   • [General] Run security scan regularly: axle scan
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

## axle doctor

Run environment diagnostics to check system setup.

### Syntax

```bash
axle doctor
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
7. **CLI Installation**: axle command works

### Examples

```bash
$ axle doctor

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
   ✓ CLI command 'axle' is working
```

### Notes

- RAM check requires psutil (optional dependency)
- Warnings don't prevent usage but indicate potential issues
- Run after installation to verify setup
- Use when troubleshooting issues

---

## axle path

Show the current tools folder location.

### Syntax

```bash
axle path
```

### Description

Displays the absolute path to the tools directory and lists its contents.

### Examples

```bash
$ axle path

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

## axle help

Display help message and command reference.

### Syntax

```bash
axle help
```

### Description

Shows comprehensive help information including all available commands and their usage.

### Examples

```bash
$ axle help

usage: axle [-h] {list,run,info,scan,doctor,path,help} ...

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
axle -h
axle --help
axle run -h
```

### `-V, --version`

Show version information and exit.

```bash
axle -V
axle --version
```

This displays the current version of Axle installed on your system.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error occurred |
| 2 | Invalid command or arguments |

---

## Configuration Files

Axle uses these configuration files:

- `pyproject.toml` - Package metadata and dependencies
- `requirements.txt` - Pinned dependency versions
- `.axlerc` (optional) - User configuration (not yet implemented)

---

## Environment Variables

These environment variables affect Axle behavior:

| Variable | Purpose | Default |
|----------|---------|---------|
| `AXLE_TOOLS_DIR` | Custom tools directory | `tools/` |
| `AXLE_SECURITY_POLICY` | Security policy (strict/warn/permissive) | `warn` |
| `PYTHONPATH` | Python module search path | (system default) |

---

## See Also

- [Usage Guide](usage.md) - How to use tools effectively
- [Installation Guide](installation.md) - Setup instructions
- [Troubleshooting](troubleshooting.md) - Solve common problems
