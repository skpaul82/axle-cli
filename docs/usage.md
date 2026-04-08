# Usage Guide

This guide shows you how to use Buddy Tools effectively.

## Basic Concepts

### The Tool Numbering System

Tools are numbered for easy reference:

```
1. seo_keyword_checker
2. meta_tag_auditor
3. daily_life_hack_generator
```

You can run tools by number or by name:

```bash
# By number
buddy run 1 "your prompt"

# By name
buddy run seo_keyword_checker "your prompt"
```

### Prompts

Most tools accept a "prompt" - this is the input text or context for the tool:

```bash
buddy run 1 "python is a great programming language for data science"
```

## Common Commands

### List All Tools

See what tools are available:

```bash
buddy list
```

Output:
```
Hey buddy, let me know how I can help you. Choose a tool from the list or enter a number.

  1. seo_keyword_checker - Analyze text for SEO keyword density and optimization suggestions
  2. meta_tag_auditor - Analyze HTML/webpage for meta tag completeness and SEO best practices
  3. daily_life_hack_generator - Generate personalized productivity and life optimization tips
```

### Run a Tool

Execute a tool with a prompt:

```bash
buddy run 1 "your text here"
```

### Get Tool Information

Learn more about a specific tool:

```bash
buddy info seo_keyword_checker
```

### Check Your Setup

Verify everything is working:

```bash
buddy doctor
```

### Security Scan

Check for vulnerabilities:

```bash
buddy scan
```

## Tool-Specific Usage

### 1. SEO Keyword Checker

Analyzes text for keyword density and SEO optimization.

**Basic Usage:**

```bash
buddy run 1 "python is a great programming language for data science and machine learning"
```

**What It Does:**

- Extracts important keywords from your text
- Calculates keyword density (frequency/percentage)
- Checks if keywords appear in the first 100 words
- Provides SEO recommendations

**Best Practices:**

1. **Optimal Density**: Aim for 1-2% keyword density
2. **Prominence**: Include focus keywords in the first 100 words
3. **Variations**: Use natural variations of keywords
4. **Readability**: Don't sacrifice readability for metrics

**Example Output:**

```
🔍 SEO Keyword Analysis
============================================================

📝 Analyzing text (15 words)...

🎯 Top Keywords:
------------------------------------------------------------

1. "Python"
   Occurrences: 2 / 15 words
   Density: 13.3%
   Status: ⚠ High density (13.3%), may appear as keyword stuffing

💡 Recommendations:
• Consider reducing keyword frequency for better SEO
```

### 2. Meta Tag Auditor

Analyzes HTML or webpages for meta tag completeness and SEO best practices.

**Basic Usage with URL:**

```bash
buddy run 2 "https://example.com"
```

**Basic Usage with HTML File:**

```bash
buddy run 2 "./page.html"
```

**What It Checks:**

- Title tag (50-60 characters optimal)
- Meta description (150-160 characters optimal)
- Viewport tag (mobile-friendly)
- Canonical URL
- Open Graph tags (social sharing)
- Twitter Card tags
- Schema.org markup
- Heading structure (H1 tags)
- Image alt text

**Best Practices:**

1. **Title Length**: Keep between 50-60 characters
2. **Description**: 150-160 characters for optimal display
3. **Open Graph**: Include for better social sharing
4. **H1 Tags**: Use only one H1 per page
5. **Alt Text**: Add descriptive alt text to all images

**Example Output:**

```
🔍 Meta Tag Audit
============================================================

📝 Analyzing: https://example.com

⚠️ Issues Found

HIGH:
• Missing meta description (150-160 chars recommended)

✅ Present Tags

   Title:
     Example Domain
     13 chars

💡 Quick Wins:
   1. Add/optimize meta description (150-160 characters)
   2. Ensure title tag is 50-60 characters
   3. Add Open Graph tags for social sharing
```

### 3. Daily Life Hack Generator

Generates personalized productivity and life optimization tips.

**Basic Usage:**

```bash
buddy run 3 "I need better productivity"
```

**More Specific:**

```bash
buddy run 3 "morning routine tips"
```

**What It Does:**

- Matches your context to relevant life hacks
- Provides difficulty ratings (Easy/Medium/Hard)
- Shows time estimates
- Explains why each hack works

**Categories:**

- Morning Routine
- Productivity
- Health
- Finance
- Tech
- Organization
- Mindfulness

**Example Prompts:**

- "morning routine"
- "productivity tips"
- "save money"
- "get organized"
- "fitness motivation"
- "work from home"

**Example Output:**

```
💡 Personalized Life Hacks for: "I need better productivity"

============================================================

1. 🟢 Pomodoro Technique: 25min work, 5min break
   Category: Productivity
   Difficulty: Easy | Time: N/A
   💭 Why: Prevents burnout, maintains focus, and creates urgency for tasks.

2. 🟢 2-minute rule: If it takes <2 min, do it now
   Category: Productivity
   Difficulty: Easy | Time: N/A
   💭 Why: Prevents small tasks from piling up and becoming overwhelming.
```

## Tips for Better Results

### SEO Tools

1. **Use Real Content**: Analyze actual web content, not placeholder text
2. **Compare Competitors**: Run the same analysis on competitor content
3. **Iterate**: Make changes and re-analyze to see improvements
4. **Focus**: Optimize for one primary keyword per piece of content

### Meta Tag Auditor

1. **Check Your Own Site**: Regularly audit your own pages
2. **Competitor Analysis**: See what meta tags competitors use
3. **Social Preview**: Use Open Graph checking tools to preview social shares
4. **Mobile**: Always check viewport and mobile optimization

### Life Hack Generator

1. **Be Specific**: More specific prompts give better results
2. **Try Variations**: Experiment with different phrasing
3. **Start Small**: Begin with "Easy" difficulty hacks
4. **Build Habits**: Focus on one or two hacks at a time

## Advanced Usage

### Piping Content

You can pipe content into tools (on Unix-like systems):

```bash
echo "Your content here" | xargs buddy run 1
```

### Chaining Commands

Combine buddy commands:

```bash
buddy scan && buddy list && buddy run 3 "productivity"
```

### Using in Scripts

Use buddy commands in shell scripts:

```bash
#!/bin/bash
# Daily SEO check
buddy run 1 "$(cat today's-content.txt)"
```

### Integration with Other Tools

Combine with other CLI tools:

```bash
# Get content from URL, analyze keywords
curl -s https://example.com | buddy run 1
```

## Common Use Cases

### Content Creation

```bash
# Analyze blog post for SEO
buddy run 1 "$(cat blog-post.md)"

# Get writing productivity tips
buddy run 3 "writing focus"
```

### Website Audit

```bash
# Audit homepage
buddy run 2 "https://mysite.com"

# Security check
buddy scan
```

### Daily Routine

```bash
# Morning productivity tips
buddy run 3 "morning routine energy"

# Health optimization
buddy run 3 "daily health habits"
```

## Troubleshooting

### Tool Not Found

If you get "tool not found":

1. Check the tool name with `buddy list`
2. Use the number instead: `buddy run 1 "prompt"`
3. Verify the tool file exists in `tools/`

### Empty Results

If a tool produces no results:

1. Make sure you provided a prompt
2. Check if the prompt is relevant to the tool
3. Try a more specific prompt

### Slow Performance

Some tools may be slow due to:

1. ML model loading (first run)
2. Large file processing
3. Network requests (URL analysis)

## Best Practices Summary

1. **Start with `buddy list`** - See what's available
2. **Use meaningful prompts** - Better input = better output
3. **Read the recommendations** - Tools provide actionable advice
4. **Iterate and improve** - Make changes based on suggestions
5. **Combine tools** - Use multiple tools together for best results

## Getting More Help

- [Command Reference](commands.md) - Detailed command documentation
- [Troubleshooting](troubleshooting.md) - Solve common problems
- GitHub Issues - Report bugs or request features
