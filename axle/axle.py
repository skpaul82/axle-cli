#!/usr/bin/env python3
"""Axle CLI."""

import argparse
import importlib.util
import json
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

# Import tool discoverer
from axle.tool_discoverer import ToolDiscoverer

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

# Import tool metadata system
from axle.tool_metadata import (
    update_metadata,
    load_metadata,
    format_tool_metadata,
    search_tools,
    list_tools_summarized,
    get_tool_description_from_file,
)

TOOLS_DIR = Path(__file__).parent.parent / "tools"

# Version from package
try:
    from importlib.metadata import version

    __version__ = version("axle-cli")
except Exception:
    __version__ = "1.2.0"

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
    print("\n🔧 Discovering tools...")
    print("=" * 60)

    tools_path = TOOLS_DIR
    if not tools_path.exists():
        print(f"❌ Tools directory not found.")
        print(f"\n📁 Tools directory should be at: {tools_path.absolute()}")
        print(f"\n💡 To get started:")
        print(f"   1. Create the tools directory:")
        print(f"      mkdir -p {tools_path.absolute()}")
        print(f"   2. Copy your Python scripts to this directory")
        print(f"   3. Run: axle list")
        print(f"   4. Run: axle help <tool_name> for usage")
        print(f"\n   💡 Axle works with ANY Python script!")
        print(f"   Just drop it in the tools directory and run it.")
        return 1

    # Use discoverer to find all tools
    discoverer = ToolDiscoverer(tools_path)
    tools = discoverer.list_tools()

    if not tools:
        print("No tools found in the tools directory.")
        print(f"\n📁 Tools directory: {tools_path.absolute()}")
        print(f"\n💡 To add tools:")
        print(f"   1. Copy any Python script (.py file) to: {tools_path.absolute()}")
        print(f"   2. Run: axle list")
        print(f"   3. Run: axle help <tool_name> for usage")
        print(f"\n   💡 Axle works with ANY Python script!")
        return 0

    print(f"\nFound {len(tools)} tool(s):\n")

    for i, tool in enumerate(tools, 1):
        # Check if it has the Axle contract
        has_contract = tool.metadata.get('has_contract', False)
        contract_badge = "✅" if has_contract else "📜"

        # Check if it uses argparse (main with no args)
        main_func = tool.get_main_function()
        uses_argparse = main_func and main_func.arg_count == 0

        print(f"  {i}. {contract_badge} {tool.name} - {tool.description}")

        # Show available functions
        if tool.metadata.get('all_functions'):
            funcs = tool.metadata['all_functions']
            main_funcs = tool.metadata.get('main_functions', [])
            if main_funcs:
                if uses_argparse:
                    print(f"     🔴 Main: {main_funcs[0]} (argparse-based tool)")
                else:
                    print(f"     🔴 Main: {', '.join(main_funcs)}")

        # Show help command
        print(f"     💡 axle help {tool.name}")

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


def run_tool(tool_identifier, command=None, prompt_or_args=None, enable_security=False, enable_code_review=False):
    """Run a tool by number or name.

    Args:
        tool_identifier: Tool number or name
        command: Optional specific function to run
        prompt_or_args: Prompt text or arguments as string
        enable_security: Enable security validation
        enable_code_review: Enable code review
    """
    tools_path = TOOLS_DIR
    if not tools_path.exists():
        print(f"❌ Tools directory '{TOOLS_DIR}' not found.")
        return 1

    # Check config file for enabled settings if flags are not provided
    should_check_security = enable_security or is_security_enabled()
    should_check_code_review = enable_code_review or is_code_review_enabled()

    # Security validation
    tool_file = None
    if should_check_security:
        discoverer = ToolDiscoverer(tools_path)
        tool = discoverer.get_tool(tool_identifier)
        if tool:
            tool_file = tool.tool_path
            print(f"\n🔒 Validating tool security...")
            policy = get_security_policy()
            print(f"   Security Policy: {policy.upper()}")

            if not validate_tool_before_execution(tool_file, policy=policy):
                print(f"\n❌ Tool execution blocked by security policy.")
                print(f"   To override: AXLE_SECURITY_POLICY=permissive axle run {tool_identifier}")
                return 1

            print(f"   ✅ Security validation passed")
        else:
            print(f"\n❌ Tool '{tool_identifier}' not found.")
            print(f"   Run 'axle list' to see available tools.")
            return 1

    # Code review
    if should_check_code_review:
        if not tool_file:
            discoverer = ToolDiscoverer(tools_path)
            tool = discoverer.get_tool(tool_identifier)
            if tool:
                tool_file = tool.tool_path

        if tool_file:
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

    # Use discoverer to run the tool
    discoverer = ToolDiscoverer(tools_path)

    # Parse arguments - prompt_or_args is already a list from argparse
    args_list = []
    if prompt_or_args:
        if isinstance(prompt_or_args, list):
            args_list = prompt_or_args
        elif isinstance(prompt_or_args, str):
            # If it's a string, try to parse as JSON first, then split by spaces
            try:
                parsed_args = json.loads(prompt_or_args)
                if isinstance(parsed_args, list):
                    args_list = parsed_args
                elif isinstance(parsed_args, str):
                    args_list = [parsed_args]
            except json.JSONDecodeError:
                # Split by spaces
                args_list = prompt_or_args.split()

    # Run the tool
    return discoverer.run_tool(tool_identifier, command, args_list)


def show_tool_usage_help(tool_identifier):
    """Show usage help for a specific tool.

    Args:
        tool_identifier: Tool name or number

    Returns:
        Exit code (0 for success, 1 for error)
    """
    tools_path = TOOLS_DIR
    if not tools_path.exists():
        print(f"❌ Tools directory '{TOOLS_DIR}' not found.")
        return 1

    discoverer = ToolDiscoverer(tools_path)
    tool = discoverer.get_tool(tool_identifier)

    if not tool:
        print(f"❌ Tool '{tool_identifier}' not found.")
        print(f"   Run 'axle list' to see available tools.")
        return 1

    print(tool.get_help_text())
    print_community_footer()
    return 0


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


def update_axle(check_only=False):
    """Update Axle CLI to the latest version.

    Args:
        check_only: If True, only check for updates without installing

    Returns:
        0 on success, 1 on failure
    """
    print("\n🔄 Axle Updater")
    print("=" * 60)

    # Get the current directory
    current_dir = Path.cwd()

    # Check if we're in a git repository
    git_dir = current_dir / ".git"
    if not git_dir.exists():
        # Try to find .git in parent directories
        for parent in [current_dir] + list(current_dir.parents):
            if (parent / ".git").exists():
                git_dir = parent / ".git"
                current_dir = parent
                break

    if not git_dir.exists():
        print("❌ Not in a git repository.")
        print("\n💡 To update Axle, navigate to the axle-cli directory and run:")
        print("   cd /path/to/axle-cli")
        print("   git pull origin main")
        print("   pip install -e .")
        print_community_footer()
        return 1

    print(f"\n📁 Repository: {current_dir}")
    print(f"📍 Current directory: {Path.cwd()}")

    # Check current version
    try:
        current_version = __version__
        print(f"📌 Current version: {current_version}")
    except Exception:
        print("⚠️  Could not determine current version")

    # Check if there are uncommitted changes
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=10
        )

        if result.stdout.strip():
            print("\n⚠️  You have uncommitted changes:")
            print(result.stdout)
            print("\n💡 Please commit or stash your changes before updating.")
            print("   git stash")
            print("   axle update")
            print("   git stash pop")
            print_community_footer()
            return 1
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"\n⚠️  Could not check git status: {e}")
        print_community_footer()
        return 1

    # Fetch latest changes
    print("\n📡 Fetching latest changes from GitHub...")
    try:
        result = subprocess.run(
            ["git", "fetch", "origin"],
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=30
        )

        if result.returncode != 0:
            print(f"❌ Failed to fetch updates: {result.stderr}")
            print_community_footer()
            return 1

        print("✅ Fetched latest changes")

    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"❌ Failed to fetch updates: {e}")
        print_community_footer()
        return 1

    # Check if we're already up to date
    try:
        result = subprocess.run(
            ["git", "rev-list", "--count", "--left-right", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=10
        )

        if result.stdout.strip():
            behind, ahead = result.stdout.strip().split("\t")
            behind = int(behind)
            ahead = int(ahead)

            if behind == 0 and ahead == 0:
                print("\n✅ Already up to date!")
                print_community_footer()
                return 0
            elif behind > 0:
                print(f"\n📦 {behind} new commit(s) available")
            elif ahead > 0:
                print(f"\n⚠️  Your local branch is {ahead} commit(s) ahead of origin/main")
                print("   This is unusual. Consider pushing or resetting.")

        if check_only:
            print("\n💡 To install updates, run:")
            print("   axle update")
            print_community_footer()
            return 0

    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError) as e:
        print(f"\n⚠️  Could not check for updates: {e}")

    # Pull latest changes
    print("\n⬇️  Pulling latest changes...")
    try:
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=30
        )

        if result.returncode != 0:
            print(f"❌ Failed to pull updates: {result.stderr}")
            print_community_footer()
            return 1

        print("✅ Pulled latest changes")
        if result.stdout:
            print(result.stdout)

    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"❌ Failed to pull updates: {e}")
        print_community_footer()
        return 1

    # Update dependencies
    print("\n📦 Updating dependencies...")
    try:
        requirements_file = current_dir / "requirements.txt"
        if requirements_file.exists():
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print("✅ Dependencies updated")
            else:
                print("⚠️  Some dependencies could not be updated")
                print(result.stdout)
        else:
            print("⏭️  No requirements.txt found, skipping dependency update")

    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"⚠️  Could not update dependencies: {e}")

    # Reinstall the package
    print("\n🔧 Reinstalling Axle CLI...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=60
        )

        if result.returncode == 0:
            print("✅ Axle CLI reinstalled successfully")

            # Try to get new version
            try:
                from importlib.metadata import version
                new_version = version("axle-cli")
                print(f"📌 New version: {new_version}")
            except Exception:
                pass

        else:
            print(f"❌ Failed to reinstall: {result.stderr}")
            print_community_footer()
            return 1

    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"❌ Failed to reinstall: {e}")
        print_community_footer()
        return 1

    print("\n✅ Update complete!")
    print("\n💡 Run 'axle doctor' to verify your installation.")
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


def run_metadata_command(action, tool=None, query=None):
    """Run tool metadata commands.

    Args:
        action: Action to perform (scan, show, search, list)
        tool: Tool name (for 'show' action)
        query: Search query (for 'search' action)

    Returns:
        0 on success, 1 on failure
    """
    if action == "scan":
        print("\n🔍 Scanning tools for metadata...")
        print("=" * 60)

        success, message = update_metadata()
        if success:
            print(f"✅ {message}")

            # Show summary
            metadata = load_metadata()
            if metadata and "_metadata" in metadata:
                meta_info = metadata["_metadata"]
                print(f"\n📊 Metadata Summary:")
                print(f"   Last Updated: {meta_info.get('last_updated', 'Unknown')}")
                print(f"   Tool Count: {meta_info.get('tool_count', 0)}")
                print(f"   Axle Version: {meta_info.get('axle_version', 'Unknown')}")
        else:
            print(f"❌ {message}")

        print_community_footer()
        return 0 if success else 1

    elif action == "show":
        if not tool:
            print("\n❌ Please provide a tool name")
            print("   Usage: axle metadata show <tool_name>")
            print_community_footer()
            return 1

        metadata = load_metadata()
        if not metadata or tool not in metadata:
            print(f"\n❌ Tool '{tool}' not found in metadata")
            print("   Run 'axle metadata scan' to update metadata")
            print_community_footer()
            return 1

        formatted = format_tool_metadata(tool, metadata[tool])
        print(formatted)
        print_community_footer()
        return 0

    elif action == "search":
        if not query:
            print("\n❌ Please provide a search query")
            print("   Usage: axle metadata search <query>")
            print_community_footer()
            return 1

        results = search_tools(query)
        if not results:
            print(f"\n❌ No results found for '{query}'")
            print("   Try scanning tools first: axle metadata scan")
            print_community_footer()
            return 0

        print(f"\n🔍 Search Results for '{query}':")
        print("=" * 60)

        for tool_name, tool_metadata in results:
            print(f"\n📋 {tool_name}")

            # Get description
            if tool_metadata.get('has_get_description'):
                tool_path = Path(tool_metadata['path'])
                description = get_tool_description_from_file(tool_path)
                if description:
                    print(f"   {description}")

            # Show matching functions
            matching_functions = [
                f for f in tool_metadata.get('functions', [])
                if query.lower() in f['name'].lower()
            ]
            if matching_functions:
                print(f"   Matching functions: {', '.join([f['name'] for f in matching_functions])}")

        print_community_footer()
        return 0

    elif action == "list":
        summaries = list_tools_summarized()

        if not summaries:
            print("\n⚠️  No tools found in metadata")
            print("   Run 'axle metadata scan' to scan tools")
            print_community_footer()
            return 0

        print(f"\n📋 Available Tools ({len(summaries)}):")
        print("=" * 60)

        for summary in summaries:
            status = "✅" if summary['has_contract'] else "⚠️ "
            print(f"\n{status} {summary['name']}")
            if summary['description']:
                print(f"   {summary['description']}")
            print(f"   Functions: {summary['function_count']}, Classes: {summary['class_count']}")

        print_community_footer()
        return 0

    return 1


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
        "func",
        nargs="?",
        help="Optional specific function/command to run within the tool"
    )
    run_parser.add_argument(
        "args",
        nargs="*",
        help="Arguments to pass to the tool function (space-separated)"
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
    help_parser = subparsers.add_parser("help", help="Show this help message")
    help_parser.add_argument("tool", nargs="?", help="Show help for a specific tool")

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

    # axle update
    update_parser = subparsers.add_parser("update", help="Update Axle CLI to latest version")
    update_parser.add_argument(
        "--check",
        action="store_true",
        help="Only check for updates without installing"
    )

    # axle metadata
    metadata_parser = subparsers.add_parser("metadata", help="Manage tool metadata")
    metadata_subparsers = metadata_parser.add_subparsers(dest="metadata_action", required=True)

    # axle metadata scan
    metadata_subparsers.add_parser("scan", help="Scan tools and update metadata")

    # axle metadata show
    metadata_show_parser = metadata_subparsers.add_parser("show", help="Show detailed metadata for a tool")
    metadata_show_parser.add_argument("tool", help="Tool name")

    # axle metadata search
    metadata_search_parser = metadata_subparsers.add_parser("search", help="Search tools by name, functions, or description")
    metadata_search_parser.add_argument("query", help="Search query")

    # axle metadata list
    metadata_subparsers.add_parser("list", help="List all tools with summaries")

    args = parser.parse_args()

    # Route to appropriate command
    if args.command == "list":
        return list_tools()
    elif args.command == "run":
        # Combine args into prompt_or_args
        prompt_or_args = args.args if args.args else None

        return run_tool(
            args.tool,
            command=getattr(args, "func", None),
            prompt_or_args=prompt_or_args,
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
    elif args.command == "update":
        return update_axle(check_only=getattr(args, "check", False))
    elif args.command == "metadata":
        return run_metadata_command(
            action=getattr(args, "metadata_action", None),
            tool=getattr(args, "tool", None),
            query=getattr(args, "query", None),
        )
    elif args.command == "help":
        tool = getattr(args, "tool", None)
        if tool:
            # Show tool-specific help
            return show_tool_usage_help(tool)
        else:
            # Show general help
            parser.print_help()
            return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
