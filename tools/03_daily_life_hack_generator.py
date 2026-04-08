#!/usr/bin/env python3
"""Daily Life Hack Generator - Generate productivity and life optimization tips."""

import random
import sys


def get_description():
    """Return tool description."""
    return "Generate personalized productivity and life optimization tips"


def get_hack_database():
    """Return comprehensive database of curated life hacks."""
    return {
        "morning": [
            {
                "hack": "Drink 16oz water immediately upon waking",
                "category": "Morning Routine",
                "difficulty": "Easy",
                "time": "1 min",
                "why": "Hydrating after sleep rehydrates your brain, improves focus, and kickstarts metabolism."
            },
            {
                "hack": "Make your bed first thing",
                "category": "Morning Routine",
                "difficulty": "Easy",
                "time": "2 min",
                "why": "Completes your first task of the day, creating momentum and sense of accomplishment."
            },
            {
                "hack": "5-minute morning stretch routine",
                "category": "Morning Routine",
                "difficulty": "Easy",
                "time": "5 min",
                "why": "Increases blood flow, reduces muscle tension, and boosts energy naturally."
            },
            {
                "hack": "No phone for first 30 minutes of the day",
                "category": "Morning Routine",
                "difficulty": "Medium",
                "time": "N/A",
                "why": "Prevents reactive mindset and allows you to start the day proactively."
            },
            {
                "hack": "Prepare tomorrow's clothes tonight",
                "category": "Morning Routine",
                "difficulty": "Easy",
                "time": "2 min (night before)",
                "why": "Eliminates decision fatigue and saves morning time."
            }
        ],
        "productivity": [
            {
                "hack": "Pomodoro Technique: 25min work, 5min break",
                "category": "Productivity",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Prevents burnout, maintains focus, and creates urgency for tasks."
            },
            {
                "hack": "Batch similar tasks together",
                "category": "Productivity",
                "difficulty": "Medium",
                "time": "N/A",
                "why": "Reduces context switching and increases efficiency by up to 40%."
            },
            {
                "hack": "2-minute rule: If it takes <2 min, do it now",
                "category": "Productivity",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Prevents small tasks from piling up and becoming overwhelming."
            },
            {
                "hack": "Time blocking: Schedule every hour of your day",
                "category": "Productivity",
                "difficulty": "Medium",
                "time": "10 min (morning)",
                "why": "Creates structure, reduces procrastination, and improves time awareness."
            },
            {
                "hack": "Eat the frog: Do your hardest task first",
                "category": "Productivity",
                "difficulty": "Medium",
                "time": "N/A",
                "why": "Tackles most challenging task when willpower is highest, reducing anxiety."
            },
            {
                "hack": "Turn off all notifications during deep work",
                "category": "Productivity",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Eliminates distractions and can increase focus time by up to 3x."
            },
            {
                "hack": "Use noise-canceling headphones or white noise",
                "category": "Productivity",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Blocks distractions and creates a focused work environment."
            }
        ],
        "health": [
            {
                "hack": "Take a 5-minute walk every hour",
                "category": "Health",
                "difficulty": "Easy",
                "time": "5 min/hour",
                "why": "Counteracts sedentary behavior, boosts circulation, and refreshes focus."
            },
            {
                "hack": "20-20-20 rule: Every 20 min, look 20ft away for 20 sec",
                "category": "Health",
                "difficulty": "Easy",
                "time": "20 sec",
                "why": "Reduces eye strain and headaches from screen use."
            },
            {
                "hack": "Keep a water bottle at your desk",
                "category": "Health",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Encourages hydration, which improves energy and cognitive function."
            },
            {
                "hack": "Stand during phone calls",
                "category": "Health",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Burns calories and reduces sedentary time effortlessly."
            },
            {
                "hack": "Meal prep on Sunday for the week",
                "category": "Health",
                "difficulty": "Medium",
                "time": "2 hours",
                "why": "Saves time during the week, ensures healthier eating, and reduces decision fatigue."
            },
            {
                "hack": "Practice 4-7-8 breathing when stressed",
                "category": "Health",
                "difficulty": "Easy",
                "time": "1 min",
                "why": "Activates parasympathetic nervous system, reducing anxiety quickly."
            }
        ],
        "finance": [
            {
                "hack": "Automate savings: Set up auto-transfer on payday",
                "category": "Finance",
                "difficulty": "Easy",
                "time": "10 min (one-time)",
                "why": "Pays yourself first without relying on willpower."
            },
            {
                "hack": "24-hour rule before non-essential purchases",
                "category": "Finance",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Prevents impulse buying and saves money."
            },
            {
                "hack": "Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings",
                "category": "Finance",
                "difficulty": "Medium",
                "time": "30 min (monthly)",
                "why": "Balanced budgeting framework that's simple and effective."
            },
            {
                "hack": "Negotiate recurring bills annually",
                "category": "Finance",
                "difficulty": "Medium",
                "time": "1 hour/year",
                "why": "Can save hundreds per year on insurance, internet, and subscriptions."
            },
            {
                "hack": "Unsubscribe from marketing emails",
                "category": "Finance",
                "difficulty": "Easy",
                "time": "15 min",
                "why": "Reduces temptation to spend and decreases inbox clutter."
            },
            {
                "hack": "Use cashback apps for purchases",
                "category": "Finance",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Earn money back on purchases you'd make anyway."
            }
        ],
        "tech": [
            {
                "hack": "Use password manager (e.g., Bitwarden, 1Password)",
                "category": "Tech",
                "difficulty": "Medium",
                "time": "30 min setup",
                "why": "Improves security and eliminates password memory."
            },
            {
                "hack": "Enable two-factor authentication everywhere",
                "category": "Tech",
                "difficulty": "Easy",
                "time": "15 min",
                "why": "Protects accounts from unauthorized access effectively."
            },
            {
                "hack": "Use keyboard shortcuts for your most-used actions",
                "category": "Tech",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Saves significant time and reduces repetitive strain."
            },
            {
                "hack": "Set up automatic cloud backups",
                "category": "Tech",
                "difficulty": "Easy",
                "time": "10 min (one-time)",
                "why": "Protects against data loss from hardware failure or theft."
            },
            {
                "hack": "Use focus mode or website blockers during work",
                "category": "Tech",
                "difficulty": "Easy",
                "time": "N/A",
                "why": "Prevents digital distractions and improves productivity."
            },
            {
                "hack": "Clean up your desktop downloads folder weekly",
                "category": "Tech",
                "difficulty": "Easy",
                "time": "5 min/week",
                "why": "Organized digital workspace reduces stress and improves efficiency."
            }
        ],
        "organization": [
            {
                "hack": "One-touch rule: Handle items once (do, delegate, defer, delete)",
                "category": "Organization",
                "difficulty": "Medium",
                "time": "N/A",
                "why": "Prevents clutter buildup and reduces decision fatigue."
            },
            {
                "hack": "Designate a place for everything (key hook, mail tray)",
                "category": "Organization",
                "difficulty": "Easy",
                "time": "30 min",
                "why": "Eliminates daily searching for lost items."
            },
            {
                "hack": "Do a 10-minute evening tidy-up",
                "category": "Organization",
                "difficulty": "Easy",
                "time": "10 min/night",
                "why": "Starts each morning with a clean, organized space."
            },
            {
                "hack": "Use the 'one in, one out' rule for new items",
                "category": "Organization",
                "difficulty": "Medium",
                "time": "N/A",
                "why": "Prevents accumulation and maintains clutter-free space."
            },
            {
                "hack": "Create a launching pad near the door (keys, wallet, bag)",
                "category": "Organization",
                "difficulty": "Easy",
                "time": "5 min",
                "why": "Never forget essentials when leaving the house."
            },
            {
                "hack": "Digitize important documents",
                "category": "Organization",
                "difficulty": "Medium",
                "time": "1 hour",
                "why": "Creates backups and reduces physical paper clutter."
            }
        ],
        "mindfulness": [
            {
                "hack": "Practice gratitude: Write 3 things you're grateful for",
                "category": "Mindfulness",
                "difficulty": "Easy",
                "time": "2 min",
                "why": "Shifts mindset to positivity and improves mental health."
            },
            {
                "hack": "Take a 10-minute tech break daily",
                "category": "Mindfulness",
                "difficulty": "Medium",
                "time": "10 min",
                "why": "Reduces digital overwhelm and improves presence."
            },
            {
                "hack": "Practice box breathing: 4-4-4-4 pattern",
                "category": "Mindfulness",
                "difficulty": "Easy",
                "time": "2 min",
                "why": "Calms nervous system and reduces stress quickly."
            },
            {
                "hack": "Journal for 5 minutes about your day",
                "category": "Mindfulness",
                "difficulty": "Easy",
                "time": "5 min",
                "why": "Processes emotions, gains clarity, and tracks patterns."
            },
            {
                "hack": "Set boundaries: Learn to say 'no' to non-essentials",
                "category": "Mindfulness",
                "difficulty": "Medium",
                "time": "N/A",
                "why": "Protects time and energy for what truly matters."
            }
        ]
    }


def extract_keywords(prompt):
    """Extract keywords from user prompt."""
    # Simple keyword extraction - split and filter common words
    words = prompt.lower().split()
    stop_words = {'i', 'want', 'need', 'help', 'for', 'the', 'a', 'an', 'to', 'and', 'or', 'but', 'with', 'my', 'me', 'am', 'is', 'are'}

    keywords = [w for w in words if len(w) > 2 and w not in stop_words]
    return keywords


def select_hacks(context, hack_db):
    """Select relevant hacks based on context keywords."""
    all_hacks = []
    keywords = extract_keywords(context)

    # Create a flat list of hacks with category names for matching
    for category, hacks in hack_db.items():
        for hack in hacks:
            all_hacks.append((category, hack))

    # Score hacks based on keyword matches
    scored_hacks = []
    for category, hack in all_hacks:
        score = 0

        # Check if category matches
        if any(keyword in category for keyword in keywords):
            score += 3

        # Check if keywords appear in hack description
        hack_text = f"{hack['hack']} {hack['why']}".lower()
        for keyword in keywords:
            if keyword in hack_text:
                score += 1

        # Add small random factor for variety
        score += random.uniform(0, 0.5)

        scored_hacks.append((score, category, hack))

    # Sort by score and return top matches
    scored_hacks.sort(key=lambda x: x[0], reverse=True)
    top_hacks = [hack for score, category, hack in scored_hacks[:10]]

    # If no good matches, return diverse selection
    if sum(score for score, _, _ in scored_hacks[:10]) == 0:
        categories = list(hack_db.keys())
        random.shuffle(categories)
        top_hacks = []
        for cat in categories[:5]:
            if hack_db[cat]:
                top_hacks.append(random.choice(hack_db[cat]))

    return top_hacks[:5]


def format_hacks(hacks, context):
    """Format hacks for display."""
    print(f"\n💡 Personalized Life Hacks for: \"{context}\"\n")
    print("=" * 60)

    for i, hack in enumerate(hacks, 1):
        difficulty_emoji = {
            'Easy': '🟢',
            'Medium': '🟡',
            'Hard': '🔴'
        }.get(hack['difficulty'], '⚪')

        print(f"\n{i}. {difficulty_emoji} {hack['hack']}")
        print(f"   Category: {hack['category']}")
        print(f"   Difficulty: {hack['difficulty']} | Time: {hack['time']}")
        print(f"   💭 Why: {hack['why']}")

    print("\n" + "=" * 60)
    print("📚 Want more tips? Try these prompts:")
    print("   \"morning routine\"")
    print("   \"productivity tips\"")
    print("   \"fitness hacks\"")
    print("   \"save money\"")
    print("   \"organization\"")


def main(prompt):
    """Main entry point for life hack generation."""
    if not prompt or not prompt.strip():
        print("❌ Please provide a context or situation.")
        print("   Usage: buddy run daily_life_hack_generator \"I need better productivity\"")
        print("   Usage: buddy run daily_life_hack_generator \"morning routine tips\"")
        return

    context = prompt.strip()

    # Get hack database
    hack_db = get_hack_database()

    # Select relevant hacks
    selected_hacks = select_hacks(context, hack_db)

    # Format and display
    format_hacks(selected_hacks, context)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(" ".join(sys.argv[1:]))
    else:
        main("")
