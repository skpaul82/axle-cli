#!/usr/bin/env python3
"""SEO Keyword Checker - Analyze text for keyword density and SEO suggestions."""

import re
from collections import Counter
import sys


def get_description():
    """Return tool description."""
    return "Analyze text for SEO keyword density and optimization suggestions"


def download_nltk_data():
    """Download required NLTK data silently."""
    try:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
    except ImportError:
        print("⚠ NLTK not installed. Install with: pip install nltk")
        sys.exit(1)


def extract_keywords(text):
    """Extract important keywords from text using NLTK."""
    download_nltk_data()

    try:
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
    except ImportError:
        # Fallback to simple tokenization
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'will', 'with', 'that', 'this', 'from', 'they', 'would', 'there', 'their', 'what', 'about', 'which', 'when', 'make', 'like', 'into', 'year', 'your', 'just', 'over', 'also', 'such', 'because', 'these', 'first', 'being', 'through', 'most', 'some', 'those'}
        words = [w for w in words if w not in stop_words]
        return Counter(words)

    # Tokenize and filter
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))

    # Filter: meaningful words only
    keywords = [
        word for word in words
        if word.isalpha()
        and len(word) > 2
        and word not in stop_words
    ]

    return Counter(keywords)


def calculate_density(text, keywords):
    """Calculate keyword density metrics."""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    total_words = len(words)

    if total_words == 0:
        return {}

    densities = {}
    for keyword, count in keywords.most_common(20):
        density = (count / total_words) * 100
        densities[keyword] = {
            'count': count,
            'density': density,
            'total_words': total_words
        }

    return densities


def check_prominence(text, keyword):
    """Check if keyword appears in first 100 words (title and introduction)."""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    first_100 = ' '.join(words[:100])

    return keyword.lower() in first_100.lower()


def generate_suggestions(densities, text):
    """Generate SEO suggestions based on keyword analysis."""
    suggestions = []

    for keyword, metrics in densities.items():
        density = metrics['density']
        count = metrics['count']

        # Check optimal density (1-2%)
        if 1.0 <= density <= 2.0:
            suggestions.append({
                'keyword': keyword,
                'type': 'success',
                'message': f'✓ Optimal density ({density:.1f}%)'
            })
        elif density < 1.0:
            suggestions.append({
                'keyword': keyword,
                'type': 'warning',
                'message': f'⚠ Low density ({density:.1f}%), consider increasing to 1-2%'
            })
        else:  # density > 2.0
            suggestions.append({
                'keyword': keyword,
                'type': 'warning',
                'message': f'⚠ High density ({density:.1f}%), may appear as keyword stuffing'
            })

        # Check prominence
        if check_prominence(text, keyword):
            suggestions.append({
                'keyword': keyword,
                'type': 'success',
                'message': f'✓ Appears in first 100 words (good for SEO)'
            })
        else:
            suggestions.append({
                'keyword': keyword,
                'type': 'info',
                'message': f'💡 Consider placing in first 100 words for better prominence'
            })

    return suggestions


def main(prompt):
    """Main entry point for SEO keyword analysis."""
    if not prompt or not prompt.strip():
        print("❌ Please provide text to analyze.")
        print("   Usage: buddy run seo_keyword_checker \"your text here\"")
        return

    text = prompt.strip()

    print(f"\n🔍 SEO Keyword Analysis")
    print("=" * 60)
    print(f"\n📝 Analyzing text ({len(text.split())} words)...\n")

    # Extract keywords
    keywords = extract_keywords(text)

    if not keywords:
        print("⚠ No significant keywords found in the text.")
        return

    # Calculate densities
    densities = calculate_density(text, keywords)

    # Display top keywords
    print("🎯 Top Keywords:")
    print("-" * 60)

    for i, (keyword, metrics) in enumerate(list(densities.items())[:10], 1):
        density = metrics['density']
        count = metrics['count']
        total = metrics['total_words']

        print(f"\n{i}. \"{keyword.capitalize()}\"")
        print(f"   Occurrences: {count} / {total} words")
        print(f"   Density: {density:.1f}%")

        # Visual density indicator
        optimal = "✓" if 1.0 <= density <= 2.0 else "⚠"
        print(f"   Status: {optimal} {'Optimal' if 1.0 <= density <= 2.0 else 'Needs attention'}")

    # Generate and display suggestions
    print("\n" + "=" * 60)
    print("💡 SEO Recommendations")
    print("-" * 60)

    suggestions = generate_suggestions(densities, text)

    # Group suggestions by type
    by_type = {'success': [], 'warning': [], 'info': []}
    for s in suggestions:
        by_type[s['type']].append(s)

    # Display warnings first
    if by_type['warning']:
        print("\n⚠️ Issues to Address:")
        for s in by_type['warning'][:5]:
            print(f"   {s['message']}: \"{s['keyword'].capitalize()}\"")

    # Display successes
    if by_type['success']:
        print("\n✅ What's Working Well:")
        for s in by_type['success'][:5]:
            print(f"   {s['message']}: \"{s['keyword'].capitalize()}\"")

    # Display info tips
    if by_type['info']:
        print("\n💡 Optimization Tips:")
        for s in by_type['info'][:3]:
            print(f"   {s['message']}: \"{s['keyword'].capitalize()}\"")

    # Overall assessment
    print("\n" + "=" * 60)
    print("📊 Overall Assessment")

    top_keyword = list(densities.keys())[0]
    top_density = densities[top_keyword]['density']

    if 1.0 <= top_density <= 2.0 and check_prominence(text, top_keyword):
        print("   ✅ Good SEO foundation! Your main keyword is well-optimized.")
    elif top_density < 1.0:
        print("   ⚠️ Consider increasing keyword frequency for better SEO.")
    else:
        print("   ⚠️ Keyword density may be too high. Balance with natural language.")

    print("\n💡 Quick Tips:")
    print("   • Target keyword density: 1-2%")
    print("   • Place focus keyword in first 100 words")
    print("   • Use variations and related terms naturally")
    print("   • Focus on readability, not just metrics")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(" ".join(sys.argv[1:]))
    else:
        main("")
