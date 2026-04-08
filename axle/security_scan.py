#!/usr/bin/env python3
"""Security and vulnerability scan helper."""

import json
import re
import subprocess
import sys
from pathlib import Path


TOOLS_DIR = "tools"

COMMUNITY_FOOTER = """
---
🌐 Community & Support
⭐ Star the GitHub repo: https://github.com/skpaul82/axle-cli
🐦 Follow on X: @_skpaul82
📸 Instagram: skpaul82
📧 Newsletter: axle.sanjoypaul.com/agent-aio

♥ Built for the community
"""


def scan_dependencies():
    """Scan dependencies for vulnerabilities using pip-audit."""
    print("\n📦 Dependency Scan")
    print("-" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip_audit", "--format", "json"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ No vulnerabilities found in dependencies!\n")
            return []
        else:
            # Try to parse JSON output
            try:
                vulns = json.loads(result.stdout)
                return vulns
            except json.JSONDecodeError:
                # Fallback to text output
                print(result.stdout)
                return []

    except FileNotFoundError:
        print("⚠️ pip-audit not found.")
        print("   Install with: pip install pip-audit")
        print("   Or run: pip install -r requirements.txt\n")
        return []
    except Exception as e:
        print(f"⚠️ Error running pip-audit: {e}\n")
        return []


def parse_vulnerabilities(vulns):
    """Parse and categorize vulnerabilities."""
    if not vulns:
        return []

    parsed = []

    for vuln in vulns:
        name = vuln.get("name", "Unknown")
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for vuln_info in vuln.get("vulnerabilities", []):
            severity = vuln_info.get("severity", "unknown").lower()
            if severity in severity_counts:
                severity_counts[severity] += 1

        # Determine overall severity
        if severity_counts["critical"] > 0:
            overall = "CRITICAL"
        elif severity_counts["high"] > 0:
            overall = "HIGH"
        elif severity_counts["medium"] > 0:
            overall = "MEDIUM"
        elif severity_counts["low"] > 0:
            overall = "LOW"
        else:
            overall = "UNKNOWN"

        # Get affected version and fix version if available
        vuln_ids = [v.get("id", "") for v in vuln.get("vulnerabilities", [])]
        vuln_ids = [vid for vid in vuln_ids if vid]

        parsed.append(
            {
                "name": name,
                "severity": overall,
                "counts": severity_counts,
                "vuln_ids": vuln_ids,
            }
        )

    return parsed


def display_vulnerabilities(parsed_vulns):
    """Display vulnerability findings."""
    if not parsed_vulns:
        return

    print("⚠️ Vulnerabilities Found:\n")

    # Group by severity
    by_severity = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": [], "UNKNOWN": []}

    for vuln in parsed_vulns:
        severity = vuln["severity"]
        by_severity[severity].append(vuln)

    # Display by severity level
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]:
        if by_severity[severity]:
            emoji = {
                "CRITICAL": "🔴",
                "HIGH": "🟠",
                "MEDIUM": "🟡",
                "LOW": "🟢",
                "UNKNOWN": "⚪",
            }.get(severity, "⚪")

            print(f"{emoji} {severity}:")

            for vuln in by_severity[severity]:
                print(f"   • {vuln['name']}")

                # Show counts
                counts = vuln["counts"]
                count_strs = [
                    f"{s}: {counts[s]}"
                    for s in ["critical", "high", "medium", "low"]
                    if counts[s] > 0
                ]
                if count_strs:
                    print(f"     {', '.join(count_strs)}")

                # Show CVE IDs
                if vuln["vuln_ids"]:
                    print(f"     IDs: {', '.join(vuln['vuln_ids'][:3])}")

            print()


def scan_scripts():
    """Scan Python scripts for security issues."""
    print("\n🔍 Script Security Scan")
    print("-" * 60)

    tools_path = Path(TOOLS_DIR)
    if not tools_path.exists():
        print(f"⚠️ Tools directory '{TOOLS_DIR}' not found.\n")
        return []

    issues = []

    for py_file in tools_path.glob("*.py"):
        if py_file.name == "__init__.py":
            continue

        try:
            content = py_file.read_text()
            file_issues = []

            # Check for dangerous functions
            dangerous_patterns = {
                "eval(": "Use of eval() can execute arbitrary code",
                "exec(": "Use of exec() can execute arbitrary code",
                "compile(": "Use of compile() with strings may be unsafe",
                "__import__(": "Dynamic imports may be unsafe",
                "os.system": "os.system() can execute arbitrary commands",
                "subprocess.call": "subprocess.call() with shell=True may be unsafe",
                "subprocess.run": "subprocess.run() with shell=True may be unsafe",
            }

            for pattern, message in dangerous_patterns.items():
                if pattern in content:
                    # Check if shell=True is used for subprocess
                    if "subprocess" in pattern and "shell=True" in content:
                        file_issues.append(f"⚠️ {pattern} with shell=True")

                    file_issues.append(f"⚠️ {message}")

            # Check for potential hardcoded secrets
            secret_patterns = {
                r'password\s*=\s*["\'][^"\']+["\']': "Possible hardcoded password",
                r'api[_-]?key\s*=\s*["\'][^"\']+["\']': "Possible hardcoded API key",
                r'secret\s*=\s*["\'][^"\']+["\']': "Possible hardcoded secret",
                r'token\s*=\s*["\'][^"\']+["\']': "Possible hardcoded token",
            }

            for pattern, message in secret_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    file_issues.append(f"🔴 {message}")

            # Check for imports that may be unsafe
            unsafe_imports = {
                "pickle": "pickle module can be unsafe with untrusted data",
                "shelve": "shelve module can be unsafe with untrusted data",
                "marshal": "marshal module can be unsafe",
            }

            for imp, message in unsafe_imports.items():
                if f"import {imp}" in content or f"from {imp}" in content:
                    file_issues.append(f"⚠️ {message}")

            if file_issues:
                issues.append({"file": py_file.name, "issues": file_issues})

        except Exception as e:
            issues.append(
                {"file": py_file.name, "issues": [f"⚠️ Could not scan file: {e}"]}
            )

    if not issues:
        print("✅ No obvious security issues found in scripts!\n")
    else:
        print(f"⚠️ Found potential issues in {len(issues)} file(s):\n")

        for item in issues:
            print(f"📄 {item['file']}:")
            for issue in item["issues"]:
                print(f"   {issue}")
            print()

    return issues


def generate_recommendations(vulns, script_issues):
    """Generate security recommendations."""
    print("\n💡 Recommendations")
    print("-" * 60)

    recommendations = []

    # Dependency recommendations
    if vulns:
        recommendations.append(
            {
                "priority": "HIGH",
                "category": "Dependencies",
                "action": "Update vulnerable packages",
            }
        )
        recommendations.append(
            {
                "priority": "HIGH",
                "category": "Dependencies",
                "action": "Run: pip install --upgrade <package_name>",
            }
        )
        recommendations.append(
            {
                "priority": "MEDIUM",
                "category": "Dependencies",
                "action": "Pin dependency versions in requirements.txt",
            }
        )

    # Script recommendations
    if script_issues:
        recommendations.append(
            {
                "priority": "HIGH",
                "category": "Code Security",
                "action": "Review and remove hardcoded credentials",
            }
        )
        recommendations.append(
            {
                "priority": "MEDIUM",
                "category": "Code Security",
                "action": "Avoid eval(), exec(), and shell=True in subprocess calls",
            }
        )
        recommendations.append(
            {
                "priority": "LOW",
                "category": "Code Security",
                "action": "Use environment variables for secrets",
            }
        )

    # General recommendations
    recommendations.append(
        {
            "priority": "LOW",
            "category": "General",
            "action": "Run security scan regularly: axle scan",
        }
    )
    recommendations.append(
        {
            "priority": "LOW",
            "category": "General",
            "action": "Keep dependencies updated regularly",
        }
    )

    # Sort by priority
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))

    # Display recommendations
    current_priority = None
    for rec in recommendations:
        if rec["priority"] != current_priority:
            current_priority = rec["priority"]
            print(f"\n{current_priority} Priority:")

        print(f"   • [{rec['category']}] {rec['action']}")

    print()


def main():
    """Main entry point for security scanning."""
    print("\n🔒 Axle Security Scan")
    print("=" * 60)

    # Scan dependencies
    vulns = scan_dependencies()
    parsed_vulns = parse_vulnerabilities(vulns)
    display_vulnerabilities(parsed_vulns)

    # Scan scripts
    script_issues = scan_scripts()

    # Generate recommendations
    generate_recommendations(parsed_vulns, script_issues)

    # Summary
    print("=" * 60)
    print("📊 Summary")
    print("-" * 60)

    vuln_count = len(parsed_vulns)
    issue_count = len(script_issues)

    if vuln_count == 0 and issue_count == 0:
        print("\n✅ No security issues found!")
        print("   Your installation looks secure.")
    else:
        print(f"\n⚠️ Found {vuln_count} vulnerable package(s)")
        print(f"⚠️ Found {issue_count} file(s) with potential issues")

        print("\n📝 For detailed vulnerability information, run:")
        print("   python -m pip_audit --verbose")

    print(COMMUNITY_FOOTER)


if __name__ == "__main__":
    main()
