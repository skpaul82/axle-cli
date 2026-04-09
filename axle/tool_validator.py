#!/usr/bin/env python3
"""Tool security validation module for Axle.

This module provides security validation for tools before execution.
It scans for dangerous patterns, hardcoded secrets, and unsafe imports.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

# Security severity levels
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"

# Security policies
POLICY_STRICT = "strict"  # Block execution on any finding
POLICY_WARN = "warn"  # Warn but allow execution
POLICY_PERMISSIVE = "permissive"  # Only warn on critical/high


class SecurityFinding:
    """Represents a security finding."""

    def __init__(self, severity: str, category: str, message: str, line_no: int = None):
        self.severity = severity
        self.category = category
        self.message = message
        self.line_no = line_no

    def __str__(self):
        line_info = f":{self.line_no}" if self.line_no else ""
        emoji = {
            SEVERITY_CRITICAL: "🔴",
            SEVERITY_HIGH: "🟠",
            SEVERITY_MEDIUM: "🟡",
            SEVERITY_LOW: "🟢",
        }.get(self.severity, "⚪")

        return f"{emoji} {self.severity}{line_info} [{self.category}] {self.message}"


class ToolValidator:
    """Validates tool security before execution."""

    # Dangerous patterns to check for
    DANGEROUS_PATTERNS = {
        SEVERITY_CRITICAL: {
            r"eval\s*\(": "eval() can execute arbitrary code",
            r"exec\s*\(": "exec() can execute arbitrary code",
            r'__import__\s*\(\s*["\']': "Dynamic import can execute arbitrary code",
        },
        SEVERITY_HIGH: {
            r"os\.system\s*\(": "os.system() can execute arbitrary shell commands",
            r"subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True": "subprocess with shell=True is dangerous",
            r"pickle\.load": "pickle can execute arbitrary code when loading untrusted data",
            r"marshal\.load": "marshal module can execute arbitrary code",
        },
        SEVERITY_MEDIUM: {
            r"compile\s*\(": "compile() with strings may be unsafe",
            r"shelve\.open": "shelve can be unsafe with untrusted data",
            r'input\s*\(\s*["\']password': "Password input may be logged",
        },
        SEVERITY_LOW: {
            r"print\s*\(": "Debug print statements found",
            r"pprint": "Pretty print statements found",
        },
    }

    # Secret patterns
    SECRET_PATTERNS = {
        SEVERITY_CRITICAL: {
            r'password\s*=\s*["\'][^"\']{8,}["\']': "Hardcoded password detected",
            r'api[_-]?key\s*=\s*["\'][^"\']{20,}["\']': "Hardcoded API key detected",
            r'secret[_-]?key\s*=\s*["\'][^"\']{20,}["\']': "Hardcoded secret key detected",
            r'token\s*=\s*["\'][^"\']{20,}["\']': "Hardcoded token detected",
            r'private[_-]?key\s*=\s*["\']': "Hardcoded private key detected",
        }
    }

    # Unsafe imports
    UNSAFE_IMPORTS = {
        SEVERITY_HIGH: {
            "pickle": "pickle module is unsafe with untrusted data",
            "marshal": "marshal module is unsafe",
        }
    }

    def __init__(self, policy: str = POLICY_WARN):
        """Initialize validator with security policy.

        Args:
            policy: Security policy (strict/warn/permissive)
        """
        self.policy = policy

    def validate_tool(self, tool_path: Path) -> Tuple[bool, List[SecurityFinding]]:
        """Validate a tool file for security issues.

        Args:
            tool_path: Path to the tool file

        Returns:
            Tuple of (is_safe, findings)
        """
        try:
            content = tool_path.read_text()
        except Exception as e:
            return False, [
                SecurityFinding(
                    SEVERITY_HIGH, "File Access", f"Cannot read tool file: {e}"
                )
            ]

        findings = []

        # Check for dangerous patterns
        findings.extend(self._check_dangerous_patterns(content, tool_path))

        # Check for hardcoded secrets
        findings.extend(self._check_secrets(content, tool_path))

        # Check for unsafe imports
        findings.extend(self._check_unsafe_imports(content, tool_path))

        # Determine if tool is safe based on policy
        is_safe = self._is_safe(findings)

        return is_safe, findings

    def _check_dangerous_patterns(
        self, content: str, tool_path: Path
    ) -> List[SecurityFinding]:
        """Check for dangerous code patterns."""
        findings = []

        lines = content.split("\n")

        for severity, patterns in self.DANGEROUS_PATTERNS.items():
            # Skip low severity checks in permissive mode
            if self.policy == POLICY_PERMISSIVE and severity == SEVERITY_LOW:
                continue

            for pattern, message in patterns.items():
                matches = list(re.finditer(pattern, content))
                for match in matches:
                    # Find line number
                    line_no = content[: match.start()].count("\n") + 1

                    # Skip if in comment
                    line = lines[line_no - 1] if line_no <= len(lines) else ""
                    if line.lstrip().startswith("#"):
                        continue
                    hash_pos = line.find("#")
                    if hash_pos != -1:
                        line_start = content.rfind("\n", 0, match.start()) + 1
                        match_col = match.start() - line_start
                        if hash_pos < match_col:
                            continue

                    findings.append(
                        SecurityFinding(severity, "Dangerous Pattern", message, line_no)
                    )

        return findings

    def _check_secrets(self, content: str, tool_path: Path) -> List[SecurityFinding]:
        """Check for hardcoded secrets."""
        findings = []
        lines = content.split("\n")

        for severity, patterns in self.SECRET_PATTERNS.items():
            for pattern, message in patterns.items():
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                for match in matches:
                    line_no = content[: match.start()].count("\n") + 1

                    # Skip if in comment or docstring
                    line = lines[line_no - 1] if line_no <= len(lines) else ""
                    stripped = line.strip()
                    if (
                        stripped.startswith("#")
                        or stripped.startswith('"""')
                        or stripped.startswith("'''")
                    ):
                        continue

                    findings.append(
                        SecurityFinding(severity, "Hardcoded Secret", message, line_no)
                    )

        return findings

    def _check_unsafe_imports(
        self, content: str, tool_path: Path
    ) -> List[SecurityFinding]:
        """Check for unsafe module imports."""
        findings = []

        for severity, modules in self.UNSAFE_IMPORTS.items():
            # Skip high severity in permissive mode
            if self.policy == POLICY_PERMISSIVE and severity == SEVERITY_HIGH:
                continue

            for module, message in modules.items():
                pattern = rf"(?:^import\s+{re.escape(module)}\b|^from\s+{re.escape(module)}\s+import)"
                for imp_match in re.finditer(pattern, content, re.MULTILINE):
                    line_no = content[: imp_match.start()].count("\n") + 1
                    findings.append(
                        SecurityFinding(severity, "Unsafe Import", message, line_no)
                    )

        return findings

    def _is_safe(self, findings: List[SecurityFinding]) -> bool:
        """Determine if tool is safe based on policy and findings."""
        if not findings:
            return True

        if self.policy == POLICY_STRICT:
            # Block on any finding
            return False

        elif self.policy == POLICY_WARN:
            # Only block on critical findings
            critical_findings = [f for f in findings if f.severity == SEVERITY_CRITICAL]
            return len(critical_findings) == 0

        elif self.policy == POLICY_PERMISSIVE:
            # Only block on critical/high findings
            blocking_findings = [
                f for f in findings if f.severity in [SEVERITY_CRITICAL, SEVERITY_HIGH]
            ]
            return len(blocking_findings) == 0

        return True

    def display_findings(self, findings: List[SecurityFinding]):
        """Display security findings."""
        if not findings:
            print("✅ No security issues found")
            return

        # Group by severity
        by_severity = {
            SEVERITY_CRITICAL: [],
            SEVERITY_HIGH: [],
            SEVERITY_MEDIUM: [],
            SEVERITY_LOW: [],
        }

        for finding in findings:
            by_severity[finding.severity].append(finding)

        # Display by severity
        for severity in [
            SEVERITY_CRITICAL,
            SEVERITY_HIGH,
            SEVERITY_MEDIUM,
            SEVERITY_LOW,
        ]:
            if by_severity[severity]:
                print(f"\n{severity} Severity:")
                for finding in by_severity[severity]:
                    print(f"   {finding}")


def get_security_policy() -> str:
    """Get security policy from environment or config."""
    import os

    policy = os.getenv("AXLE_SECURITY_POLICY", "warn").lower()

    if policy not in [POLICY_STRICT, POLICY_WARN, POLICY_PERMISSIVE]:
        policy = POLICY_WARN

    return policy


def validate_tool_before_execution(tool_path: Path, policy: str = None) -> bool:
    """Validate tool before execution (main entry point).

    Args:
        tool_path: Path to tool file
        policy: Security policy (defaults to env var or 'warn')

    Returns:
        True if tool is safe to execute, False otherwise
    """
    if policy is None:
        policy = get_security_policy()

    validator = ToolValidator(policy=policy)
    is_safe, findings = validator.validate_tool(tool_path)

    if findings:
        print(f"\n🔒 Security Validation: {tool_path.name}")
        print("-" * 60)

        validator.display_findings(findings)

        print("\n" + "-" * 60)

        if is_safe:
            print(f"⚠️  Tool has {len(findings)} security warning(s) but will run.")
            print(f"   Policy: {policy.upper()}")
            return True
        else:
            print(f"❌ Tool BLOCKED due to {len(findings)} security finding(s).")
            print(f"   Policy: {policy.upper()}")
            print(f"\n   To override, set AXLE_SECURITY_POLICY=permissive")
            return False
    else:
        return True
