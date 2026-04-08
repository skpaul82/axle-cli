# Troubleshooting Guide

Solutions to common problems when using Buddy Tools.

## Installation Issues

### "Command not found: buddy"

**Problem:** After installation, the `buddy` command is not recognized.

**Solutions:**

1. **Verify Installation:**
   ```bash
   pip show buddy-tools
   ```
   If not installed, run:
   ```bash
   pip install -e .
   ```

2. **Check Python Scripts Directory:**
   ```bash
   python -m site --user-site
   python -m site --user-base
   ```
   Ensure the user base's `bin` directory is in your PATH.

3. **Try Python Module Invocation:**
   ```bash
   python -m scripts.buddy list
   ```

4. **Edit Mode Verification:**
   Make sure you installed with `-e` flag:
   ```bash
   pip install -e .
   ```

### "ModuleNotFoundError: No module named 'X'"

**Problem:** Import errors for required packages.

**Solutions:**

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation:**
   ```bash
   pip list | grep package-name
   ```

3. **Reinstall Package:**
   ```bash
   pip uninstall buddy-tools
   pip install -e .
   ```

4. **Virtual Environment:**
   Make sure you're in the correct virtual environment:
   ```bash
   which python
   ```

### "Permission denied" when installing

**Problem:** Can't install packages due to permissions.

**Solutions:**

1. **Use Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

2. **User Install Flag:**
   ```bash
   pip install --user -e .
   ```

3. **macOS/Linux - Use sudo** (not recommended):
   ```bash
   sudo pip install -e .
   ```

### spaCy Model Download Fails

**Problem:** Cannot download en_core_web_sm model.

**Solutions:**

1. **Check Internet Connection:**
   ```bash
   curl -I https://github.com
   ```

2. **Try Alternative Download Method:**
   ```bash
   python -m spacy download en_core_web_sm --direct
   ```

3. **Manual Download:**
   ```bash
   wget https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0-py3-none-any.whl
   pip install en_core_web_sm-3.0.0-py3-none-any.whl
   ```

4. **Skip Model:**
   The tools may still work with reduced functionality.

## Tool Execution Issues

### "Tool not found" Error

**Problem:** Tool identifier doesn't match any available tools.

**Solutions:**

1. **List Available Tools:**
   ```bash
   buddy list
   ```

2. **Use Number Instead:**
   ```bash
   buddy run 1 "your prompt"
   ```

3. **Check Tool File:**
   Verify the `.py` file exists in `tools/` directory:
   ```bash
   ls -la tools/
   ```

### Tool Produces No Output

**Problem:** Tool runs but produces empty or minimal output.

**Solutions:**

1. **Provide a Prompt:**
   ```bash
   buddy run 1 "your actual text here"
   ```

2. **Check Tool Requirements:**
   Some tools need specific input (URL for meta_tag_auditor).

3. **Verbose Mode:**
   Run with python directly to see errors:
   ```bash
   python -c "import tools.tool_name; tools.tool_name.main('test')"
   ```

### Tool Execution is Slow

**Problem:** Tools take a long time to run.

**Causes and Solutions:**

1. **First Run:** ML models load on first run. Subsequent runs are faster.

2. **Large Input:** Processing large files takes time. Try smaller samples first.

3. **Network Requests:** Tools that fetch URLs depend on network speed.

4. **System Resources:**
   ```bash
   buddy doctor
   ```
   Check RAM and disk space.

### "ImportError" in Tool

**Problem:** Tool fails to import required modules.

**Solutions:**

1. **Install Missing Dependencies:**
   ```bash
   pip install missing-package
   ```

2. **Reinstall All Dependencies:**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check Python Path:**
   ```bash
   python -c "import sys; print(sys.path)"
   ```

## Performance Issues

### High Memory Usage

**Problem:** Buddy Tools uses excessive memory.

**Solutions:**

1. **Check Memory Usage:**
   ```bash
   buddy doctor
   ```
   Verify you have at least 8GB RAM.

2. **Close Other Applications:** Free up memory.

3. **Use Lighter Models:** Some ML models have smaller alternatives.

4. **Process Smaller Files:** Break large inputs into smaller chunks.

### Slow Startup

**Problem:** `buddy` command takes time to start.

**Solutions:**

1. **First Run:** Initial startup is slower. Subsequent runs are faster.

2. **Edit Mode:** If installed in edit mode, Python checks for file changes.

3. **PATH Issues:** Large PATH can slow down command lookup.

## Dependency Conflicts

### Version Conflicts

**Problem:** Other packages require different versions of dependencies.

**Solutions:**

1. **Use Virtual Environment:** Isolate Buddy Tools dependencies.

2. **Check Conflicts:**
   ```bash
   pip check
   ```

3. **Update Conflicting Packages:**
   ```bash
   pip install --upgrade conflicting-package
   ```

### pip Install Fails

**Problem:** Cannot install due to dependency conflicts.

**Solutions:**

1. **Force Reinstall:**
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

2. **Ignore Installed:**
   ```bash
   pip install -I -r requirements.txt
   ```

3. **Create Fresh Environment:**
   ```bash
   python -m venv fresh_env
   source fresh_env/bin/activate
   pip install -r requirements.txt
   ```

## Platform-Specific Issues

### macOS

**Problem:** Various macOS-specific issues.

**Solutions:**

1. **Use python3:**
   ```bash
   python3 scripts/install_buddy.py
   ```

2. **Xcode Command Line Tools:**
   ```bash
   xcode-select --install
   ```

3. **Rosetta (Apple Silicon):**
   ```bash
   softwareupdate --install-rosetta
   ```

### Windows

**Problem:** Path separators, command differences.

**Solutions:**

1. **Use py Launcher:**
   ```bash
   py scripts/install_buddy.py
   ```

2. **Path Separators:**
   Use forward slashes in Python:
   ```python
   path = "tools/file.py"  # Not "tools\file.py"
   ```

3. **PowerShell Execution Policy:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Linux

**Problem:** Missing system dependencies.

**Solutions:**

1. **Install System Dependencies:**
   ```bash
   sudo apt-get install python3-dev build-essential  # Ubuntu/Debian
   sudo dnf install python3-devel gcc  # Fedora
   ```

2. **Permissions:**
   Don't use sudo with pip. Use virtual environments instead.

## Getting Help

### Still Having Issues?

1. **Check Diagnostics:**
   ```bash
   buddy doctor
   ```
   Run this and include the output when asking for help.

2. **Enable Debug Mode:**
   ```bash
   python -m scripts.buddy --verbose
   ```

3. **Check Logs:**
   Look for error messages in terminal output.

4. **Search Existing Issues:**
   Check GitHub Issues for similar problems.

5. **Create an Issue:**
   When creating an issue, include:
   - Your operating system
   - Python version (`python --version`)
   - Buddy Tools version (`pip show buddy-tools`)
   - Full error message
   - Steps to reproduce
   - Output of `buddy doctor`

### Community Resources

- **GitHub:** https://github.com/skpaul82/axle-py
- **X/Twitter:** [@_skpaul82](https://x.com/_skpaul82)
- **Instagram:** [skpaul82](https://instagram.com/skpaul82)
- **Newsletter:** [axle.sanjoypaul.com/agent-aio](https://axle.sanjoypaul.com/agent-aio)

## Reporting Bugs

When reporting bugs, provide:

1. **Description:** Clear description of the problem
2. **Steps:** How to reproduce the issue
3. **Expected:** What you expected to happen
4. **Actual:** What actually happened
5. **Environment:** OS, Python version, Buddy Tools version
6. **Logs:** Full error traceback
7. **Doctor Output:** Run `buddy doctor` and include output

## Feature Requests

We welcome feature requests!

1. Check if the feature already exists
2. Search existing feature requests
3. Describe the use case clearly
4. Explain why it's important
5. Suggest a possible implementation (optional)
