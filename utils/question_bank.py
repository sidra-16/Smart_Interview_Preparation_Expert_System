"""
question_bank.py
Loads and serves interview questions from the JSON database.
Provides filtering by skill, role, and difficulty level.
"""

import json
import os
import random

# Path to the questions data file
QUESTIONS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "questions.json"
)


def load_questions() -> dict:
    """Loads all questions from the JSON file."""
    try:
        with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading questions: {e}")
        return {"technical": {}, "hr": []}


def get_questions_for_skill(skill: str, count: int = 3) -> list:
    """
    Returns interview questions for a specific technical skill.

    Args:
        skill: Skill name (e.g., 'python', 'dsa', 'sql')
        count: Maximum number of questions to return

    Returns:
        List of question dictionaries
    """
    data = load_questions()
    skill_key = skill.lower().replace("-", "_").replace(" ", "_")

    # Map display skill names to JSON keys
    skill_map = {
        "html_css": "html_css",
        "javascript": "javascript",
        "python": "python",
        "dsa": "dsa",
        "oop": "oop",
        "sql": "sql",
        "git": "git",
        "figma": "figma",
        "user_research": "user_research",
        "statistics": "statistics",
        "excel": None,
        "visualization": None,
        "prototyping": None,
    }

    json_key = skill_map.get(skill_key, skill_key)
    if json_key is None:
        return []

    technical = data.get("technical", {})
    questions = technical.get(json_key, [])

    # Shuffle and return requested count
    shuffled = random.sample(questions, min(count, len(questions)))
    return shuffled


def get_hr_questions(count: int = 3) -> list:
    """
    Returns a selection of HR/behavioral interview questions.

    Args:
        count: Number of HR questions to return

    Returns:
        List of HR question dictionaries
    """
    data = load_questions()
    hr_questions = data.get("hr", [])
    return random.sample(hr_questions, min(count, len(hr_questions)))


def get_questions_for_role_and_weak_skills(role: str, weak_skills: list, max_per_skill: int = 2) -> dict:
    """
    Generates a curated question set based on role and weak skills.
    Prioritizes questions for skills the user needs to improve.

    Args:
        role: Target job role (for future role-specific filtering)
        weak_skills: List of skills the user is weak in
        max_per_skill: Max questions per skill

    Returns:
        Dict mapping skill to list of questions
    """
    question_set = {}

    for skill in weak_skills:
        questions = get_questions_for_skill(skill, max_per_skill)
        if questions:
            question_set[skill] = questions

    # Always include some HR questions
    question_set["hr"] = get_hr_questions(3)

    return question_set


def evaluate_answer(question: dict, user_answer: str) -> dict:
    """
    Evaluates a user's mock interview answer using keyword matching.
    This is the core of the mock interview feedback system.

    Args:
        question: Question dict with 'keywords' and 'sample_answer' fields
        user_answer: The user's typed answer

    Returns:
        Dict with 'score', 'feedback', 'matched_keywords', 'missed_keywords'
    """
    if not user_answer or not user_answer.strip():
        return {
            "score": 0,
            "feedback": "⚠️ No answer provided. Please type your response.",
            "matched_keywords": [],
            "missed_keywords": question.get("keywords", []),
            "rating": "No Answer"
        }

    keywords = question.get("keywords", [])
    answer_lower = user_answer.lower()

    matched = []
    missed = []

    for keyword in keywords:
        # Check if keyword (or its parts) appear in the answer
        keyword_lower = keyword.lower()
        if keyword_lower in answer_lower:
            matched.append(keyword)
        else:
            # Check for partial word matches for multi-word keywords
            parts = keyword_lower.split()
            if len(parts) > 1 and any(part in answer_lower for part in parts if len(part) > 3):
                matched.append(keyword)
            else:
                missed.append(keyword)

    total = len(keywords)
    if total == 0:
        score = 50
    else:
        score = int((len(matched) / total) * 100)

    # Generate feedback based on score
    if score >= 80:
        rating = "Excellent"
        feedback = "✅ **Excellent answer!** You covered the key concepts well."
    elif score >= 60:
        rating = "Good"
        feedback = "👍 **Good answer!** You captured most important points."
    elif score >= 40:
        rating = "Fair"
        feedback = "⚡ **Fair answer.** You have the right idea but could add more detail."
    else:
        rating = "Needs Improvement"
        feedback = "📚 **Needs improvement.** Review the key concepts for this topic."

    if missed:
        feedback += f"\n\n**Missing concepts:** {', '.join(missed)}"

    return {
        "score": score,
        "feedback": feedback,
        "matched_keywords": matched,
        "missed_keywords": missed,
        "rating": rating,
        "sample_answer": question.get("sample_answer", "")
    }


def get_all_skills() -> list:
    """Returns a list of all available technical skills in the question bank."""
    data = load_questions()
    return list(data.get("technical", {}).keys())
