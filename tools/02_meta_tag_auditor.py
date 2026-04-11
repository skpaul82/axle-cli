#!/usr/bin/env python3
"""Meta Tag Auditor - Analyze HTML/webpage for meta tag completeness and SEO best practices."""

import re
import sys
from urllib.parse import urlparse


def get_description():
    """Return tool description."""
    return "Analyze HTML/webpage for meta tag completeness and SEO best practices"


def is_url(text):
    """Check if text is a URL."""
    try:
        result = urlparse(text.strip())
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def fetch_html(url):
    """Fetch HTML content from URL."""
    try:
        import requests

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except ImportError:
        print("❌ requests library not installed. Install with: pip install requests")
        return None
    except Exception as e:
        print(f"❌ Error fetching URL: {e}")
        return None


def parse_html(html):
    """Parse HTML and extract meta tags."""
    try:
        from bs4 import BeautifulSoup

        return BeautifulSoup(html, "lxml")
    except ImportError:
        try:
            from bs4 import BeautifulSoup

            return BeautifulSoup(html, "html.parser")
        except ImportError:
            print(
                "❌ beautifulsoup4 not installed. Install with: pip install beautifulsoup4 lxml"
            )
            return None


def audit_meta_tags(soup):
    """Audit meta tags for SEO best practices."""
    issues = []
    present_tags = []

    # Check title tag
    title = soup.find("title")
    if title and title.string:
        title_text = title.string.strip()
        title_len = len(title_text)
        present_tags.append(("Title", title_text, f"{title_len} chars"))

        if title_len == 0:
            issues.append(("CRITICAL", "Missing title tag content"))
        elif title_len < 30:
            issues.append(
                (
                    "MEDIUM",
                    f"Title too short ({title_len} chars). Recommend 50-60 chars.",
                )
            )
        elif title_len > 60:
            issues.append(
                (
                    "MEDIUM",
                    f"Title too long ({title_len} chars). Recommend 50-60 chars.",
                )
            )
        else:
            present_tags.append(("Title", "✓ Optimal length", "50-60 chars"))
    else:
        issues.append(("CRITICAL", "Missing title tag"))

    # Check meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        desc_content = meta_desc.get("content", "").strip()
        desc_len = len(desc_content)
        present_tags.append(
            (
                "Description",
                desc_content[:50] + "..." if desc_len > 50 else desc_content,
                f"{desc_len} chars",
            )
        )

        if desc_len < 120:
            issues.append(
                (
                    "HIGH",
                    f"Description too short ({desc_len} chars). Recommend 150-160 chars.",
                )
            )
        elif desc_len > 160:
            issues.append(
                (
                    "LOW",
                    f"Description slightly long ({desc_len} chars). Optimal: 150-160 chars.",
                )
            )
        else:
            present_tags.append(("Description", "✓ Optimal length", "150-160 chars"))
    else:
        issues.append(("CRITICAL", "Missing meta description"))

    # Check viewport
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport:
        present_tags.append(("Viewport", "✓ Present", "Mobile-friendly"))
    else:
        issues.append(("MEDIUM", "Missing viewport meta tag (affects mobile)"))

    # Check canonical URL
    canonical = soup.find("link", attrs={"rel": "canonical"})
    if canonical and canonical.get("href"):
        present_tags.append(("Canonical", "✓ Present", canonical.get("href")))
    else:
        issues.append(("LOW", "Missing canonical URL (recommended for SEO)"))

    # Check robots
    robots = soup.find("meta", attrs={"name": "robots"})
    if robots:
        present_tags.append(("Robots", "✓ Present", robots.get("content", "")))
    else:
        issues.append(("INFO", "Missing robots meta tag (optional)"))

    # Check Open Graph tags
    og_title = soup.find("meta", attrs={"property": "og:title"})
    og_desc = soup.find("meta", attrs={"property": "og:description"})
    og_image = soup.find("meta", attrs={"property": "og:image"})

    og_count = sum([bool(og_title), bool(og_desc), bool(og_image)])
    if og_count >= 2:
        present_tags.append(
            ("Open Graph", f"✓ {og_count}/3 tags", "Social sharing optimized")
        )
    elif og_count == 1:
        issues.append(
            (
                "LOW",
                "Incomplete Open Graph tags. Add og:title, og:description, og:image",
            )
        )
    else:
        issues.append(
            ("MEDIUM", "Missing Open Graph tags (recommended for social sharing)")
        )

    # Check Twitter Card
    twitter_card = soup.find("meta", attrs={"name": "twitter:card"})
    if twitter_card:
        present_tags.append(("Twitter Card", "✓ Present", "Twitter sharing optimized"))
    else:
        issues.append(
            ("LOW", "Missing Twitter Card tags (recommended for Twitter sharing)")
        )

    # Check schema.org
    schema_scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    if schema_scripts:
        present_tags.append(
            ("Schema.org", f"✓ {len(schema_scripts)} markup(s)", "Structured data")
        )
    else:
        issues.append(("LOW", "No Schema.org markup found (optional but recommended)"))

    # Check headings structure
    h1_count = len(soup.find_all("h1"))
    if h1_count == 1:
        present_tags.append(("H1", "✓ One H1 tag", "Proper heading structure"))
    elif h1_count == 0:
        issues.append(("MEDIUM", "Missing H1 tag (important for SEO)"))
    else:
        issues.append(
            ("MEDIUM", f"Multiple H1 tags ({h1_count}). Use only one H1 per page.")
        )

    # Check images with alt text
    images = soup.find_all("img")
    images_with_alt = [img for img in images if img.get("alt")]
    if images:
        alt_percentage = (len(images_with_alt) / len(images)) * 100
        if alt_percentage >= 80:
            present_tags.append(
                (
                    "Images",
                    f"✓ {len(images_with_alt)}/{len(images)} with alt",
                    "Good accessibility",
                )
            )
        elif alt_percentage >= 50:
            issues.append(
                (
                    "LOW",
                    f"{int(alt_percentage)}% of images have alt text. Aim for 100%.",
                )
            )
        else:
            issues.append(
                (
                    "MEDIUM",
                    f"Many images missing alt text ({len(images) - len(images_with_alt)} of {len(images)}).",
                )
            )

    return issues, present_tags


def generate_recommendations(issues):
    """Generate prioritized recommendations."""
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}

    # Sort by priority
    sorted_issues = sorted(issues, key=lambda x: priority_order.get(x[0], 5))

    # Group by priority
    by_priority = {}
    for priority, message in sorted_issues:
        if priority not in by_priority:
            by_priority[priority] = []
        by_priority[priority].append(message)

    return by_priority


def main(prompt):
    """Main entry point for meta tag auditing."""
    if not prompt or not prompt.strip():
        print("❌ Please provide a URL or HTML file path to analyze.")
        print('   Usage: buddy run meta_tag_auditor "https://example.com"')
        print('   Usage: buddy run meta_tag_auditor "./page.html"')
        return

    input_text = prompt.strip()

    print(f"\n🔍 Meta Tag Audit")
    print("=" * 60)
    print(f"\n📝 Analyzing: {input_text}\n")

    # Fetch or read HTML
    if is_url(input_text):
        html = fetch_html(input_text)
        if html is None:
            return
    else:
        # Try to read as file
        try:
            with open(input_text, "r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {input_text}")
            return
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return

    # Parse HTML
    soup = parse_html(html)
    if soup is None:
        return

    # Audit meta tags
    issues, present_tags = audit_meta_tags(soup)

    # Display critical issues first
    critical = [i for i in issues if i[0] == "CRITICAL"]
    if critical:
        print("🚨 Critical Issues")
        print("-" * 60)
        for _, message in critical:
            print(f"   ❌ {message}\n")

    # Display other issues
    other_issues = [i for i in issues if i[0] != "CRITICAL"]
    if other_issues:
        print("⚠️ Issues Found")
        print("-" * 60)
        by_priority = generate_recommendations(other_issues)

        for priority in ["HIGH", "MEDIUM", "LOW", "INFO"]:
            if priority in by_priority:
                print(f"\n{priority}:")
                for message in by_priority[priority][:5]:
                    print(f"   • {message}")

    # Display present tags
    if present_tags:
        print("\n" + "=" * 60)
        print("✅ Present Tags")
        print("-" * 60)

        for tag_name, value, detail in present_tags:
            print(f"\n   {tag_name}:")
            print(f"     {value}")
            if detail:
                print(f"     {detail}")

    # Generate summary and recommendations
    print("\n" + "=" * 60)
    print("📊 Summary & Recommendations")
    print("-" * 60)

    # Count by severity
    severity_counts = {}
    for priority, _ in issues:
        severity_counts[priority] = severity_counts.get(priority, 0) + 1

    print(f"\n   Total Issues: {len(issues)}")
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        count = severity_counts.get(severity, 0)
        if count > 0:
            print(f"   {severity}: {count}")

    # Overall score
    total_tags = len(present_tags) + len(issues)
    if total_tags > 0:
        score = (len(present_tags) / total_tags) * 100
        print(f"\n   SEO Score: {score:.0f}%")

        if score >= 80:
            print("   ✅ Great! Your page has strong SEO fundamentals.")
        elif score >= 60:
            print("   ⚠️ Good foundation. Address critical issues for better SEO.")
        else:
            print("   ❌ Needs improvement. Focus on critical issues first.")

    # Quick wins
    print("\n💡 Quick Wins:")
    print("   1. Add/optimize meta description (150-160 characters)")
    print("   2. Ensure title tag is 50-60 characters")
    print("   3. Add Open Graph tags for social sharing")
    print("   4. Add alt text to all images")
    print("   5. Implement Schema.org markup")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        main(" ".join(sys.argv[1:]))
    else:
        main("")
