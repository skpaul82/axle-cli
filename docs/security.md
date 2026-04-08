# 🔒 Security Features

**Axle** includes **mandatory built-in security validation** for all tools. Every tool is automatically scanned for security issues **before execution**.

---

## Overview

Axle's security system protects you from:
- **Malicious code execution** (eval, exec, arbitrary code)
- **Hardcoded secrets** (passwords, API keys, tokens)
- **Unsafe imports** (pickle, marshal)
- **Dangerous subprocess calls** (shell=True)
- **Command injection** vulnerabilities

**This is a MANDATORY feature** - all tools are validated by default before execution.

---

## How It Works

### 1. Automatic Pre-Execution Validation

Every time you run a tool with `axle run`, it undergoes security validation:

```bash
$ axle run 1 "test prompt"

🔒 Validating tool security...
   Security Policy: WARN
   ✅ Security validation passed

🔧 Running 01_seo_keyword_checker.py...
```

### 2. Security Checks Performed

| Check | Description | Severity |
|-------|-------------|----------|
| **eval() detection** | Blocks arbitrary code execution | CRITICAL |
| **exec() detection** | Blocks arbitrary code execution | CRITICAL |
| **Dynamic imports** | Flags `__import__()` with strings | CRITICAL |
| **os.system()** | Detects arbitrary shell commands | HIGH |
| **subprocess with shell=True** | Detects command injection risk | HIGH |
| **pickle/marshal** | Flags unsafe deserialization | HIGH |
| **Hardcoded passwords** | Detects `password="..."` patterns | CRITICAL |
| **Hardcoded API keys** | Detects `api_key="..."` patterns | CRITICAL |
| **Hardcoded tokens** | Detects `token="..."` patterns | CRITICAL |
| **Hardcoded secrets** | Detects `secret="..."` patterns | CRITICAL |
| **Private keys** | Detects `private_key="..."` patterns | CRITICAL |
| **Debug prints** | Flags `print()` statements | LOW |

### 3. Real-Time Protection

- **Instant validation**: Tools are validated in milliseconds
- **No configuration needed**: Works out of the box
- **Automatic blocking**: Dangerous tools are blocked by default
- **Clear feedback**: Shows exactly what security issues were found

---

## Security Policies

Axle provides three security policies to balance security and usability:

### WARN (Default - Recommended)

**Blocks**: Critical severity findings
**Warns**: High, Medium, Low findings
**Best for**: Development environments

```bash
export AXLE_SECURITY_POLICY=warn
```

Example:
```
🔒 Validating tool security...
   Security Policy: WARN

⚠️  Tool has 2 security warning(s) but will run.
   Policy: WARN
   ✅ Tool execution allowed
```

### STRICT (High Security)

**Blocks**: ALL security findings (Critical, High, Medium, Low)
**Best for**: Production environments, untrusted tools

```bash
export AXLE_SECURITY_POLICY=strict
```

Example:
```
🔒 Validating tool security...
   Security Policy: STRICT

LOW Severity:
   🟢 LOW:27 [Dangerous Pattern] Debug print statements found

❌ Tool BLOCKED due to 1 security finding(s).
   Policy: STRICT
```

### PERMISSIVE (Relaxed)

**Blocks**: Only Critical and High severity findings
**Best for**: Trusted tools, local development

```bash
export AXLE_SECURITY_POLICY=permissive
```

---

## Configuration

### Setting Security Policy

**Method 1: Environment Variable (Recommended)**
```bash
# Set in your ~/.bashrc or ~/.zshrc
export AXLE_SECURITY_POLICY=strict

# Or temporary
AXLE_SECURITY_POLICY=warn axle run 1 "prompt"
```

**Method 2: Command Option**
```bash
# Check current policy
axle security

# Set policy for session
axle security --policy strict
```

### Viewing Current Policy

```bash
$ axle security

🔒 Axle Security Configuration
============================================================

Current Policy: WARN

Policy Details:

  ✓ WARN
     Block only on CRITICAL findings, warn on others
     Blocks: Critical severity
     Best for: Development environments (default)

  STRICT
     Block execution on ANY security finding
     Blocks: All severity levels (Critical, High, Medium, Low)
     Best for: Production environments, untrusted tools

  PERMISSIVE
     Block only on CRITICAL/HIGH findings
     Blocks: Critical, High severity
     Best for: Trusted tools, local development
```

---

## Security Scan Command

In addition to automatic validation, you can manually scan tools:

```bash
# Scan all dependencies and tools
axle scan

# Output includes:
# - Dependency vulnerabilities (pip-audit)
# - Tool security issues
# - Recommendations
```

---

## Examples

### Example 1: Safe Tool Execution

```bash
$ axle run 3 "productivity tips"

🔒 Validating tool security...
   Security Policy: WARN
   ✅ Security validation passed

🔧 Running 03_daily_life_hack_generator.py...
```

### Example 2: Tool with Warnings

```bash
$ axle run custom_tool

🔒 Validating tool security...
   Security Policy: WARN

MEDIUM Severity:
   🟡 MEDIUM:42 [Dangerous Pattern] compile() with strings may be unsafe

------------------------------------------------------------
⚠️  Tool has 1 security warning(s) but will run.
   Policy: WARN

🔧 Running custom_tool...
```

### Example 3: Blocked Tool

```bash
$ axle run suspicious_tool

🔒 Validating tool security...
   Security Policy: WARN

CRITICAL Severity:
   🔴 CRITICAL:15 [Hardcoded Secret] Hardcoded API key detected

------------------------------------------------------------
❌ Tool BLOCKED due to 1 security finding(s).
   Policy: WARN

   To override: AXLE_SECURITY_POLICY=permissive axle run suspicious_tool
```

---

## Best Practices

### 1. Development Environments
```bash
export AXLE_SECURITY_POLICY=warn
```
- Blocks dangerous code
- Warns about issues
- Good balance of security and usability

### 2. Production Environments
```bash
export AXLE_SECURITY_POLICY=strict
```
- Maximum security
- Blocks ALL findings
- Suitable for untrusted tools

### 3. Trusted Tools
```bash
export AXLE_SECURITY_POLICY=permissive
```
- Only blocks critical/high severity
- Use only for tools you trust
- Not recommended for untrusted code

### 4. Regular Security Scans
```bash
# Run weekly
axle scan
```

---

## Security vs Usability

| Policy | Security | Usability | Speed | Use Case |
|--------|----------|------------|-------|----------|
| **STRICT** | ⭐⭐⭐⭐⭐ | ⭐⭐ | Fast | Production, untrusted tools |
| **WARN** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Fast | Development (default) |
| **PERMISSIVE** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Fast | Trusted tools only |

---

## Troubleshooting

### Tool Blocked but You Trust It

**Option 1**: Use permissive policy
```bash
AXLE_SECURITY_POLICY=permissive axle run tool_name
```

**Option 2**: Fix the security issues
- Remove hardcoded secrets (use environment variables)
- Avoid eval(), exec(), shell=True
- Use safer alternatives

### Too Many False Positives

If you're getting too many warnings for trusted code:

1. **Use PERMISSIVE policy** for development
2. **Review the findings** to understand the risks
3. **Fix critical issues** in the tool code

### Validation Taking Too Long

Security validation is designed to be fast (< 100ms typically). If it's slow:

1. Check if the tool file is extremely large (> 1000 lines)
2. Consider splitting the tool into smaller modules
3. Report performance issues to the Axle team

---

## FAQ

**Q: Can I disable security validation?**

A: No, security validation is mandatory for all tools. However, you can use the PERMISSIVE policy to minimize blocking.

**Q: What happens if a tool is blocked?**

A: The tool will not execute. You'll see a message explaining why and how to override if needed.

**Q: Are my tools validated every time?**

A: Yes, every tool is validated before every execution. This ensures real-time protection.

**Q: Can I add custom security rules?**

A: Currently, security rules are built-in. Custom rules may be added in future versions.

**Q: Does validation slow down tool execution?**

A: No, validation is very fast (typically < 100ms) and has negligible impact on performance.

---

## Summary

✅ **Mandatory**: All tools validated before execution
✅ **Automatic**: No configuration needed
✅ **Configurable**: Three security policies (warn/strict/permissive)
✅ **Real-time**: Instant validation and feedback
✅ **Comprehensive**: 10+ security checks performed
✅ **Safe**: Blocks dangerous code by default

**Security is not optional in Axle - it's built-in.**
