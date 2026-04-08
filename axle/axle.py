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
from axle.tool_validator import validate_tool_before_execution, get_security_policy

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


def print_community_footer():
    """Print community links footer."""
    print(COMMUNITY_FOOTER)


def list_tools():
    """List all available tools in the tools directory."""
    print(
        "Hey there, let me know how I can help you. Choose a tool from the list or enter a number.\n"
    )

    tools_path = Path(TOOLS_DIR)
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

    if not files:
        print("No tools found in the tools directory.")
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


def run_tool(tool_identifier, prompt=""):
    """Run a tool by number or name."""
    tools_path = Path(TOOLS_DIR)
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

    # 🔒 SECURITY VALIDATION: Validate tool before execution
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
        print(f"❌ Error running tool: {e}")
        return 1


def show_tool_info(tool_name):
    """Show information about a specific tool."""
    tools_path = Path(TOOLS_DIR)
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

    tools_path = Path(TOOLS_DIR)
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
        try:
            __import__(dep)
            print(f"   ✓ {dep}")
        except ImportError:
            print(f"   ✗ {dep} (not installed)")

    # Check tools directory
    tools_path = Path(TOOLS_DIR)
    print(f"\n🔧 Tools Directory:")
    if tools_path.exists():
        tools_count = len(
            [f for f in tools_path.glob("*.py") if f.name != "__init__.py"]
        )
        print(f"   ✓ Found at: {tools_path.absolute()}")
        print(f"   ✓ Contains {tools_count} tools")
    else:
        print(f"   ✗ Not found at: {tools_path.absolute()}")

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
    tools_path = Path(TOOLS_DIR).absolute()
    print(f"📁 Tools folder path: {tools_path}")

    if tools_path.exists():
        files = list(tools_path.glob("*.py"))
        if files:
            print(f"\nContains {len(files)} file(s):")
            for f in sorted(files):
                if f.name != "__init__.py":
                    print(f"  - {f.name}")
    else:
        print("\n⚠ Directory does not exist yet.")

    print_community_footer()
    return 0


def show_security_config(policy=None):
    """Show or configure security policy."""
    from axle.tool_validator import POLICY_STRICT, POLICY_WARN, POLICY_PERMISSIVE

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
                "use_case": "Trusted tools, local development",
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
    tools_path = Path(TOOLS_DIR)
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


def main():
    """Main entry point for the Axle CLI."""
    parser = argparse.ArgumentParser(
        prog="axle",
        description="Axle: A modular CLI platform for running Python microtools.",
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
        return run_tool(args.tool, args.prompt)
    elif args.command == "info":
        return show_tool_info(args.tool)
    elif args.command == "scan":
        return scan_dependencies()
    elif args.command == "doctor":
        return run_diagnostics()
    elif args.command == "path":
        return show_tools_path()
    elif args.command == "security":
        return show_security_config(getattr(args, "policy", None))
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
