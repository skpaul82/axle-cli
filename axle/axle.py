#!/usr/bin/env python3
"""Axle CLI."""

import argparse
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Import tool security validator
from axle.tool_validator import get_security_policy, validate_tool_before_execution

# Import code reviewer
from axle.code_reviewer import (
    CodeReviewer,
    get_auto_fix_policy,
    get_code_review_policy,
    should_run_code_review,
)

# Import config management
from axle.config import (
    is_security_enabled,
    is_code_review_enabled,
    set_security_setting,
    set_code_review_setting,
    get_security_setting,
    get_code_review_setting,
    show_config,
)

TOOLS_DIR = Path(__file__).parent.parent / "tools"

# Version from package
try:
    from importlib.metadata import version

    __version__ = version("axle-cli")
except Exception:
    __version__ = "1.1.0"

COMMUNITY_FOOTER = """
---
🌐 Community & Support
⭐ Star on GitHub: https://github.com/skpaul82/axle-cli
🐦 Follow on X: @_skpaul82
🌐 Website: https://www.axle.sanjoypaul.com

♥ Built for the community
"""


def print_community_footer():
    """Print community links footer."""
    print(COMMUNITY_FOOTER)


def list_tools():
    """List all available tools in the tools directory."""
    print(
        "Hey there, let me know how I can help you. Choose a tool from the list or enter a number.\n"
    )

    tools_path = TOOLS_DIR
    if not tools_path.exists():
        print(f"❌ Tools directory not found.")
        print(f"\n📁 Tools directory should be at: {tools_path.absolute()}")
        print(f"\n💡 To get started:")
        print(f"   1. Create the tools directory:")
        print(f"      mkdir -p {tools_path.absolute()}")
        print(f"   2. Add your Python tools to this directory")
        print(
            f"   3. Each tool must implement get_description() and main(prompt) functions"
        )
        print(f"   4. Learn more at: https://www.axle.sanjoypaul.com")
        return 1

    files = sorted(
        [
            f
            for f in tools_path.iterdir()
            if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"
        ]
    )

    if not files:
        print("No tools found in the tools directory.")
        print(f"\n📁 Tools directory: {tools_path.absolute()}")
        print(f"\n💡 To add tools:")
        print(f"   1. Create Python files in: {tools_path.absolute()}")
        print(
            f"   2. Each tool must implement get_description() and main(prompt) functions"
        )
        print(f"   3. Example tool structure:")
        print(f"      def get_description() -> str:")
        print(f"          return 'Your tool description'")
        print(f"      def main(prompt: str) -> None:")
        print(f"          # Your tool logic here")
        print(f"          pass")
        print(f"   4. Learn more at: https://www.axle.sanjoypaul.com")
        return 0

    for i, f in enumerate(files, 1):
        # Try to get description from tool
        description = _get_tool_description(f)
        print(f"  {i}. {f.stem} - {description}")

    print_community_footer()
    return 0


def _get_tool_description(tool_file):
    """Get description from a tool file."""
    try:
        spec = importlib.util.spec_from_file_location(tool_file.stem, tool_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "get_description"):
                return module.get_description()
        return "No description available"
    except Exception:
        return "No description available"


def run_tool(tool_identifier, prompt="", enable_security=False, enable_code_review=False):
    """Run a tool by number or name."""
    tools_path = TOOLS_DIR
    if not tools_path.exists():
        print(f"❌ Tools directory '{TOOLS_DIR}' not found.")
        return 1

    files = sorted(
        [
            f
            for f in tools_path.iterdir()
            if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"
        ]
    )

    # Determine which tool to run
    tool_file = None
    try:
        # Try as number
        tool_num = int(tool_identifier)
        if tool_num < 1 or tool_num > len(files):
            print(f"❌ Invalid tool number. Choose between 1 and {len(files)}.")
            return 1
        tool_file = files[tool_num - 1]
    except ValueError:
        # Try as name
        tool_name = (
            tool_identifier
            if tool_identifier.endswith(".py")
            else f"{tool_identifier}.py"
        )
        for f in files:
            if f.name == tool_name:
                tool_file = f
                break
        if not tool_file:
            print(f"❌ Tool '{tool_identifier}' not found.")
            print(f"   Run 'axle list' to see available tools.")
            return 1

    # Check config file for enabled settings if flags are not provided
    should_check_security = enable_security or is_security_enabled()
    should_check_code_review = enable_code_review or is_code_review_enabled()

    # 🔒 SECURITY VALIDATION: Only run if enabled via flag or config
    if should_check_security:
        print(f"\n🔒 Validating tool security...")
        policy = get_security_policy()
        print(f"   Security Policy: {policy.upper()}")

        if not validate_tool_before_execution(tool_file, policy=policy):
            print(f"\n❌ Tool execution blocked by security policy.")
            print(
                f"   To override: AXLE_SECURITY_POLICY=permissive axle run {tool_identifier}"
            )
            return 1

        print(f"   ✅ Security validation passed")
    else:
        print(f"\n⏭️  Security validation skipped")
        if not is_security_enabled():
            print(f"   Enable with: axle security enable")
        print(f"   Or use: axle run {tool_identifier} --security")

    # 🔍 CODE REVIEW: Only run if enabled via flag or config
    if should_check_code_review:
        print(f"\n🔍 Running automatic code review...")
        reviewer = CodeReviewer(verbose=False)
        issues = reviewer.review_file(tool_file)

        if issues:
            print(f"   Found {len(issues)} code quality issue(s):")
            for issue in issues:
                print(f"   {issue}")

            # Determine if we should auto-fix
            auto_fix = get_auto_fix_policy()
            if auto_fix:
                auto_fixed, manual_fixes = reviewer.auto_fix_issues(tool_file, issues)
                if auto_fixed > 0:
                    print(f"   ✅ Applied {auto_fixed} automatic fix(es)")
                if manual_fixes > 0:
                    print(f"   ⚠️  {manual_fixes} issue(s) need manual attention")
            else:
                # Ask user if they want to fix
                auto_fixable = sum(1 for i in issues if i.fixable == "AUTO")
                if auto_fixable > 0:
                    print(f"\n   📋 Apply {auto_fixable} automatic fix(es)? [Y/n]: ", end="")
                    try:
                        user_choice = input().strip().lower()
                        if user_choice != "n":
                            auto_fixed, manual_fixes = reviewer.auto_fix_issues(tool_file, issues)
                            if auto_fixed > 0:
                                print(f"   ✅ Applied {auto_fixed} automatic fix(es)")
                            if manual_fixes > 0:
                                print(f"   ⚠️  {manual_fixes} issue(s) need manual attention")
                        else:
                            manual_fixes = sum(1 for i in issues if i.fixable == "MANUAL")
                            if manual_fixes > 0:
                                print(f"   ⚠️  {manual_fixes} issue(s) need manual attention")
                    except (EOFError, KeyboardInterrupt):
                        # In non-interactive mode, skip the fixes
                        manual_fixes = sum(1 for i in issues if i.fixable == "MANUAL")
                        if manual_fixes > 0:
                            print(f"   ⚠️  {manual_fixes} issue(s) need manual attention")
                else:
                    manual_fixes = sum(1 for i in issues if i.fixable == "MANUAL")
                    if manual_fixes > 0:
                        print(f"   ⚠️  {manual_fixes} issue(s) need manual attention")
        else:
            print(f"   ✅ Code review passed")
    else:
        print(f"\n⏭️  Code review skipped")
        if not is_code_review_enabled():
            print(f"   Enable with: axle review enable")
        print(f"   Or use: axle run {tool_identifier} --code-review")

    # Load and run the tool
    try:
        spec = importlib.util.spec_from_file_location(tool_file.stem, tool_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "main"):
                print(f"\n🔧 Running {tool_file.stem}...\n")
                module.main(prompt)
                print_community_footer()
                return 0
            else:
                print(f"❌ Tool '{tool_file.stem}' does not have a main() function.")
                return 1
    except Exception as e:
        import traceback

        print(f"❌ Error running tool: {e}", file=sys.stderr)
        traceback.print_exc()
        return 1


def show_tool_info(tool_name):
    """Show information about a specific tool."""
    tools_path = TOOLS_DIR
    if not tools_path.exists():
        print(f"❌ Tools directory '{TOOLS_DIR}' not found.")
        return 1

    # Try exact match first
    tool_file = tool_name if tool_name.endswith(".py") else f"{tool_name}.py"
    tool_path = tools_path / tool_file

    # If not found, try matching the name part (after numeric prefix)
    if not tool_path.exists():
        for f in tools_path.glob("*.py"):
            if f.name == "__init__.py":
                continue
            # Match by name part (with or without numeric prefix)
            if (
                f.stem == tool_name
                or f.stem.endswith(f"_{tool_name}")
                or f.stem == f"_{tool_name}".replace("_", "", 1)
            ):
                tool_path = f
                break
            # Check if the name contains the search term
            if tool_name in f.stem:
                tool_path = f
                break

    if not tool_path.exists():
        print(f"❌ Tool '{tool_name}' not found.")
        print(f"   Run 'axle list' to see available tools.")
        return 1

    try:
        spec = importlib.util.spec_from_file_location(tool_name, tool_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print(f"\n📋 Tool: {tool_name}")
            print(f"📍 Location: {tool_path.absolute()}")

            if hasattr(module, "get_description"):
                print(f"📝 Description: {module.get_description()}")

            if hasattr(module, "__doc__") and module.__doc__:
                print(f"\n📄 Documentation:\n{module.__doc__.strip()}")

            print_community_footer()
            return 0
    except Exception as e:
        print(f"❌ Error loading tool: {e}")
        return 1


def scan_dependencies():
    """Run security vulnerability scan on dependencies."""
    print("🔒 Running Axle Security Scan")
    print("=" * 50)

    # Check if pip-audit is installed
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip_audit", "--format", "json"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("✓ No critical vulnerabilities found in dependencies.\n")
        else:
            # Try to parse and display results
            print("⚠ Potential vulnerabilities detected:\n")
            print(result.stdout)
    except FileNotFoundError:
        print("⚠ pip-audit is not installed.")
        print("  Install with: pip install pip-audit")
        print("  Or run: pip install -r requirements.txt (pip-audit is included)\n")

    # Basic script scan
    print("🔍 Scanning scripts for security issues...\n")

    tools_path = TOOLS_DIR
    if tools_path.exists():
        issues = []
        for py_file in tools_path.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            content = py_file.read_text()

            # Check for dangerous imports
            dangerous = ["eval(", "exec(", "compile(", "__import__("]
            for danger in dangerous:
                if danger in content:
                    issues.append(f"⚠ {py_file.name}: Uses {danger}")

            # Check for potential secrets (basic patterns)
            secret_patterns = ["api_key", "apikey", "secret", "password", "token"]
            for pattern in secret_patterns:
                if f'"{pattern}": "' in content or f"'{pattern}': '" in content:
                    issues.append(
                        f"⚠ {py_file.name}: May contain hardcoded '{pattern}'"
                    )

        if issues:
            for issue in issues:
                print(issue)
        else:
            print("✓ No obvious security issues found in scripts.\n")

    print_community_footer()
    return 0


def run_diagnostics():
    """Run environment and setup diagnostics."""
    print("🏥 Axle Environment Check")
    print("=" * 50)

    # Python version
    py_version = sys.version_info
    print(
        f"\n🐍 Python Version: {py_version.major}.{py_version.minor}.{py_version.micro}"
    )
    if py_version < (3, 10):
        print("   ⚠ Warning: Python 3.10+ recommended")
    else:
        print("   ✓ Python version OK")

    # Platform
    print(f"\n💻 Platform: {platform.system()} {platform.machine()}")

    # Disk space
    disk = shutil.disk_usage(".")
    disk_free_gb = disk.free / (1024**3)
    print(f"\n💾 Disk Space:")
    print(f"   Free: {disk_free_gb:.1f} GB")
    if disk_free_gb < 5:
        print("   ⚠ Warning: Less than 5GB free space")
    else:
        print("   ✓ Disk space OK")

    # RAM (basic check)
    try:
        import psutil

        ram_gb = psutil.virtual_memory().total / (1024**3)
        print(f"\n🧠 RAM: {ram_gb:.1f} GB")
        if ram_gb < 8:
            print("   ⚠ Warning: Less than 8GB RAM")
        else:
            print("   ✓ RAM OK")
    except ImportError:
        print("\n🧠 RAM: Unable to check (psutil not installed)")

    # Check key dependencies
    print(f"\n📦 Key Dependencies:")
    dependencies = [
        "pandas",
        "numpy",
        "requests",
        "bs4",
        "nltk",
        "sklearn",
        "spacy",
        "sentence_transformers",
    ]

    for dep in dependencies:
        if importlib.util.find_spec(dep) is not None:
            print(f"   ✓ {dep}")
        else:
            print(f"   ✗ {dep} (not installed)")

    # Check tools directory
    tools_path = TOOLS_DIR
    print(f"\n🔧 Tools Directory:")
    if tools_path.exists():
        tools_count = len(
            [f for f in tools_path.glob("*.py") if f.name != "__init__.py"]
        )
        print(f"   ✓ Found at: {tools_path.absolute()}")
        print(f"   ✓ Contains {tools_count} tools")
        if tools_count == 0:
            print(f"\n💡 To add tools, visit: https://www.axle.sanjoypaul.com")
    else:
        print(f"   ✗ Not found at: {tools_path.absolute()}")
        print(f"\n💡 To create tools directory:")
        print(f"      mkdir -p {tools_path.absolute()}")
        print(f"   Learn more at: https://www.axle.sanjoypaul.com")

    # Check if CLI is installed
    print(f"\n⚙️ CLI Installation:")
    try:
        result = subprocess.run(["axle", "--help"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print("   ✓ CLI command 'axle' is working")
        else:
            print("   ⚠ CLI command 'axle' exists but may have issues")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("   ⚠ CLI command 'axle' not found in PATH")
        print("     Run: pip install -e .")

    print_community_footer()
    return 0


def show_tools_path():
    """Show the current tools folder location."""
    tools_path = TOOLS_DIR
    print(f"📁 Tools folder path: {tools_path.absolute()}")

    if tools_path.exists():
        files = list(tools_path.glob("*.py"))
        if files:
            print(f"\nContains {len(files)} file(s):")
            for f in sorted(files):
                if f.name != "__init__.py":
                    print(f"  - {f.name}")
        else:
            print("\n📭 Directory is empty.")
            print(f"\n💡 To add tools:")
            print(f"   1. Create Python files in: {tools_path.absolute()}")
            print(f"   2. Each tool must implement:")
            print(f"      - get_description() -> str")
            print(f"      - main(prompt: str) -> None")
            print(f"   3. Learn more at: https://www.axle.sanjoypaul.com")
    else:
        print("\n⚠ Directory does not exist yet.")
        print(f"\n💡 To get started:")
        print(f"   1. Create the tools directory:")
        print(f"      mkdir -p {tools_path.absolute()}")
        print(f"   2. Add your Python tools to this directory")
        print(f"   3. Learn more at: https://www.axle.sanjoypaul.com")

    print_community_footer()
    return 0


def show_security_config(policy=None, enable=None, disable=None, show=None):
    """Show or configure security policy."""
    from axle.tool_validator import POLICY_PERMISSIVE, POLICY_STRICT, POLICY_WARN

    if enable:
        # Enable security validation
        set_security_setting(True)
        print("\n✅ Security validation ENABLED")
        print("\nSecurity checks will now run by default when using 'axle run'.")
        print("To disable: axle security disable")
        print_community_footer()
        return 0

    if disable:
        # Disable security validation
        set_security_setting(False)
        print("\n❌ Security validation DISABLED")
        print("\nSecurity checks will be skipped by default.")
        print("To enable: axle security enable")
        print("\nYou can still run security checks manually with:")
        print("  axle run <tool> --security")
        print_community_footer()
        return 0

    if show:
        # Show current configuration
        config = show_config()
        current_setting = get_security_setting()

        print("\n🔒 Axle Security Configuration")
        print("=" * 60)

        if current_setting:
            status = "ENABLED" if current_setting == "enabled" else "DISABLED"
            print(f"\nSecurity Validation: {status}")
        else:
            print("\nSecurity Validation: DISABLED (default)")

        print("\nUsage:")
        print("  axle security enable   - Enable security checks by default")
        print("  axle security disable  - Disable security checks by default")
        print("  axle run <tool> --security - Run security check for this tool only")
        print_community_footer()
        return 0

    if policy is None:
        # Show current policy
        current_policy = get_security_policy()

        print("\n🔒 Axle Security Configuration")
        print("=" * 60)

        print(f"\nCurrent Policy: {current_policy.upper()}")

        policies = {
            POLICY_STRICT: {
                "description": "Block execution on ANY security finding",
                "blocks": ["All severity levels (Critical, High, Medium, Low)"],
                "use_case": "Production environments, untrusted tools",
            },
            POLICY_WARN: {
                "description": "Block only on CRITICAL findings, warn on others",
                "blocks": ["Critical severity"],
                "use_case": "Development environments (default)",
            },
            POLICY_PERMISSIVE: {
                "description": "Block only on CRITICAL/HIGH findings",
                "blocks": ["Critical, High severity"],
                "use_case": "Trusted tools, local development (default)",
            },
        }

        print("\nPolicy Details:")
        for p_name, p_info in policies.items():
            is_current = "✓" if p_name == current_policy else " "
            print(f"\n  {is_current} {p_name.upper()}")
            print(f"     {p_info['description']}")
            print(f"     Blocks: {', '.join(p_info['blocks'])}")
            print(f"     Best for: {p_info['use_case']}")

        print("\n\nHow to Set Policy:")
        print("  Environment Variable: export AXLE_SECURITY_POLICY=<policy>")
        print("  Command: axle security --policy <policy>")
        print("\nAvailable Policies: strict, warn, permissive")

    else:
        # Set policy
        print(f"\n🔒 Setting Security Policy: {policy.upper()}")
        print("\nTo make this permanent, set the environment variable:")
        print(f"  export AXLE_SECURITY_POLICY={policy}")
        print("\nThen run your tool:")
        print("  axle run <tool>")

    print_community_footer()
    return 0


def uninstall_axle(keep_tools=True, remove_tools=False):
    """Uninstall Axle CLI while preserving tools directory."""
    print("\n🗑️  Axle Uninstaller")
    print("=" * 60)

    if remove_tools:
        keep_tools = False

    # Check what will be removed
    tools_path = TOOLS_DIR
    has_custom_tools = False

    if keep_tools and tools_path.exists():
        tool_files = [f for f in tools_path.glob("*.py") if f.name != "__init__.py"]
        # Check if user has custom tools (beyond the 3 default ones)
        if len(tool_files) > 3:
            has_custom_tools = True

    print("\nThis will uninstall the Axle CLI.")
    if keep_tools and has_custom_tools:
        print(f"✅ Your tools directory will be preserved with {len(tool_files)} tools")
    elif keep_tools and tools_path.exists():
        print("✅ Your tools directory will be preserved")
    elif not keep_tools and tools_path.exists():
        print("⚠️  Your tools directory will also be removed")

    print("\nTo uninstall, run:")
    print("  pip uninstall axle-cli")

    if keep_tools:
        print(f"\nYour tools will remain at: {tools_path.absolute()}")
        print("To reinstall Axle later:")
        print("  pip install -e .")
        print("  (from the directory containing tools/)")

    print_community_footer()
    return 0


def run_code_review_command(tool=None, fix=False, review_all=False, dry_run=False, verbose=False, enable=None, disable=None, show=None):
    """Run code review on tool(s).

    Args:
        tool: Specific tool name to review
        fix: Apply automatic fixes
        review_all: Review all tools
        dry_run: Show what would be fixed without making changes
        verbose: Enable detailed output
        enable: Enable code review by default
        disable: Disable code review by default
        show: Show current code review configuration
    """
    # Handle enable/disable/show commands
    if enable:
        set_code_review_setting(True)
        print("\n✅ Code review ENABLED")
        print("\nCode review will now run by default when using 'axle run'.")
        print("To disable: axle review disable")
        print_community_footer()
        return 0

    if disable:
        set_code_review_setting(False)
        print("\n❌ Code review DISABLED")
        print("\nCode review will be skipped by default.")
        print("To enable: axle review enable")
        print("\nYou can still run code review manually with:")
        print("  axle run <tool> --code-review")
        print("  axle review <tool_name>")
        print_community_footer()
        return 0

    if show:
        config = show_config()
        current_setting = get_code_review_setting()

        print("\n🔍 Axle Code Review Configuration")
        print("=" * 60)

        if current_setting:
            status = "ENABLED" if current_setting == "enabled" else "DISABLED"
            print(f"\nCode Review: {status}")
        else:
            print("\nCode Review: DISABLED (default)")

        print("\nUsage:")
        print("  axle review enable   - Enable code review by default")
        print("  axle review disable  - Disable code review by default")
        print("  axle run <tool> --code-review - Run code review for this tool only")
        print("  axle review <tool>   - Run code review on a specific tool")
        print("  axle review --all    - Run code review on all tools")
        print_community_footer()
        return 0

    print("🔍 Axle Code Review")
    print("=" * 50)

    tools_path = TOOLS_DIR
    if not tools_path.exists():
        print(f"❌ Tools directory '{TOOLS_DIR}' not found.")
        return 1

    # Determine which tools to review
    tools_to_review = []
    if review_all:
        tools_to_review = [
            f for f in tools_path.glob("*.py") if f.name != "__init__.py"
        ]
    elif tool:
        # Find the specific tool
        tool_file = tool if tool.endswith(".py") else f"{tool}.py"
        tool_path = tools_path / tool_file
        if tool_path.exists():
            tools_to_review = [tool_path]
        else:
            # Try to find by name part
            for f in tools_path.glob("*.py"):
                if tool in f.stem:
                    tools_to_review = [f]
                    break
        if not tools_to_review:
            print(f"❌ Tool '{tool}' not found.")
            print(f"   Run 'axle list' to see available tools.")
            return 1
    else:
        print("❌ Please specify a tool or use --all to review all tools.")
        print("   Usage: axle review <tool_name>")
        print("          axle review --all")
        return 1

    if not tools_to_review:
        print("No tools found to review.")
        return 1

    # Create reviewer
    reviewer = CodeReviewer(verbose=verbose)
    all_issues = []
    total_auto_fixed = 0
    total_manual_fixes = 0

    # Review each tool
    for tool_path in sorted(tools_to_review):
        print(f"\n📁 {tool_path.name}:")

        issues = reviewer.review_file(tool_path)
        all_issues.extend(issues)

        if issues:
            print(f"   Found {len(issues)} issue(s)")
            for issue in issues:
                if verbose:
                    print(f"   {issue}")
                else:
                    # Show only severity and category in non-verbose mode
                    print(f"   {issue.severity} [{issue.category}] {issue.message}")

            # Apply fixes if requested
            if fix or dry_run:
                auto_fixed, manual_fixes = reviewer.auto_fix_issues(
                    tool_path, issues, dry_run=dry_run
                )
                if auto_fixed > 0:
                    if dry_run:
                        print(f"   📋 Would fix: {auto_fixed} automatic fix(es)")
                    else:
                        print(f"   ✅ Applied {auto_fixed} automatic fix(es)")
                    total_auto_fixed += auto_fixed
                if manual_fixes > 0:
                    print(f"   ⚠️  {manual_fixes} issue(s) need manual attention")
                    total_manual_fixes += manual_fixes
        else:
            print("   ✅ No issues found")

    # Summary
    print(f"\n{'=' * 50}")
    print(f"📊 Review Summary:")
    print(f"   Tools reviewed: {len(tools_to_review)}")
    print(f"   Total issues: {len(all_issues)}")
    if fix or dry_run:
        if dry_run:
            print(f"   Would apply: {total_auto_fixed} automatic fix(es)")
        else:
            print(f"   Applied: {total_auto_fixed} automatic fix(es)")
        print(f"   Manual fixes needed: {total_manual_fixes}")

    # Show policy info
    print(f"\n🔧 Configuration:")
    print(f"   Code Review Policy: {get_code_review_policy().upper()}")
    print(f"   Auto-Fix: {get_auto_fix_policy()}")

    # Show environment variables
    print(f"\n💡 Environment Variables:")
    print(f"   AXLE_CODE_REVIEW={get_code_review_policy()}")
    print(f"   AXLE_AUTO_FIX={get_auto_fix_policy()}")

    # Exit with error if critical issues found
    has_critical = any(i.severity == "CRITICAL" for i in all_issues)
    if has_critical:
        print(f"\n❌ Critical issues found!")
        return 1

    return 0


def main():
    """Main entry point for the Axle CLI."""
    parser = argparse.ArgumentParser(
        prog="axle",
        description="Axle: A modular CLI platform for running Python microtools.",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # axle list
    subparsers.add_parser("list", help="List all available tools")

    # axle run
    run_parser = subparsers.add_parser("run", help="Run a tool by number or name")
    run_parser.add_argument("tool", help="Tool number or name (without .py)")
    run_parser.add_argument(
        "prompt", nargs="?", default="", help="Optional prompt text"
    )
    run_parser.add_argument(
        "--security",
        action="store_true",
        help="Enable security validation (default: disabled)"
    )
    run_parser.add_argument(
        "--code-review",
        action="store_true",
        help="Enable code quality review (default: disabled)"
    )

    # axle info
    info_parser = subparsers.add_parser("info", help="Show tool information")
    info_parser.add_argument("tool", help="Tool name")

    # axle scan
    subparsers.add_parser("scan", help="Scan dependencies for vulnerabilities")

    # axle doctor
    subparsers.add_parser("doctor", help="Run environment diagnostics")

    # axle path
    subparsers.add_parser("path", help="Show tools folder location")

    # axle help
    subparsers.add_parser("help", help="Show this help message")

    # axle security
    security_parser = subparsers.add_parser(
        "security", help="Show or configure security policy"
    )
    security_parser.add_argument(
        "--policy",
        choices=["strict", "warn", "permissive"],
        help="Set security policy (or use AXLE_SECURITY_POLICY env var)",
    )
    security_parser.add_argument(
        "--enable",
        action="store_true",
        help="Enable security validation by default"
    )
    security_parser.add_argument(
        "--disable",
        action="store_true",
        help="Disable security validation by default"
    )
    security_parser.add_argument(
        "--show",
        action="store_true",
        help="Show current security configuration"
    )

    # axle review
    review_parser = subparsers.add_parser("review", help="Run code review on tools")
    review_parser.add_argument(
        "tool", nargs="?", help="Tool name to review (omit for --all)"
    )
    review_parser.add_argument(
        "--fix", action="store_true", help="Apply automatic fixes"
    )
    review_parser.add_argument(
        "--all", action="store_true", help="Review all tools"
    )
    review_parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be fixed without making changes"
    )
    review_parser.add_argument(
        "--verbose", action="store_true", help="Detailed output"
    )
    review_parser.add_argument(
        "--enable",
        action="store_true",
        help="Enable code review by default"
    )
    review_parser.add_argument(
        "--disable",
        action="store_true",
        help="Disable code review by default"
    )
    review_parser.add_argument(
        "--show",
        action="store_true",
        help="Show current code review configuration"
    )

    # axle uninstall
    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Uninstall Axle CLI (preserves tools directory)"
    )
    uninstall_parser.add_argument(
        "--keep-tools",
        action="store_true",
        default=True,
        help="Preserve tools directory (default: True)",
    )
    uninstall_parser.add_argument(
        "--remove-tools", action="store_true", help="Also remove tools directory"
    )

    args = parser.parse_args()

    # Route to appropriate command
    if args.command == "list":
        return list_tools()
    elif args.command == "run":
        return run_tool(
            args.tool,
            args.prompt,
            enable_security=getattr(args, "security", False),
            enable_code_review=getattr(args, "code_review", False),
        )
    elif args.command == "info":
        return show_tool_info(args.tool)
    elif args.command == "scan":
        return scan_dependencies()
    elif args.command == "doctor":
        return run_diagnostics()
    elif args.command == "path":
        return show_tools_path()
    elif args.command == "security":
        return show_security_config(
            policy=getattr(args, "policy", None),
            enable=getattr(args, "enable", False),
            disable=getattr(args, "disable", False),
            show=getattr(args, "show", False),
        )
    elif args.command == "review":
        return run_code_review_command(
            tool=getattr(args, "tool", None),
            fix=getattr(args, "fix", False),
            review_all=getattr(args, "all", False),
            dry_run=getattr(args, "dry_run", False),
            verbose=getattr(args, "verbose", False),
            enable=getattr(args, "enable", False),
            disable=getattr(args, "disable", False),
            show=getattr(args, "show", False),
        )
    elif args.command == "uninstall":
        return uninstall_axle(
            keep_tools=not getattr(args, "remove_tools", False),
            remove_tools=getattr(args, "remove_tools", False),
        )
    elif args.command == "help":
        parser.print_help()
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
