#!/usr/bin/env python3
"""Interactive installer for Axle."""

import shutil
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = "tools"

FAQ_URL = "https://www.axle.sanjoypaul.com/docs/troubleshooting"
DOCS_URL = "https://www.axle.sanjoypaul.com/docs"

COMMUNITY_FOOTER = """
---
🌐 Community & Support
⭐ Star on GitHub: https://github.com/skpaul82/axle-cli
🐦 Follow on X: @_skpaul82
🌐 Website: https://www.axle.sanjoypaul.com

♥ Built for the community
"""


def welcome_message():
    """Display welcome message."""
    print("\n" + "=" * 60)
    print("🚀 Welcome to Axle Setup!")
    print("=" * 60)
    print("\nAxle is a CLI platform for SEO and daily-life productivity.")
    print("\nThis installer will:")
    print("  1. Check your system requirements")
    print("  2. Install Python dependencies")
    print("  3. Set up the axle command")
    print("  4. Download required ML models")
    print("  5. Verify installation")


def check_environment():
    """Run comprehensive environment check first."""
    print("\n" + "=" * 60)
    print("🔍 Environment Check")
    print("=" * 60)

    issues = []

    # Check Python version
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"\n🐍 Python Version: {version_str}")

    if version < (3, 10):
        print(f"   ❌ Python 3.10+ required. You have {version_str}")
        issues.append("Python version")
    else:
        print(f"   ✅ Python version OK")

    # Check pip availability
    print("\n📦 Checking pip availability...")
    pip_available = False
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            pip_version = result.stdout.strip()
            print(f"   ✅ pip available: {pip_version}")
            pip_available = True
        else:
            print("   ❌ pip not available")
            issues.append("pip not available")
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"   ❌ pip check failed: {e}")
        issues.append("pip not available")

    # Check if we can install packages
    if pip_available:
        print("\n🔧 Testing package installation...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                print("   ✅ Can install packages")
            else:
                print("   ⚠️  Cannot install packages")
                issues.append("Cannot install packages")
        except Exception as e:
            print(f"   ⚠️  Package install test failed: {e}")
            issues.append("Package installation failed")

    # If issues found, show FAQ
    if issues:
        print("\n" + "=" * 60)
        print("⚠️  Environment Issues Detected")
        print("=" * 60)
        print("\nThe following issues were found:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")

        print("\n📚 Troubleshooting Options:")
        print(f"   1. Read the FAQ: {FAQ_URL}")
        print(f"   2. Documentation: {DOCS_URL}")
        print("   3. Try manual installation (see README.md)")

        print("\nCommon solutions:")
        print("   • Python version: Upgrade to 3.10+ from python.org")
        print("   • pip issues: Try 'python -m ensurepip --upgrade'")
        print("   • Permission issues: Try using 'pip install --user'")

        continue_install = (
            input("\nContinue with installation anyway? [y/N]: ").strip().lower()
        )
        if continue_install not in ["y", "yes"]:
            print("\n❌ Installation cancelled. Please resolve the issues above.")
            print(f"See FAQ for help: {FAQ_URL}")
            sys.exit(1)

    print("\n✅ Environment check passed")


def check_python_version():
    """Check if Python version is 3.10+."""
    print("\n" + "-" * 60)
    print("📋 Checking Python version...")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    print(f"   Found Python {version_str}")

    if version < (3, 10):
        print(f"   ❌ Python 3.10+ required. You have {version_str}")
        print("   Please upgrade Python: https://www.python.org/downloads/")
        return False
    else:
        print(f"   ✅ Python version OK (3.10+ required)")
        return True


def check_disk_space():
    """Check if there's enough disk space (5-8GB)."""
    print("\n📊 Checking disk space...")

    try:
        disk = shutil.disk_usage(".")
        free_gb = disk.free / (1024**3)

        print(f"   Available: {free_gb:.1f} GB")

        if free_gb < 5:
            print(f"   ⚠️ Warning: Less than 5GB free space")
            print("      Some ML models may not download properly")
            return False
        else:
            print(f"   ✅ Disk space OK")
            return True
    except Exception as e:
        print(f"   ⚠️ Could not check disk space: {e}")
        return True


def check_ram():
    """Check if there's enough RAM (8GB minimum)."""
    print("\n🧠 Checking RAM...")

    try:
        import psutil

        ram_gb = psutil.virtual_memory().total / (1024**3)

        print(f"   Available: {ram_gb:.1f} GB")

        if ram_gb < 8:
            print(f"   ⚠️ Warning: Less than 8GB RAM")
            print("      Some tools may run slowly")
            return False
        else:
            print(f"   ✅ RAM OK")
            return True
    except ImportError:
        print("   ⚠️ Could not check RAM (psutil not installed)")
        return True


def get_tools_directory():
    """Prompt user for tools directory."""
    print("\n" + "-" * 60)
    print("📁 Tools Directory Configuration")
    print(f"   Default: {TOOLS_DIR}")

    tools_dir_input = input(
        "\nEnter tools directory path (press Enter for default): "
    ).strip()

    if not tools_dir_input:
        tools_dir = Path(TOOLS_DIR)
    else:
        tools_dir = Path(tools_dir_input).expanduser()

    # Create directory if it doesn't exist
    if not tools_dir.exists():
        create = (
            input(f"\nDirectory '{tools_dir}' does not exist. Create it? [Y/n]: ")
            .strip()
            .lower()
        )
        if create in ["", "y", "yes"]:
            try:
                tools_dir.mkdir(parents=True, exist_ok=True)
                print(f"   ✅ Created directory: {tools_dir}")
            except Exception as e:
                print(f"   ❌ Could not create directory: {e}")
                return None
        else:
            print("   ❌ Installation cancelled.")
            sys.exit(0)

    return tools_dir


def display_tools(tools_dir):
    """Display tools that will be installed."""
    print(f"\n📦 Tools in {tools_dir}:")

    py_files = list(tools_dir.glob("*.py"))
    py_files = [f for f in py_files if f.name != "__init__.py"]

    if py_files:
        for i, f in enumerate(sorted(py_files), 1):
            print(f"   {i}. {f.stem}")
    else:
        print("   (No tools found - you can add them later)")


def confirm_installation():
    """Confirm installation with user."""
    print("\n" + "-" * 60)
    confirm = input("Proceed with installation? [Y/n]: ").strip().lower()

    if confirm in ["n", "no"]:
        print("\n❌ Installation cancelled.")
        sys.exit(0)


def run_command(cmd, description):
    """Run a command and display progress."""
    print(f"\n🔄 {description}...")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed")
        print(f"   Error: {e.stderr}")
        return False


def upgrade_pip():
    """Upgrade pip to latest version."""
    return run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip"
    )


def install_dependencies():
    """Install dependencies from requirements.txt."""
    req_file = Path(__file__).parent.parent / "requirements.txt"
    if not req_file.exists():
        print(
            f"   ❌ requirements.txt not found at {req_file}. Cannot install dependencies."
        )
        return False

    return run_command(
        [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
        "Installing dependencies",
    )


def install_package():
    """Install axle package in editable mode."""
    result = run_command(
        [sys.executable, "-m", "pip", "install", "-e", "."], "Installing axle package"
    )

    # Ensure tools directory exists after installation
    if result:
        tools_dir = Path(__file__).parent.parent / "tools"
        if not tools_dir.exists():
            print(f"\n📁 Creating tools directory at: {tools_dir}")
            try:
                tools_dir.mkdir(parents=True, exist_ok=True)
                print(f"   ✅ Created tools directory")
                # Create __init__.py
                init_file = tools_dir / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# Axle tools directory\n")
                    print(f"   ✅ Created __init__.py")
            except Exception as e:
                print(f"   ⚠️ Could not create tools directory: {e}")
        else:
            print(f"\n📁 Tools directory exists at: {tools_dir}")

    return result


def download_spacy_model():
    """Download spaCy English model."""
    print("\n📥 Downloading spaCy model (en_core_web_sm)...")

    try:
        subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
            check=True,
            capture_output=True,
        )
        print("   ✅ spaCy model downloaded")
        return True
    except subprocess.CalledProcessError:
        print("   ⚠️ Could not download spaCy model")
        print(
            "      You can download it later: python -m spacy download en_core_web_sm"
        )
        return False


def verify_installation():
    """Verify that installation was successful."""
    print("\n" + "-" * 60)
    print("🧪 Verifying installation...")

    # Test axle command
    try:
        result = subprocess.run(["axle", "list"], capture_output=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ axle command works!")
        else:
            print("   ⚠️ axle command exists but may have issues")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("   ❌ axle command not found")
        print("      Make sure you ran: pip install -e .")
        return False

    return True


def display_success_message():
    """Display success message and next steps."""
    print("\n" + "=" * 60)
    print("✅ Installation Complete!")
    print("=" * 60)

    print("\n🚀 Quick Start:")
    print("   axle list              # See all available tools")
    print('   axle run 1 "your text"  # Run SEO keyword checker')
    print("   axle doctor            # Check your setup")
    print("   axle help              # See all commands")

    print("\n💡 Next Steps:")
    print("   1. Try the example commands above")
    print("   2. Read the documentation in docs/")
    print("   3. Add your own tools to the tools/ directory")

    print(COMMUNITY_FOOTER)


def main():
    """Main installation workflow."""
    try:
        # Welcome
        welcome_message()

        # Environment check (runs first, may exit)
        check_environment()

        # System checks
        checks_passed = True
        checks_passed &= check_python_version()
        checks_passed &= check_disk_space()
        checks_passed &= check_ram()

        if not checks_passed:
            response = (
                input("\n⚠️ Some system checks failed. Continue anyway? [Y/n]: ")
                .strip()
                .lower()
            )
            if response in ["n", "no"]:
                print("\n❌ Installation cancelled.")
                sys.exit(1)

        # Get tools directory
        tools_dir = get_tools_directory()
        if not tools_dir:
            sys.exit(1)

        # Display tools
        display_tools(tools_dir)

        # Confirm
        confirm_installation()

        # Installation steps
        success = True
        success &= upgrade_pip()
        success &= install_dependencies()
        success &= install_package()
        download_spacy_model()  # Non-critical

        if success:
            verify_installation()
            display_success_message()
        else:
            print(
                "\n❌ Installation encountered errors. Please check the output above."
            )
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
