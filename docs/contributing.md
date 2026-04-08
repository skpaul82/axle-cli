# Contributing Guide

Thank you for your interest in contributing to Axle CLI! This guide will help you get started.

## Ways to Contribute

We welcome contributions in many forms:

- **Bug Reports**: Report issues you encounter
- **Feature Requests**: Suggest new features or tools
- **Code Contributions**: Fix bugs or add features
- **Documentation**: Improve documentation
- **Tools**: Create new tools for the toolkit
- **Testing**: Help test and verify functionality

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/your-username/axle-cli.git
cd axle-cli
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install in editable mode
pip install -e .
pip install -r requirements.txt
```

### 3. Install Development Dependencies

```bash
# Optional: Install development tools
pip install flake8 black isort pytest
```

### 4. Verify Installation

```bash
buddy doctor
buddy list
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

Edit files following the guidelines below.

### 3. Test Your Changes

```bash
# Run basic tests
buddy list
buddy run 1 "test"
buddy doctor
```

### 4. Commit Changes

```bash
git add .
git commit -m "Clear description of changes"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Adding New Tools

### Tool Structure

All tools must follow this structure:

```python
#!/usr/bin/env python3
"""Tool description."""

import sys

def get_description():
    """Return tool description."""
    return "Brief one-line description of what this tool does"

def main(prompt):
    """Main entry point for the tool.

    Args:
        prompt: User-provided prompt string (may be empty)
    """
    # Your tool logic here
    print(f"Processing: {prompt}")

if __name__ == "__main__":
    main(" ".join(sys.argv[1:]))
```

### Tool Requirements

1. **File Naming**: Use numbered prefix: `04_your_tool_name.py`
2. **Description**: Implement `get_description()` function
3. **Main Function**: Implement `main(prompt)` function
4. **Error Handling**: Handle errors gracefully
5. **User Feedback**: Provide clear output and error messages

### Tool Template

```python
#!/usr/bin/env python3
"""Your Tool Name - Brief description."""

def get_description():
    """Return tool description."""
    return "What this tool does"

def main(prompt):
    """Main entry point."""
    if not prompt or not prompt.strip():
        print("❌ Please provide input.")
        print("   Usage: buddy run your_tool \"your input here\"")
        return

    # Process input
    result = process_input(prompt)

    # Display results
    print(f"\n🔍 Results:")
    print(f"   {result}")

def process_input(text):
    """Process the input text.

    Args:
        text: Input string to process

    Returns:
        Processed result
    """
    # Your logic here
    return text.upper()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(" ".join(sys.argv[1:]))
    else:
        main("")
```

### Tool Guidelines

1. **Purpose**: Tools should be useful for SEO or daily-life productivity
2. **Input**: Accept a prompt string from the user
3. **Output**: Provide clear, formatted output with emojis for readability
4. **Errors**: Handle errors gracefully with helpful messages
5. **Dependencies**: Minimize external dependencies when possible
6. **Performance**: Consider execution time and resource usage

## Code Style

### Python Style Guide

Follow [PEP 8](https://pep8.org/) style guidelines:

```python
# Good
def calculate_density(text, keywords):
    """Calculate keyword density."""
    total_words = len(text.split())
    if total_words == 0:
        return 0
    return len(keywords) / total_words

# Bad
def calc(t,k):
    return len(k)/len(t.split())
```

### Formatting Tools

We use these tools for code formatting:

```bash
# Format code
black scripts/ tools/

# Sort imports
isort scripts/ tools/

# Lint code
flake8 scripts/ tools/
```

### Naming Conventions

- **Files**: `snake_case.py` (with numeric prefix for tools)
- **Functions**: `snake_case`
- **Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Classes**: `PascalCase`

### Docstrings

Use Google-style docstrings:

```python
def calculate_metrics(text, keywords):
    """Calculate various SEO metrics.

    Args:
        text: The text content to analyze
        keywords: List of keywords to check

    Returns:
        Dictionary with metrics including density, prominence,
        and frequency
    """
    pass
```

## Testing

### Manual Testing

Test your changes manually:

```bash
# Test CLI commands
buddy list
buddy info your_tool
buddy run your_tool "test input"

# Test error handling
buddy run your_tool ""
buddy run 999 "test"
```

### Automated Testing (Future)

We're working on adding automated tests. For now, manual testing is sufficient.

### Testing Checklist

Before submitting a PR:

- [ ] Tool appears in `buddy list`
- [ ] Tool runs without errors
- [ ] Tool produces expected output
- [ ] Tool handles empty/invalid input gracefully
- [ ] Tool description is clear
- [ ] Code follows style guidelines
- [ ] No console errors or warnings

## Documentation

### Updating Documentation

If you add features or change behavior:

1. **README.md**: Update features list if needed
2. **docs/usage.md**: Add usage examples
3. **docs/commands.md**: Update command reference
4. **docs/changelog.md**: Add entry to changelog

### Documentation Style

- Use clear, concise language
- Provide examples for common use cases
- Include error messages and solutions
- Use code blocks for commands and code

## Pull Request Guidelines

### PR Title

Use clear, descriptive titles:

```
Good: Add sentiment analysis tool for SEO
Bad: fixed stuff
```

### PR Description

Include:

1. **Summary**: What changes were made and why
2. **Testing**: How you tested the changes
3. **Screenshots**: If applicable (especially for UI changes)
4. **Breaking Changes**: Note any breaking changes
5. **Related Issues**: Link to related issues

### PR Template

```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How I tested these changes

## Screenshots (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tested manually
- [ ] Ready for review
```

## Code Review Process

### What We Look For

1. **Functionality**: Does it work as intended?
2. **Code Quality**: Is code clean and well-structured?
3. **Style**: Does it follow PEP 8 and project conventions?
4. **Documentation**: Is it well-documented?
5. **Testing**: Has it been adequately tested?
6. **Performance**: Are there any performance concerns?

### Review Timeline

We aim to review PRs within 1-3 days. Complex changes may take longer.

### Feedback

We provide constructive feedback on all PRs. Don't take it personally - we're all working to improve the project!

## Community Guidelines

### Be Respectful

- Treat everyone with respect
- Welcome newcomers and help them learn
- Assume good intentions

### Be Constructive

- Focus on what is best for the community
- Show empathy towards other community members

### Be Collaborative

- Work together to solve problems
- Ask for help when needed
- Offer help when you can

## Getting Help

### Questions?

- Check existing documentation
- Search GitHub Issues
- Start a discussion on GitHub
- Reach out on social media

### Need Guidance?

- Ask in your PR: "I'm not sure about this part"
- Request a review from a maintainer
- Start a discussion for complex changes

## Recognition

Contributors are recognized in:

- CONTRIBUTORS.md file
- Release notes for significant contributions
- Project README for major contributors

Thank you for contributing to Buddy Tools! 🎉

---

## Quick Reference

### Essential Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -e .

# Development
git checkout -b feature/my-feature
# make changes
git add .
git commit -m "Description"
git push origin feature/my-feature

# Testing
buddy list
buddy run 1 "test"
buddy doctor
```

### Resources

- [Python Style Guide](https://pep8.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Effective PR Descriptions](https://github.blog/2014-09-30-writing-good-commit-messages/)
