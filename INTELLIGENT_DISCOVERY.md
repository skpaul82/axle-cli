# 🔍 Intelligent Tool Discovery System

**Axle v1.2.0+** includes an intelligent tool discovery system that allows you to run **ANY Python script** through the Axle CLI without requiring modifications or specific contracts.

## 🎯 What This Means

Simply drop any Python script into the `tools/` directory, and Axle will:
- ✅ **Automatically discover** all functions, classes, and their signatures
- ✅ **Extract docstrings** and usage information
- ✅ **Intelligently convert** CLI arguments to proper Python types
- ✅ **Support multiple interfaces**: contract-based, argparse-based, or function-based
- ✅ **Provide detailed help** for all available functions

## 📋 Tool Types

Axle intelligently handles three types of Python tools:

### 1. **Axle Contract Tools** (✅ Badge)
Traditional Axle tools that implement the standard contract:
```python
def get_description() -> str:
    return "Tool description"

def main(prompt: str) -> None:
    # Tool logic
    pass
```

**Usage**: `axle run <tool> "prompt text"`

### 2. **Argparse-Based Tools** (📜 Badge + "argparse-based" label)
Standalone Python scripts with their own CLI interface using argparse:
```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to analyze")
    args = parser.parse_args()
    # Tool logic
```

**Usage**: `axle run <tool>` (tool's own CLI interface)

### 3. **Multi-Function Tools** (📜 Badge)
Python scripts with multiple functions that can be called individually:
```python
def add(a: float, b: float) -> float:
    return a + b

def multiply(a: float, b: float) -> float:
    return a * b
```

**Usage**: `axle run <tool> <function> <arg1> <arg2>`

## 🚀 Usage Examples

### Listing All Tools
```bash
$ axle list

🔧 Discovering tools...
============================================================

Found 8 tool(s):

  1. ✅ 01_seo_keyword_checker - SEO Keyword Checker
     🔴 Main: main
     💡 axle help 01_seo_keyword_checker
  2. 📜 competitor_analysis - SERP & Competitor Content Analysis
     🔴 Main: main (argparse-based tool)
     💡 axle help competitor_analysis
  3. 📜 example_simple_calculator - A simple calculator tool
     🔴 Main: main (argparse-based tool)
     💡 axle help example_simple_calculator
```

### Getting Tool Help
```bash
$ axle help example_simple_calculator

============================================================
Tool: example_simple_calculator
============================================================

A simple calculator tool - demonstrates Axle's intelligent discovery.

📋 Available Functions:
  • add(<a> <b>)
    Add two numbers together.
  • divide(<a> <b>)
    Divide a by b.
  • main() 🔴 MAIN
    Main calculator function - runs an interactive calculator.
  • multiply(<a> <b>)
    Multiply two numbers.

💡 Usage: axle run example_simple_calculator

💡 Other functions:
   • axle run example_simple_calculator add <a> <b>
   • axle run example_simple_calculator divide <a> <b>
   • axle run example_simple_calculator multiply <a> <b>
```

### Running Different Tool Types

#### 1. Contract-based tool
```bash
axle run 01_seo_keyword_checker "python programming tutorial"
```

#### 2. Argparse-based tool
```bash
# Just run it - Axle will call its main() and let argparse handle it
axle run content_optimizer

# Or run it directly with Python to see its options
python tools/content_optimizer.py --help
```

#### 3. Multi-function tool
```bash
# Run specific function with arguments
axle run example_simple_calculator add 5 3
# Output: ✅ Result: 8.0

axle run example_simple_calculator multiply 4 7
# Output: ✅ Result: 28.0

# Run main function (interactive)
axle run example_simple_calculator
```

## 🎨 Creating Your Own Tools

### Option 1: Simple Multi-Function Tool
Just create a Python file with functions:
```python
# tools/my_calculations.py

def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price."""
    return price * (1 - discount_percent / 100)

def calculate_tax(price: float, tax_rate: float) -> float:
    """Calculate tax amount."""
    return price * tax_rate / 100
```

**Use it**:
```bash
axle run my_calculations calculate_discount 100 20
# Output: ✅ Result: 80.0
```

### Option 2: Interactive Tool with Main
```python
# tools/my_interactive_tool.py

def main():
    """Run interactive interface."""
    print("Welcome to my tool!")
    # Your interactive logic here
```

**Use it**:
```bash
axle run my_interactive_tool
```

### Option 3: Argparse-Based Tool
```python
# tools/my_cli_tool.py

def main():
    parser = argparse.ArgumentParser(description="My CLI Tool")
    parser.add_argument("--input", help="Input file")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()
    # Your logic here
```

**Use it**:
```bash
axle run my_cli_tool
# Note: Use python tools/my_cli_tool.py --help to see options
```

### Option 4: Axle Contract Tool
```python
# tools/my_axle_tool.py

def get_description() -> str:
    return "My tool description"

def main(prompt: str) -> None:
    # Your logic here
    print(f"Processing: {prompt}")
```

**Use it**:
```bash
axle run my_axle_tool "some prompt"
```

## 🔧 Features

### Smart Type Conversion
Axle automatically converts CLI string arguments to proper Python types based on function signatures:

```python
def process_data(count: int, rate: float, enabled: bool) -> str:
    return f"Count: {count}, Rate: {rate}, Enabled: {enabled}"
```

```bash
$ axle run my_tool process_data 10 2.5 true
# Output: Count: 10, Rate: 2.5, Enabled: True
```

### Automatic Function Discovery
Axle discovers:
- ✅ All function names and signatures
- ✅ Parameter names and types (from annotations)
- ✅ Docstrings for each function
- ✅ Main entry point detection (main, run, cli, start, execute)
- ✅ Classes and their methods

### Enhanced Help System
```bash
$ axle help <tool_name>
```

Shows:
- Tool description
- All available functions with signatures
- Function docstrings
- Usage examples for each function
- Whether the tool is contract-based, argparse-based, or multi-function

## 📊 Comparison

| Feature | Axle v1.0 | Axle v1.2+ |
|---------|-----------|------------|
| **Tool Types** | Contract-only | Contract + Argparse + Multi-function |
| **Discovery** | Manual list | Automatic AST + introspection |
| **Type Conversion** | Manual | Automatic based on signatures |
| **Help System** | Basic | Comprehensive with signatures |
| **Function Support** | main() only | Any function can be called |
| **Zero Modifications** | ❌ No | ✅ Yes |

## 🎯 Best Practices

### 1. Choose the Right Tool Type
- **Contract tools**: Best for AI/prompt-based tools
- **Argparse tools**: Best for complex CLI interfaces with many options
- **Multi-function tools**: Best for utility functions and calculations

### 2. Add Type Hints
```python
def calculate(a: int, b: float) -> float:
    return a + b
```
This helps Axle convert arguments properly.

### 3. Write Clear Docstrings
```python
def process_text(text: str, uppercase: bool = False) -> str:
    """Process text with optional uppercase conversion.

    Args:
        text: The text to process
        uppercase: Whether to convert to uppercase

    Returns:
        Processed text
    """
    return text.upper() if uppercase else text
```

### 4. Use Descriptive Function Names
```python
# Good
def calculate_monthly_payment(principal: float, rate: float, years: int) -> float:

# Avoid
def calc(p, r, y):
```

## 🛠️ Troubleshooting

### Tool Not Found
```bash
$ axle run my_tool
❌ Tool 'my_tool' not found
```
**Solution**: Check `axle list` to see available tools. Ensure the file is in the `tools/` directory.

### Function Not Found
```bash
$ axle run my_tool my_function arg1
❌ Function 'my_function' not found in tool
```
**Solution**: Use `axle help my_tool` to see available functions.

### Type Conversion Errors
```bash
$ axle run my_tool process "not_a_number"
❌ Error running process: invalid literal for int()
```
**Solution**: Provide arguments in the correct type (numbers as numbers, not strings).

### Argparse Tool Needs Options
```bash
$ axle run my_argparse_tool
# Tool's argparse shows error about missing arguments
```
**Solution**: Run the tool directly with Python to see its help:
```bash
python tools/my_argparse_tool.py --help
```

## 📚 Advanced Usage

### Calling Specific Functions
```bash
# Run a specific function from a multi-function tool
axle run <tool> <function_name> <arg1> <arg2> <arg3>

# Example
axle run example_simple_calculator divide 20 4
```

### Running Contract-Based Tools
```bash
# Old interface still works
axle run <tool> "prompt text"

# Example
axle run 01_seo_keyword_checker "python programming best practices"
```

### Running Argparse-Based Tools
```bash
# Just run the tool - Axle calls main() and lets argparse handle it
axle run <tool>

# For specific argparse options, run directly
python tools/<tool>.py --option value
```

## 🎉 Summary

With Axle's intelligent tool discovery system:
- ✅ **Drop any Python script** in `tools/` and it works
- ✅ **Zero modifications** needed for most scripts
- ✅ **Automatic type conversion** based on function signatures
- ✅ **Comprehensive help** for all tools and functions
- ✅ **Multiple interfaces** supported (contract, argparse, functions)
- ✅ **Backward compatible** with existing Axle tools

**Just drop and run!** 🚀
