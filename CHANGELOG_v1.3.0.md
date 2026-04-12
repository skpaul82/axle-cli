# Changelog v1.3.0 - Direct Tool Commands & Simplified Help

**Release Date**: 2026-04-12

## 🎉 Major Features

### 1. **Direct Tool Commands**
Tools can now be run directly as axle commands without the `run` keyword:

**Before:**
```bash
axle run competitor_analysis --urls url1 url2 --target-keyword "keyword"
axle run content_optimizer --url https://example.com
```

**After:**
```bash
axle competitor_analysis --urls url1 url2 --target-keyword "keyword"
axle content_optimizer --url https://example.com
```

### 2. **Simplified Help System**
Tool help is now cleaner and more user-friendly:

**Before:** Showed all functions, classes, signatures
**After:** Shows name, summary, and examples only

```bash
$ axle help competitor_analysis

============================================================
Tool: competitor_analysis
============================================================

SERP & Competitor Content Analysis

📌 Examples:
  axle competitor_analysis --urls https://comp1.com https://comp2.com --target-keyword "web developer"
  axle competitor_analysis --files comp1.html comp2.html comp3.html --target-keyword "crm software"

  axle help competitor_analysis --details   # full options & function list
```

### 3. **Interactive Mode**
Running `axle` with no arguments launches an interactive arrow-key menu:

```bash
$ axle
# Interactive tool picker with arrow keys
```

### 4. **Smart Help Extraction**
- Automatically extracts usage examples from tool docstrings
- Converts `python tool.py` examples to `axle tool` format
- Shows argparse options with `--details` flag

## 📋 All Changes

### axle/axle.py

**Version Update:**
- Updated from `1.2.0` to `1.3.0`

**New Features:**
1. **Interactive Mode** (lines 1182-1215)
   - Detects when axle is run with no args in a terminal
   - Launches interactive arrow-key picker
   - Handles all tool types appropriately

2. **Direct Tool Command Routing** (lines 1220-1271)
   - Checks if command is a tool before argparse validation
   - Routes to appropriate handler based on tool type
   - Shows help when no args provided
   - Passes arguments through to tools

3. **Enhanced Examples in Main Help** (lines 1277-1299)
   - Added comprehensive examples section
   - Shows both command names and numbers
   - Covers all tool types

**Tool Type Handling:**
- **Argparse-based tools**: Show help, then run with sys.argv manipulation
- **Contract tools**: Show help, then run with prompt
- **Multi-function tools**: Detect function name, pass remaining args

### axle/tool_discoverer.py

**New Methods:**

1. **`get_docstring_examples()`** (lines 160-192)
   - Extracts `Usage:` section from module docstring
   - Converts `python tool.py` to `axle tool` format
   - Returns list of example commands

2. **`get_argparse_help()`** (lines 194-230)
   - Captures argparse `--help` output
   - Replaces `usage: tool` with `usage: axle tool`
   - Returns formatted help text

**Enhanced Methods:**

1. **`get_help_text(verbose=False)`** (lines 232-295)
   - **Default mode**: Shows name, summary, examples only
   - **Verbose mode**: Shows full argparse help + function list
   - Auto-extracts examples from docstrings
   - Cleaner, more user-friendly output

**Key Improvements:**
- Examples auto-extracted from docstrings
- One-line summaries instead of full descriptions
- `--details` flag for full information
- No more overwhelming function lists by default

## 🎯 Usage Examples

### Running Tools Directly

```bash
# Argparse-based tool
axle competitor_analysis --urls url1 url2 --target-keyword "keyword"

# Contract-based tool
axle seo_keyword_checker "python programming tutorial"

# Multi-function tool
axle example_simple_calculator add 5 3
```

### Getting Help

```bash
# Simple help (default)
axle help competitor_analysis

# Detailed help with all options
axle help competitor_analysis --details
# or
axle help competitor_analysis --verbose

# Interactive mode
axle
```

### Interactive Tool Selection

```bash
$ axle
# Launches arrow-key interface to select and run tools
```

## 🔄 Backward Compatibility

All old usage patterns still work:

```bash
# Old way still works
axle run competitor_analysis --urls url1 url2
axle run seo_keyword_checker "prompt"
axle list
axle help tool_name
```

## 📊 Comparison

| Feature | v1.2.0 | v1.3.0 |
|---------|-------|-------|
| **Tool Invocation** | `axle run <tool>` | `axle <tool>` ✨ |
| **Help Output** | All functions listed | Name + examples only ✨ |
| **Interactive Mode** | ❌ No | ✅ Yes ✨ |
| **Example Extraction** | ❌ Manual | ✅ Automatic ✨ |
| **Argparse Integration** | Basic | Full help capture ✨ |

## 🐛 Bug Fixes

1. Fixed argparse conflict in run command (renamed `command` to `func`)
2. Fixed type conversion for function arguments
3. Fixed interactive mode fallback on errors

## 📚 Documentation Updates

- Created `CHANGELOG_v1.3.0.md` (this file)
- Updated `INTELLIGENT_DISCOVERY.md` with new features
- Enhanced in-CLI help examples
- Added `--details` flag documentation

## 🚀 Performance

- Tool discovery: Still < 100ms
- Help generation: Optimized with example extraction
- Interactive mode: Fast startup with lazy loading

## 🎨 User Experience Improvements

### Before
```bash
$ axle help content_optimizer

============================================================
Tool: content_optimizer
File: content_optimizer.py
============================================================

Content Optimization & SEO Scoring

Content Optimization & SEO Scoring
====================================
Analyzes content for SEO quality...

📋 Available Functions:
  • compute_seo_score(<structure> <readability>...)
    Compute a weighted SEO score (0-100).
  • count_syllables(<word>)
    Rough syllable count...
  • extract_entities(<text>)
    Extract named entities...
  • main() 🔴 MAIN
  • print_report(...)
    Print the SEO analysis report.
  • readability_scores(<text>)
    Compute Flesch-Kincaid...
  • tfidf_keyword_analysis(...)
    Analyze keyword coverage...

💡 Usage: axle run content_optimizer
   Note: This tool uses its own CLI interface...
   Or: python content_optimizer.py --help
```

### After
```bash
$ axle help content_optimizer

============================================================
Tool: content_optimizer
============================================================

Content Optimization & SEO Scoring

📌 Examples:
  axle content_optimizer --url https://example.com/page --target-keyword "project management tools"
  axle content_optimizer --file article.html --target-keyword "cloud hosting" --competitors comp1.html comp2.html
  axle content_optimizer --text "Your content here..." --target-keyword "best crm software"

  axle help content_optimizer --details   # full options & function list
```

Much cleaner! 🎉

## 🔮 Future Enhancements

Planned for v1.4.0:
- [ ] Tool aliases (short names)
- [ ] Tool categories/tags
- [ ] Search tools by functionality
- [ ] Tool configuration files
- [ ] Shell completion scripts

## 📦 Migration Guide

### For Users

**No changes needed!** All old commands still work. New commands are optional shortcuts.

### For Tool Developers

**No changes needed!** Tools work automatically with new system.

**Optional enhancements:**
- Add `Usage:` section to docstring for auto-example extraction
- Use standard argparse for consistent help integration

**Example enhanced docstring:**
```python
"""
My Tool - Does something useful

More detailed description here...

Usage:
    python my_tool.py --input file.txt --output result.txt
    python my_tool.py --url https://example.com --verbose
"""
```

This will automatically become:
```
📌 Examples:
  axle my_tool --input file.txt --output result.txt
  axle my_tool --url https://example.com --verbose
```

## ✅ Testing

All features tested with:
- ✅ Argparse-based tools (competitor_analysis, content_optimizer, etc.)
- ✅ Contract-based tools (01_seo_keyword_checker, etc.)
- ✅ Multi-function tools (example_simple_calculator)
- ✅ Interactive mode
- ✅ Help system (simple and verbose modes)
- ✅ Direct tool commands
- ✅ Backward compatibility

## 🙏 Acknowledgments

Built with community feedback to make Axle more intuitive and powerful.

---

**Version**: 1.3.0
**Release Date**: 2026-04-12
**Status**: ✅ Production Ready
