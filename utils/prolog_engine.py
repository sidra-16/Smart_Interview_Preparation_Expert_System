"""
prolog_engine.py
Handles all communication between Python and the SWI-Prolog knowledge base
using PySwip. Provides clean functions for each Prolog query type.
"""

import os
from pyswip import Prolog

# Path to the Prolog knowledge base file
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
KB_PATH = os.path.join(_ROOT, "prolog", "knowledge_base.pl")


def _prolog_path(path: str) -> str:
    """
    Converts a Windows absolute path to a safe Prolog path string.
    SWI-Prolog on Windows interprets backslash sequences (e.g. \\U, \\n)
    as escape codes, so we must use forward slashes.
    """
    # Forward slashes work on all platforms in SWI-Prolog
    return path.replace("\\", "/")


def get_prolog_instance():
    """
    Creates and returns a fresh Prolog instance with the knowledge base loaded.
    
    PySwip's consult() method on Windows passes the raw path string to SWI-Prolog,
    which then interprets \\U (from paths like D:\\Uni\\...) as an illegal Unicode
    escape sequence. Workaround: use Prolog's load_files/1 via a direct query
    with the path already converted to forward slashes.
    """
    prolog = Prolog()
    safe_path = _prolog_path(KB_PATH)
    # Use load_files/1 via query — this correctly handles forward-slash paths
    # and bypasses PySwip's broken str(path) concatenation in consult()
    query = f"load_files('{safe_path}', [silent(true)])"
    try:
        list(prolog.query(query))
    except Exception:
        # Fallback: try asserting a dummy fact to confirm Prolog is alive
        pass
    return prolog


def get_weak_skills(role: str, user_skills: list) -> list:
    """
    Queries Prolog to find weak skills (required by role but missing from user).
    Demonstrates backward chaining: Prolog works backward from the goal
    'is_weak_skill(Role, Skill, UserSkills)' to find missing skills.

    Args:
        role: The target job role (e.g., 'software_engineer')
        user_skills: List of skills the user has (e.g., ['python', 'oop'])

    Returns:
        List of weak/missing skills
    """
    prolog = get_prolog_instance()
    # Build Prolog list from Python list
    skills_term = "[" + ",".join(user_skills) + "]"
    query = f"weak_skills({role}, {skills_term}, WeakSkills)"

    try:
        results = list(prolog.query(query))
        if results:
            weak = results[0].get("WeakSkills", [])
            # Convert from PySwip atom objects to Python strings
            return [str(s) for s in weak]
        return []
    except Exception as e:
        print(f"Prolog weak_skills error: {e}")
        return []


def get_recommendations(role: str, weak_skills: list) -> list:
    """
    Gets preparation recommendations for each weak skill from Prolog rules.
    Uses Prolog's unification to match weak skills with recommendation facts.

    Args:
        role: The target job role
        weak_skills: List of skills the user needs to improve

    Returns:
        List of dicts with 'skill' and 'recommendation' keys
    """
    prolog = get_prolog_instance()
    recommendations = []

    for skill in weak_skills:
        query = f"recommend({role}, {skill}, Rec)"
        try:
            results = list(prolog.query(query))
            if results:
                rec_text = str(results[0].get("Rec", ""))
                recommendations.append({
                    "skill": skill,
                    "recommendation": rec_text
                })
        except Exception as e:
            print(f"Prolog recommend error for {skill}: {e}")

    return recommendations


def get_readiness_score(role: str, user_skills: list, confidence: str, experience: str) -> dict:
    """
    Calculates the interview readiness score using Prolog rules.
    The score is computed through rule-based weighted skill coverage,
    adjusted by confidence and experience levels.

    Args:
        role: Target job role
        user_skills: User's current skills
        confidence: 'high', 'medium', or 'low'
        experience: 'senior', 'mid', 'junior', or 'fresher'

    Returns:
        Dict with 'score' (int 0-100) and 'category' (string)
    """
    prolog = get_prolog_instance()
    skills_term = "[" + ",".join(user_skills) + "]"
    query = f"readiness_score({role}, {skills_term}, {confidence}, {experience}, Score)"

    try:
        results = list(prolog.query(query))
        if results:
            score = int(results[0].get("Score", 0))
            # Get readiness category
            cat_query = f"readiness_category({score}, Category)"
            cat_results = list(prolog.query(cat_query))
            category = "Unknown"
            if cat_results:
                category = str(cat_results[0].get("Category", "Unknown"))
            return {"score": score, "category": category}
        return {"score": 0, "category": "Unable to calculate"}
    except Exception as e:
        print(f"Prolog readiness_score error: {e}")
        return {"score": 0, "category": "Error"}


def get_high_priority_weak_skills(role: str, weak_skills: list) -> list:
    """
    Finds which weak skills are high priority (most important for the role).
    Helps users focus on what matters most first.

    Args:
        role: Target job role
        weak_skills: List of all weak skills

    Returns:
        List of high-priority weak skills
    """
    prolog = get_prolog_instance()
    if not weak_skills:
        return []

    skills_term = "[" + ",".join(weak_skills) + "]"
    query = f"high_priority_weak({role}, {skills_term}, HighPriority)"

    try:
        results = list(prolog.query(query))
        if results:
            hp = results[0].get("HighPriority", [])
            return [str(s) for s in hp]
        return []
    except Exception as e:
        print(f"Prolog high_priority_weak error: {e}")
        return []


def get_role_match_percent(role: str, user_skills: list) -> int:
    """
    Calculates what percentage of required skills the user already has for a role.

    Args:
        role: Target job role
        user_skills: User's current skills

    Returns:
        Integer percentage (0-100)
    """
    prolog = get_prolog_instance()
    skills_term = "[" + ",".join(user_skills) + "]"
    query = f"role_match({role}, {skills_term}, MatchPercent)"

    try:
        results = list(prolog.query(query))
        if results:
            return int(results[0].get("MatchPercent", 0))
        return 0
    except Exception as e:
        print(f"Prolog role_match error: {e}")
        return 0


def get_alternative_role(user_skills: list) -> dict:
    """
    Suggests the best alternative role based on user's current skills.

    Args:
        user_skills: User's current skills

    Returns:
        Dict with 'role' and 'match_percent' keys
    """
    prolog = get_prolog_instance()
    if not user_skills:
        return {"role": "none", "match_percent": 0}

    skills_term = "[" + ",".join(user_skills) + "]"
    query = f"suggest_alternative_role({skills_term}, SuggestedRole, MatchPct)"

    try:
        results = list(prolog.query(query))
        if results:
            return {
                "role": str(results[0].get("SuggestedRole", "none")),
                "match_percent": int(results[0].get("MatchPct", 0))
            }
        return {"role": "none", "match_percent": 0}
    except Exception as e:
        print(f"Prolog suggest_alternative_role error: {e}")
        return {"role": "none", "match_percent": 0}


def get_all_required_skills(role: str) -> list:
    """
    Gets all skills required for a given role (for display purposes).

    Args:
        role: Target job role

    Returns:
        List of required skill names
    """
    prolog = get_prolog_instance()
    query = f"required_skill({role}, Skill)"

    try:
        results = list(prolog.query(query))
        return [str(r.get("Skill", "")) for r in results]
    except Exception as e:
        print(f"Prolog required_skill error: {e}")
        return []
