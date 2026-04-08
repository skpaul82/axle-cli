# PyPI Publishing Guide

**Status**: Preparation for v1.0.0  
**Package Name**: TBD (axle likely taken, need alternative)  
**Current Version**: 0.1.0

---

## Overview

This guide covers publishing Axle to PyPI for simple `pip install axle` installation.

---

## Package Name Considerations

### Problem
The name "axle" is likely already taken on PyPI.

### Alternatives
- **axle-cli** - Follows Python convention (like pytest-py)
- **axle-cli** - Clear that it's a CLI tool
- **axle-platform** - Reflects platform positioning
- **axle-tools** - Emphasizes tool functionality
- **axle-runner** - Describes what it does

### Recommendation
**axle-cli** or **axle-cli**

Both are:
- Descriptive
- Likely available
- Follow Python naming conventions

---

## Pre-Publication Checklist

### 1. Update Package Name in pyproject.toml

```toml
[project]
name = "axle-cli"  # or "axle-cli"
```

### 2. Verify Metadata

Ensure `pyproject.toml` has:
- ✅ Unique package name
- ✅ Version (0.1.0)
- ✅ Description
- ✅ Long description (README.md)
- ✅ Author email (hello@skpaul.me)
- ✅ License (MIT)
- ✅ Classifiers
- ✅ Dependencies
- ✅ Entry points (axle = scripts.axle:main)

### 3. Test Build Locally

```bash
# Install build tools
pip install build twine

# Build distribution packages
python -m build

# Check generated files
ls -lh dist/
# Should see:
#   axle-cli-0.1.0.tar.gz
#     axle_cli-0.1.0-py3-none-any.whl
```

### 4. Test Installation

```bash
# Create test virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from local build
pip install dist/axle_cli-0.1.0-py3-none-any.whl

# Test it works
axle --help
axle list
axle security

# Cleanup
deactivate
rm -rf test_env
```

### 5. Check for Common Issues

```bash
# Check package structure
python -m twine check dist/*

# Should show: "PASSED" with no warnings
```

---

## Publishing to PyPI

### Step 1: Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create account
3. Enable 2FA (required for publishing)
4. Generate API token:
   - Account settings → API tokens → Add API token
   - Scope: "Entire account" (for new project)
   - Copy token (save it securely!)

### Step 2: Configure Twine

```bash
# Create .pypirc
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-api-token-here>

[testpypi]
username = __token__
password = <your-testpypi-api-token-here>
EOF

chmod 600 ~/.pypirc
```

### Step 3: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ axle-cli

# Verify it works
axle --help
```

### Step 4: Publish to PyPI

```bash
# Once satisfied with TestPyPI, publish to PyPI
python -m twine upload dist/*
```

### Step 5: Verify Installation

```bash
# Create fresh virtual environment
python -m venv verify_env
source verify_env/bin/activate

# Install from PyPI
pip install axle-cli

# Test all commands
axle --help
axle list
axle security
axle run 1 "test"
axle scan
axle doctor

# Cleanup
deactivate
rm -rf verify_env
```

---

## Post-Publication

### Update README

Add PyPI badge and install instructions:

```markdown
[![PyPI version](https://badge.fury.io/py/axle-cli.svg)](https://badge.fury.io/py/axle-cli)
[![Python versions](https://img.shields.io/pypi/pyversions/axle-cli.svg)](https://pypi.org/project/axle-cli/)

## 🚀 Quick install

```bash
pip install axle-cli
```
```

### Update Documentation

- Add PyPI link to community footer
- Update installation guide with PyPI method
- Update contribution guide with version bumping

### Monitor Downloads

Check download stats:
- https://pypistats.org/packages/axle-cli

---

## Version Management

### Release Process

1. Update version in `pyproject.toml`
2. Update `docs/changelog.md`
3. Commit changes
4. Tag release:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```
5. Build and publish:
   ```bash
   rm -rf dist/ build/
   python -m build
   python -m twine upload dist/*
   ```

### Version Numbering

Follow Semantic Versioning: MAJOR.MINOR.PATCH

- **0.1.0** → **0.1.1**: Bug fixes
- **0.1.0** → **0.2.0**: New features
- **0.1.0** → **1.0.0**: Production release

---

## Maintenance

### Update Published Package

If you need to yank (remove) a version:

```bash
# From PyPI web interface:
# 1. Go to https://pypi.org/manage/project/axle-cli/releases/
# 2. Yank the version
# 3. Provide reason
```

### Handle Name Conflicts

If "axle-cli" is taken:

1. Try alternatives:
   - `axle-cli`
   - `axle-platform`
   - `axle-runner`
   - `axle-cmd`

2. Update `pyproject.toml` with new name
3. Rebuild and republish

---

## Troubleshooting

### Issue: Package name already taken

**Solution**: Use alternative name (see above)

### Issue: Upload fails with 403 Forbidden

**Solution**: 
- Verify API token is correct
- Check token has "Entire account" scope
- Regenerate token if needed

### Issue: Package doesn't install correctly

**Solution**:
- Check `pyproject.toml` configuration
- Verify all files are included in package
- Test with `pip install -e .` locally first

### Issue: Long description not showing

**Solution**:
- Ensure README.md is valid Markdown
- Check Content-Type in pyproject.toml
- May need to use `long_description_content_type="text/markdown"`

---

## Recommendations

### For v0.1.0
- **Status**: Use GitHub install method
- **Reason**: Get feedback, iterate on features
- **Command**: `pip install git+https://github.com/skpaul82/axle-cli.git`

### For v1.0.0
- **Status**: Publish to PyPI
- **Package name**: axle-cli (or available alternative)
- **Command**: `pip install axle-cli`
- **Reason**: Production-ready, wider audience

---

## Timeline

| Version | Date | PyPI Status |
|---------|------|-------------|
| 0.1.0 | Apr 2026 | ❌ Not published (GitHub install) |
| 0.2.0 | Q2 2026 | ❌ Planned (GitHub install) |
| 0.3.0 | Q3 2026 | ❌ Planned (GitHub install) |
| 1.0.0 | Q4 2026 | ✅ Planned (PyPI publish) |

---

## Resources

- [PyPI Publishing Tutorial](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Best Practices](https://pypi.org/help/)
- [TestPyPI](https://test.pypi.org/)

---

**Status**: Ready for preparation  
**Next Step**: Choose package name and test build  
**Maintained By**: Sanjoy K. Paul  
**Date**: 2026-04-08
