# Installation Guide

This guide will help you install Axle on your system.

## System Requirements

### Minimum Requirements

- **Python**: 3.10 or higher
- **RAM**: 8GB
- **Disk Space**: 5GB free
- **Operating System**: macOS, Linux, or Windows

### Recommended Requirements

- **Python**: 3.10 or higher
- **RAM**: 16GB
- **Disk Space**: 8GB free
- **Operating System**: macOS or Linux

## Check Python Version

First, verify you have Python 3.10+ installed:

```bash
python --version
# or
python3 --version
```

You should see something like `Python 3.10.0` or higher.

If you need to install Python, download it from [python.org](https://www.python.org/downloads/).

## Installation Methods

### Method 1: Install from GitHub (Recommended) ✨

The easiest way to install Axle is directly from GitHub:

```bash
pip install git+https://github.com/skpaul82/axle-cli.git
```

That's it! You can now run:

```bash
axle list
axle run 1 "your prompt"
axle security
```

**Advantages**:
- ✅ Single command installation
- ✅ Always gets the latest version
- ✅ No manual dependency management
- ✅ Works on all platforms

### Method 2: Interactive Installation

The interactive installer guides you through the setup process:

```bash
python -m axle.install_axle
```

The installer will:
1. **Environment check**: Validates Python version, pip availability, and package installation capability
2. **System requirements**: Checks RAM, disk space, and dependencies
3. **Install dependencies**: Installs all required packages
4. **Set up the `axle` command**: Installs the package in editable mode
5. **Download required ML models**: Downloads spaCy models
6. **Verify the installation**: Confirms everything works

**Enhanced Environment Checking**:
- Runs comprehensive validation at the start
- Provides FAQ links when requirements aren't met
- Offers common solutions for known issues
- Allows you to continue or exit if problems are found

### Method 3: Manual Installation

If you prefer manual installation or need more control:

#### Step 1: Upgrade pip

```bash
pip install --upgrade pip
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including pandas, scikit-learn, spaCy, and more.

#### Step 3: Install the Package

```bash
pip install -e .
```

The `-e` flag installs in "editable" mode, which means you can modify the code and changes will take effect immediately.

#### Step 4: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

## Verification

After installation, verify everything works:

```bash
axle list
```

You should see a list of available tools.

```bash
axle doctor
```

This will run diagnostics to check your environment.

## Platform-Specific Instructions

### macOS

On macOS, you might need to use `python3` instead of `python`:

```bash
python3 -m axle.install_axle
```

Or create an alias:

```bash
alias python='python3'
alias pip='pip3'
```

### Linux

On Linux, you may need to install system dependencies first:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-pip python3-venv
```

### Windows

On Windows, use the Python launcher:

```bash
py -m axle.install_axle
```

Or use `python`:

```bash
python -m axle.install_axle
```

## Virtual Environment (Recommended)

It's highly recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install Axle
pip install -r requirements.txt
pip install -e .
```

## Troubleshooting

### "Command not found: axle"

If you get this error, the installation may not have set up the command properly. Try:

1. Make sure you ran `pip install -e .`
2. Check your PATH includes the pip scripts directory
3. Try running with python: `python -m axle.axle list`
4. Check the package is installed: `pip show axle-cli`

### "ModuleNotFoundError"

If you get import errors:

1. Make sure you installed dependencies: `pip install -r requirements.txt`
2. Check you're using the right Python environment
3. Try reinstalling: `pip install -e .`

### spaCy Model Download Fails

If the spaCy model download fails:

1. Check your internet connection
2. Try downloading manually: `python -m spacy download en_core_web_sm`
3. If it persists, the tool may still work (with reduced functionality)

### Disk Space Issues

If you're low on disk space:

1. Clean pip cache: `pip cache purge`
2. Remove virtual environments you don't need
3. Consider using lighter alternatives for ML models

## Uninstallation

To remove Axle while preserving your tools directory:

```bash
axle uninstall
# Then follow the prompts
pip uninstall axle-cli
```

To remove Axle and the tools directory:

```bash
axle uninstall --remove-tools
# Then follow the prompts
pip uninstall axle-cli
```

The uninstall command:
- Shows what will be removed
- Preserves tools directory by default
- Provides clear instructions for pip uninstall
- Shows reinstallation steps if tools are preserved

To remove the virtual environment (if you created one):

```bash
# Deactivate first
deactivate

# Remove the directory
rm -rf venv
```

## Next Steps

After installation:

1. Read the [Usage Guide](usage.md) to learn how to use the tools
2. Run `axle list` to see available tools
3. Try `axle run 1 "test"` to test a tool
4. Check out the [Command Reference](commands.md) for all commands

## Need Help?

If you encounter issues not covered here:

1. Check the [Troubleshooting](troubleshooting.md) guide
2. Search existing GitHub issues
3. Create a new issue on GitHub
4. Reach out on social media (links in README)
