# Axle Code Review System

## Overview

Axle CLI includes an automatic code review and fixing system that helps you maintain high code quality across all your tools. The system automatically checks for common issues and can fix many of them before they reach your CI/CD pipeline.

## Features

- **Automatic Code Review**: Runs every time you execute a tool (in auto mode)
- **Auto-Fixing**: Automatically fixes formatting and import issues
- **Clear Feedback**: Shows exactly what's wrong and how to fix it
- **Non-Blocking**: Won't stop your workflow by default
- **Manual Review**: Run code reviews anytime with `axle review`

## How It Works

The code review system runs in two phases:

1. **Security Validation** (existing): Checks for security issues
2. **Code Review** (new): Checks for code quality issues

### Issue Categories

The system detects issues in four categories:

- **FORMATTING**: Black formatting issues (line length, spacing, etc.)
- **IMPORTS**: isort import sorting issues
- **LINTING**: flake8 code quality issues
- **COMPLEXITY**: High code complexity warnings

### Severity Levels

- 🔴 **CRITICAL**: Syntax errors, undefined names (must fix)
- 🟠 **HIGH**: Major issues that should be fixed
- 🟡 **MEDIUM**: Important but not blocking
- 🟢 **LOW**: Minor issues (style, unused imports, etc.)

## Usage

### Automatic Review (Default)

When you run a tool, code review happens automatically:

```bash
axle run my_tool "prompt"
```

**Example Output:**
```
🔒 Validating tool security...
   Security Policy: WARN
   ✅ Security validation passed

🔍 Running automatic code review...
   Found 2 code quality issue(s):

   🟡 MEDIUM [FORMATTING] Line 14: Black formatting issues
      💡 Can auto-fix: black <file>

   🟢 LOW [IMPORTS] Line 4: Imports not sorted correctly
      💡 Can auto-fix: isort <file>

   📋 Apply 2 automatic fix(es)? [Y/n]:
```

### Manual Review

Review a specific tool:

```bash
axle review my_tool
```

Review all tools:

```bash
axle review --all
```

Review with automatic fixes:

```bash
axle review my_tool --fix
```

Show what would be fixed (dry run):

```bash
axle review my_tool --fix --dry-run
```

Detailed output:

```bash
axle review my_tool --verbose
```

## Configuration

### Environment Variables

Control code review behavior with environment variables:

```bash
# When to run code review: always, auto (default), or never
export AXLE_CODE_REVIEW=auto

# Automatically fix issues without asking
export AXLE_AUTO_FIX=false

# Enable detailed output
export AXLE_CODE_REVIEW_VERBOSE=false
```

### Configuration File

Create a `.axlerc` file in your project root:

```ini
[code_review]
enabled = true
auto_fix = false
show_skipped = true
max_complexity = 10
```

## Code Review Modes

### Auto Mode (Default)

Runs code review on recently modified files (within last hour).

```bash
export AXLE_CODE_REVIEW=auto
```

### Always Mode

Runs code review every time, regardless of file modification time.

```bash
export AXLE_CODE_REVIEW=always
```

### Never Mode

Disables automatic code review completely.

```bash
export AXLE_CODE_REVIEW=never
```

## Auto-Fixing

### What Gets Auto-Fixed

The system can automatically fix:

- ✅ **Black formatting**: All Python code style issues
- ✅ **isort imports**: Import statement ordering
- ✅ **Unused imports**: Safe to remove
- ✅ **Unused variables**: Safe to remove (with backup)

### What Requires Manual Fixing

These issues need your attention:

- ❌ **Syntax errors**: Code structure issues
- ❌ **Undefined names**: Missing imports or typos
- ❌ **Line length**: May require code restructuring
- ❌ **Complexity**: High complexity functions

### Auto-Fix Safety

The auto-fix system includes safety features:

1. **Backup Creation**: Creates `.backup` files before modifying
2. **Validation**: Checks that fixes didn't break the file
3. **Rollback**: Restores backup if something goes wrong
4. **Never Silent**: Always shows what was changed

## Best Practices

### For New Users

Enable auto-fix for seamless experience:

```bash
export AXLE_AUTO_FIX=true
export AXLE_CODE_REVIEW=always
```

### For Development

Use review mode to see issues:

```bash
export AXLE_AUTO_FIX=false
export AXLE_CODE_REVIEW=auto
```

### For CI/CD

Fail on any issues:

```bash
export AXLE_CODE_REVIEW=always
export AXLE_AUTO_FIX=false
```

## Troubleshooting

### "flake8 not found"

Install development dependencies:

```bash
pip install black isort flake8
```

Or add to your requirements:

```bash
pip install -r requirements.txt
```

### "Could not run Black/isort/flake8"

The code reviewer will skip tools that aren't available. Install them for full functionality:

```bash
pip install black isort flake8
```

### Too Many Issues

If you see many issues, run the automatic fixes first:

```bash
axle review my_tool --fix
```

Then address remaining manual issues.

### Code Review Slowing Down Workflow

Disable automatic review for faster iteration:

```bash
export AXLE_CODE_REVIEW=never
```

Then run manual reviews when needed:

```bash
axle review --all
```

## Integration with CI/CD

The code review system complements your existing CI/CD:

### Before CI

Catch issues locally before pushing:

```bash
axle review --all --fix
```

### In CI

Your CI pipeline already runs these checks, but now you'll catch them first.

### After CI

If CI fails, use the same tools locally:

```bash
black axle/ tools/
isort axle/ tools/
```

## Advanced Usage

### Reviewing Specific Files

Use the code reviewer module directly:

```bash
python -m axle.code_reviewer my_file.py --fix
```

### JSON Output

Get machine-readable output:

```bash
python -m axle.code_reviewer my_file.py --json
```

### Batch Processing

Review multiple files:

```bash
python -m axle.code_reviewer file1.py file2.py file3.py --fix
```

## Contributing

When contributing tools to Axle:

1. **Run code review** before submitting:
   ```bash
   axle review --all --fix
   ```

2. **Check CI results**: Fix any remaining issues

3. **Test your tools**: Ensure they work after fixes

4. **Document**: Add any special requirements

## Examples

### Creating a New Tool

```bash
# Create your tool
cat > tools/my_new_tool.py << 'EOF'
import sys
def get_description():
    return "My new tool"

def main(prompt):
    print(f"Processing: {prompt}")
EOF

# Run it - code review will trigger automatically
axle run my_new_tool "test"

# Fix any issues found
axle review my_new_tool --fix
```

### Fixing All Tools

```bash
# Review all tools and fix what we can
axle review --all --fix

# See what's left to fix manually
axle review --all
```

### Pre-Commit Check

Before committing:

```bash
# Quick check
axle review --all

# If clean, commit
git add .
git commit -m "My changes"
```

## Support

If you encounter issues:

1. Check this documentation first
2. Run with `--verbose` flag for more details
3. Check the GitHub Issues
4. Ask in the community forum

## Future Enhancements

Planned improvements:

- [ ] Pre-commit hook integration
- [ ] Configuration file support (.axlerc)
- [ ] More sophisticated auto-fixing
- [ ] Performance optimizations
- [ ] Integration with more linters
- [ ] Code complexity visualization
