"""
helpers.py
Utility functions for display formatting, role/skill name mapping,
and explanation generation for the Explainable AI component.
"""


# ============================================================
# DISPLAY NAME MAPPINGS
# Maps internal Prolog atom names to human-readable labels
# ============================================================

ROLE_DISPLAY_NAMES = {
    "software_engineer": "Software Engineer",
    "web_developer": "Web Developer",
    "data_analyst": "Data Analyst",
    "ui_ux_designer": "UI/UX Designer",
}

SKILL_DISPLAY_NAMES = {
    "python": "Python",
    "dsa": "Data Structures & Algorithms",
    "oop": "Object-Oriented Programming",
    "sql": "SQL & Databases",
    "git": "Git & Version Control",
    "html_css": "HTML & CSS",
    "javascript": "JavaScript",
    "statistics": "Statistics",
    "excel": "Excel & Spreadsheets",
    "visualization": "Data Visualization",
    "figma": "Figma Design Tool",
    "user_research": "User Research",
    "prototyping": "Prototyping",
}

CONFIDENCE_DISPLAY = {
    "high": "High Confidence",
    "medium": "Moderate Confidence",
    "low": "Low Confidence",
}

EXPERIENCE_DISPLAY = {
    "senior": "Senior (5+ years)",
    "mid": "Mid-Level (2-5 years)",
    "junior": "Junior (0-2 years)",
    "fresher": "Fresher (No experience)",
}

# Colors for skill tags (cycling through a palette)
SKILL_TAG_COLORS = [
    "#6C63FF", "#FF6584", "#43C6AC", "#F7971E", "#2193B0",
    "#cc2b5e", "#56ab2f", "#f7971e", "#12c2e9", "#c471ed"
]

# Score color thresholds
SCORE_COLORS = {
    "high": "#43C6AC",     # green-teal
    "medium": "#F7971E",   # orange
    "low": "#FF6584",      # pink-red
}


def role_to_display(role_key: str) -> str:
    """Converts internal role key to display name."""
    return ROLE_DISPLAY_NAMES.get(role_key, role_key.replace("_", " ").title())


def skill_to_display(skill_key: str) -> str:
    """Converts internal skill key to display name."""
    return SKILL_DISPLAY_NAMES.get(skill_key, skill_key.replace("_", " ").title())


def display_to_role(display_name: str) -> str:
    """Converts display name back to Prolog role key."""
    reverse_map = {v: k for k, v in ROLE_DISPLAY_NAMES.items()}
    return reverse_map.get(display_name, display_name.lower().replace(" ", "_"))


def display_to_skill(display_name: str) -> str:
    """Converts display skill name back to Prolog skill key."""
    reverse_map = {v: k for k, v in SKILL_DISPLAY_NAMES.items()}
    return reverse_map.get(display_name, display_name.lower().replace(" ", "_").replace("&", "").replace("  ", "_"))


def get_score_color(score: int) -> str:
    """Returns color string based on readiness score."""
    if score >= 70:
        return SCORE_COLORS["high"]
    elif score >= 40:
        return SCORE_COLORS["medium"]
    return SCORE_COLORS["low"]


def get_score_emoji(score: int) -> str:
    """Returns emoji based on score level."""
    if score >= 80:
        return "🏆"
    elif score >= 60:
        return "✅"
    elif score >= 40:
        return "⚡"
    return "📚"


def generate_ai_explanation(role: str, weak_skills: list, score: int,
                             confidence: str, experience: str) -> list:
    """
    Generates human-readable AI reasoning explanations.
    This is the Explainable AI component — explains WHY the system
    made its recommendations.

    Args:
        role: Target job role (Prolog key)
        weak_skills: List of missing skills
        score: Readiness score (0-100)
        confidence: User's confidence level
        experience: User's experience level

    Returns:
        List of explanation strings
    """
    explanations = []
    role_name = role_to_display(role)
    skill_names = [skill_to_display(s) for s in weak_skills]

    # Explanation 1: Role-skill gap analysis
    if weak_skills:
        if len(skill_names) == 1:
            exp = (
                f"🔍 You selected **{role_name}** but are missing **{skill_names[0]}**. "
                f"This skill is commonly tested in {role_name} technical interviews."
            )
        else:
            exp = (
                f"🔍 You selected **{role_name}** but are missing "
                f"**{len(skill_names)} key skills**: {', '.join(skill_names[:3])}"
                f"{'...' if len(skill_names) > 3 else ''}. "
                f"These are frequently evaluated in {role_name} interviews."
            )
        explanations.append(exp)
    else:
        explanations.append(
            f"✅ You have all the required skills for **{role_name}**! "
            "Your score is primarily influenced by confidence and experience level."
        )

    # Explanation 2: Confidence impact
    if confidence == "low":
        explanations.append(
            "⚠️ Your **low confidence level** has reduced your readiness score. "
            "Interview performance is significantly impacted by confidence. "
            "Consider practice interviews to build self-assurance."
        )
    elif confidence == "medium":
        explanations.append(
            "📊 Your **moderate confidence** is factored into the readiness score. "
            "Consistent practice and mock interviews can help boost your confidence further."
        )
    else:
        explanations.append(
            "💪 Your **high confidence level** positively contributed to your score. "
            "Confidence is a key differentiator in interview performance."
        )

    # Explanation 3: Experience impact
    if experience == "fresher":
        explanations.append(
            "🎓 As a **fresher**, focus heavily on fundamentals, personal projects, "
            "and internship experience to strengthen your profile."
        )
    elif experience == "junior":
        explanations.append(
            "📈 Your **junior-level experience** is noted. Highlight your projects "
            "and demonstrate your learning curve to interviewers."
        )
    elif experience == "mid":
        explanations.append(
            "🚀 Your **mid-level experience** is a strong asset. "
            "Focus on demonstrating leadership, problem-solving, and impact in your work."
        )
    else:
        explanations.append(
            "🏅 Your **senior experience** is highly valuable. "
            "Be ready to discuss architecture decisions, mentorship, and strategic thinking."
        )

    # Explanation 4: Score interpretation
    if score >= 80:
        explanations.append(
            f"🏆 **Score {score}/100** — You are interview ready! "
            "Focus on final polish: practice behavioral questions and system design."
        )
    elif score >= 60:
        explanations.append(
            f"✅ **Score {score}/100** — You are almost ready. "
            "Targeted practice on weak areas will push you to full readiness."
        )
    elif score >= 40:
        explanations.append(
            f"⚡ **Score {score}/100** — Good foundation, but needs preparation. "
            "Dedicate focused time to the recommended topics before your interview."
        )
    else:
        explanations.append(
            f"📚 **Score {score}/100** — Significant preparation required. "
            "Follow the recommended study plan and practice regularly."
        )

    return explanations


def get_preparation_timeline(score: int, weak_skills_count: int) -> str:
    """
    Suggests a rough preparation timeline based on readiness score.

    Args:
        score: Readiness score
        weak_skills_count: Number of weak skills

    Returns:
        Preparation timeline string
    """
    if score >= 80:
        return "1-2 weeks of light review and mock practice"
    elif score >= 60:
        return f"2-4 weeks (focus on {weak_skills_count} weak area(s))"
    elif score >= 40:
        return f"1-2 months of structured study (covering {weak_skills_count} topics)"
    else:
        return f"2-3 months of intensive preparation across {weak_skills_count} skill areas"


def format_skill_list_for_prolog(skills_display: list) -> list:
    """
    Converts a list of display skill names to Prolog-compatible keys.

    Args:
        skills_display: List of display names (e.g., ['Python', 'SQL & Databases'])

    Returns:
        List of Prolog atom strings (e.g., ['python', 'sql'])
    """
    return [display_to_skill(s) for s in skills_display]


def all_role_options() -> list:
    """Returns all role display names for use in UI dropdowns."""
    return list(ROLE_DISPLAY_NAMES.values())


def all_skill_options() -> list:
    """Returns all skill display names for use in UI multiselects."""
    return list(SKILL_DISPLAY_NAMES.values())


def confidence_options() -> dict:
    """Returns confidence options mapping for UI."""
    return CONFIDENCE_DISPLAY


def experience_options() -> dict:
    """Returns experience options mapping for UI."""
    return EXPERIENCE_DISPLAY
