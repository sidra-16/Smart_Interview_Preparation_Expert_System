"""
app.py  — Smart Interview Preparation Expert System
Main Streamlit application entry point.
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(__file__))

from assets.styles import DARK_THEME_CSS
from utils.helpers import (
    all_role_options, all_skill_options,
    display_to_role, display_to_skill,
    role_to_display, skill_to_display,
    generate_ai_explanation, get_preparation_timeline,
    get_score_color, get_score_emoji,
    CONFIDENCE_DISPLAY, EXPERIENCE_DISPLAY
)
from utils.prolog_engine import (
    get_weak_skills, get_recommendations,
    get_readiness_score, get_high_priority_weak_skills,
    get_role_match_percent, get_alternative_role
)
from utils.question_bank import (
    get_questions_for_skill, get_hr_questions,
    get_questions_for_role_and_weak_skills, evaluate_answer
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Interview Prep | AI Expert System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
for key, default in {
    "page": "home",
    "assessment_done": False,
    "role_key": "",
    "user_skills": [],
    "confidence": "medium",
    "experience": "junior",
    "weak_skills": [],
    "recommendations": [],
    "readiness": {},
    "mock_questions": [],
    "mock_idx": 0,
    "mock_answers": [],
    "mock_done": False,
    "mock_started": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🎯 Interview Prep AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Expert System Powered by Prolog</div>', unsafe_allow_html=True)
    st.markdown("---")

    pages = {
        "🏠  Home":              "home",
        "📋  Skill Assessment":  "assessment",
        "📊  AI Results":        "results",
        "🎤  Mock Interview":    "mock",
    }

    for label, page_key in pages.items():
        active = st.session_state.page == page_key
        if st.button(label, use_container_width=True, key=f"nav_{page_key}",
                     type="primary" if active else "secondary"):
            st.session_state.page = page_key
            st.rerun()

    st.markdown("---")
    if st.session_state.assessment_done:
        st.markdown("**Current Profile**")
        st.markdown(f"🎯 Role: `{role_to_display(st.session_state.role_key)}`")
        st.markdown(f"✅ Skills: `{len(st.session_state.user_skills)}`")
        score = st.session_state.readiness.get("score", 0)
        cat   = st.session_state.readiness.get("category", "")
        st.markdown(f"📊 Score: `{score}/100`")
        st.progress(score / 100)
        st.markdown(f"_{cat}_")
    else:
        st.info("Complete the Skill Assessment to see your profile.")

    st.markdown("---")
    st.markdown('<div style="color:#8b949e;font-size:0.75rem;">AI Expert System · Prolog · PySwip<br>Knowledge Repr. · Backward Chaining</div>',
                unsafe_allow_html=True)


# ── Helper: go to page ────────────────────────────────────────────────────────
def go_to(page):
    st.session_state.page = page
    st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═════════════════════════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🎯 Smart Interview Preparation</div>
        <div class="hero-subtitle">AI-Powered Expert System using Prolog Knowledge Representation & Backward Chaining</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    tiles = [
        ("🧠", "AI Reasoning", "Prolog backward chaining & unification"),
        ("📋", "Skill Gap Analysis", "Identify missing skills for your target role"),
        ("❓", "Practice Questions", "Curated technical & HR questions"),
        ("🎤", "Mock Interview", "Interactive Q&A with instant feedback"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], tiles):
        col.markdown(f"""
        <div class="metric-tile">
            <div style="font-size:2rem">{icon}</div>
            <div style="font-size:0.95rem;font-weight:700;color:#e6edf3;margin-top:0.5rem">{title}</div>
            <div style="font-size:0.78rem;color:#8b949e;margin-top:0.4rem">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="section-header">🤖 How the AI Expert System Works</div>', unsafe_allow_html=True)
        for step, (icon, title, body) in enumerate([
            ("📝", "Input Assessment", "You provide your target role, technical skills, confidence, and experience level."),
            ("⚙️", "Prolog Reasoning", "The SWI-Prolog engine applies backward chaining to identify skill gaps and compute your readiness score using weighted rules."),
            ("💡", "AI Recommendations", "The system unifies your profile against the knowledge base to generate tailored preparation advice."),
            ("🎤", "Mock Practice", "Practice with role-specific questions and receive instant keyword-matching feedback."),
        ], 1):
            st.markdown(f"""
            <div class="card" style="margin-bottom:0.6rem">
                <div style="display:flex;gap:0.8rem;align-items:flex-start">
                    <div style="font-size:1.5rem">{icon}</div>
                    <div>
                        <div style="font-weight:700;color:#e6edf3;font-size:0.95rem">{step}. {title}</div>
                        <div style="color:#8b949e;font-size:0.85rem;margin-top:0.2rem">{body}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">🏛️ AI Concepts Demonstrated</div>', unsafe_allow_html=True)
        for concept, detail in [
            ("Knowledge Representation", "Facts and rules stored in Prolog knowledge base"),
            ("Backward Chaining", "Prolog queries goals backward to find skill gaps"),
            ("Unification", "Prolog unifies role requirements with user skills"),
            ("Rule-Based Reasoning", "Weighted rules compute readiness score"),
            ("Expert System", "Domain knowledge encoded as inference rules"),
            ("Explainable AI", "System explains WHY each recommendation is made"),
        ]:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #30363d;border-radius:10px;
                        padding:0.75rem 1rem;margin-bottom:0.5rem">
                <div style="font-size:0.82rem;font-weight:600;color:#6C63FF">✦ {concept}</div>
                <div style="font-size:0.78rem;color:#8b949e;margin-top:0.2rem">{detail}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        if st.button("🚀  Start Your Assessment", use_container_width=True):
            go_to("assessment")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: SKILL ASSESSMENT
# ═════════════════════════════════════════════════════════════════════════════
def page_assessment():
    st.markdown('<div class="section-header">📋 Skill Assessment Form</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#8b949e;margin-bottom:1.5rem">Fill in your details — the Prolog AI engine will analyze your profile.</div>', unsafe_allow_html=True)

    with st.form("assessment_form"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Target Role")
        role_display = st.selectbox("Select your target job role",
                                    all_role_options(), label_visibility="collapsed")

        st.markdown("#### 🛠️ Your Technical Skills")
        st.markdown('<div style="color:#8b949e;font-size:0.85rem;margin-bottom:0.5rem">Select all skills you are comfortable with</div>', unsafe_allow_html=True)
        selected_skills_display = st.multiselect("Skills", all_skill_options(), label_visibility="collapsed")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 💪 Confidence Level")
            conf_display = st.selectbox("Confidence", list(CONFIDENCE_DISPLAY.values()), label_visibility="collapsed")
        with col2:
            st.markdown("#### 🏅 Experience Level")
            exp_display = st.selectbox("Experience", list(EXPERIENCE_DISPLAY.values()), label_visibility="collapsed")

        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("🧠  Run AI Analysis", use_container_width=True)

    if submitted:
        # Map display → Prolog keys
        role_key  = display_to_role(role_display)
        skill_keys = [display_to_skill(s) for s in selected_skills_display]
        conf_key  = {v: k for k, v in CONFIDENCE_DISPLAY.items()}[conf_display]
        exp_key   = {v: k for k, v in EXPERIENCE_DISPLAY.items()}[exp_display]

        with st.spinner("🔍 Prolog reasoning engine analyzing your profile..."):
            weak     = get_weak_skills(role_key, skill_keys)
            recs     = get_recommendations(role_key, weak)
            readiness = get_readiness_score(role_key, skill_keys, conf_key, exp_key)

        # Persist to session state
        st.session_state.role_key      = role_key
        st.session_state.user_skills   = skill_keys
        st.session_state.confidence    = conf_key
        st.session_state.experience    = exp_key
        st.session_state.weak_skills   = weak
        st.session_state.recommendations = recs
        st.session_state.readiness     = readiness
        st.session_state.assessment_done = True

        # Reset mock interview
        st.session_state.mock_questions = []
        st.session_state.mock_idx  = 0
        st.session_state.mock_answers = []
        st.session_state.mock_done = False
        st.session_state.mock_started = False

        st.success("✅ Analysis complete! Redirecting to your AI Results Dashboard...")
        go_to("results")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: AI RESULTS DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
def page_results():
    if not st.session_state.assessment_done:
        st.warning("Please complete the Skill Assessment first.")
        if st.button("Go to Assessment"):
            go_to("assessment")
        return

    role_key  = st.session_state.role_key
    user_skills = st.session_state.user_skills
    weak_skills = st.session_state.weak_skills
    recs        = st.session_state.recommendations
    readiness   = st.session_state.readiness
    confidence  = st.session_state.confidence
    experience  = st.session_state.experience

    score    = readiness.get("score", 0)
    category = readiness.get("category", "")
    score_deg = int(score * 3.6)

    st.markdown('<div class="section-header">📊 AI Results Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#8b949e;margin-bottom:1rem">Analysis for <strong style="color:#6C63FF">{role_to_display(role_key)}</strong></div>', unsafe_allow_html=True)

    # ── Row 1: Score ring + metrics ──────────────────────────────────────────
    col_score, col_m1, col_m2, col_m3 = st.columns([2, 1, 1, 1])

    with col_score:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div style="font-size:0.82rem;color:#8b949e;margin-bottom:0.8rem;font-weight:600;text-transform:uppercase;letter-spacing:1px">Readiness Score</div>
            <div class="score-ring" style="--score-deg:{score_deg}deg">
                <div class="score-inner">
                    <div class="score-number">{get_score_emoji(score)} {score}</div>
                    <div class="score-pct">out of 100</div>
                </div>
            </div>
            <div style="font-size:1rem;font-weight:700;color:{get_score_color(score)};margin-top:0.8rem">{category}</div>
        </div>""", unsafe_allow_html=True)

    for col, (val, label, color) in zip(
        [col_m1, col_m2, col_m3],
        [
            (len(weak_skills), "Weak Areas", "#FF6584"),
            (len(user_skills), "Skills You Have", "#43C6AC"),
            (f"{get_preparation_timeline(score, len(weak_skills)).split()[0]}", "Est. Prep Time", "#F7971E"),
        ]
    ):
        col.markdown(f"""
        <div class="metric-tile" style="height:100%">
            <div class="metric-value" style="color:{color}">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Skill analysis ────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">❌ Weak / Missing Skills</div>', unsafe_allow_html=True)
        if weak_skills:
            hp = get_high_priority_weak_skills(role_key, weak_skills)
            for skill in weak_skills:
                priority = "🔴 High Priority" if skill in hp else "🟡 Medium Priority"
                st.markdown(f"""
                <div class="rec-card">
                    <span class="skill-tag-weak">{skill_to_display(skill)}</span>
                    <span style="font-size:0.72rem;color:#8b949e;margin-left:0.5rem">{priority}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-good" style="color:#43C6AC">✅ You have all required skills for this role!</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header">✅ Skills You Have</div>', unsafe_allow_html=True)
        req_all = set(weak_skills + user_skills)
        for skill in user_skills:
            st.markdown(f'<span class="skill-tag-strong">{skill_to_display(skill)}</span>', unsafe_allow_html=True)
        if not user_skills:
            st.markdown('<div style="color:#8b949e">No skills selected.</div>', unsafe_allow_html=True)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ── Row 3: Progress bars ─────────────────────────────────────────────────
    match_pct = get_role_match_percent(role_key, user_skills)
    st.markdown('<div class="section-header">📈 Skill Coverage Progress</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Role Skill Match**")
        st.progress(match_pct / 100)
        st.caption(f"{match_pct}% of required skills covered")
    with col_b:
        st.markdown("**Interview Readiness**")
        st.progress(score / 100)
        st.caption(f"{score}% — {category}")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ── Row 4: Recommendations ───────────────────────────────────────────────
    st.markdown('<div class="section-header">💡 AI Preparation Recommendations</div>', unsafe_allow_html=True)
    if recs:
        for rec in recs:
            st.markdown(f"""
            <div class="rec-card">
                <div class="rec-skill">📚 {skill_to_display(rec["skill"])}</div>
                <div class="rec-text">{rec["recommendation"]}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.success("🏆 No additional preparation needed — you have all required skills!")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ── Row 5: Explainable AI ────────────────────────────────────────────────
    st.markdown('<div class="section-header">🤖 Why the AI Recommended This</div>', unsafe_allow_html=True)
    explanations = generate_ai_explanation(role_key, weak_skills, score, confidence, experience)
    for exp in explanations:
        st.markdown(f'<div class="explanation-box">{exp}</div>', unsafe_allow_html=True)

    # Prep timeline
    timeline = get_preparation_timeline(score, len(weak_skills))
    st.markdown(f"""
    <div class="gradient-card">
        <div style="font-size:0.82rem;color:#6C63FF;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">⏱️ Estimated Preparation Timeline</div>
        <div style="font-size:1.1rem;font-weight:700;color:#e6edf3;margin-top:0.4rem">{timeline}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ── Row 6: Practice Questions Preview ───────────────────────────────────
    st.markdown('<div class="section-header">❓ Practice Questions Preview</div>', unsafe_allow_html=True)
    preview_skills = weak_skills[:2] if weak_skills else user_skills[:2]
    for skill in preview_skills:
        qs = get_questions_for_skill(skill, 1)
        for q in qs:
            st.markdown(f"""
            <div class="q-card">
                <div class="q-number">📌 {skill_to_display(skill)}</div>
                <div class="q-text">{q["question"]}</div>
                <div class="q-difficulty">Difficulty: {q.get("difficulty","").title()}</div>
            </div>""", unsafe_allow_html=True)

    colb1, colb2 = st.columns(2)
    with colb1:
        if st.button("🎤  Start Mock Interview", use_container_width=True):
            go_to("mock")
    with colb2:
        if st.button("🔄  Redo Assessment", use_container_width=True):
            go_to("assessment")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: MOCK INTERVIEW
# ═════════════════════════════════════════════════════════════════════════════
def page_mock():
    if not st.session_state.assessment_done:
        st.warning("Please complete the Skill Assessment first.")
        if st.button("Go to Assessment"):
            go_to("assessment")
        return

    st.markdown('<div class="section-header">🎤 Mock Interview Session</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#8b949e;margin-bottom:1.5rem">Practice your answers — the AI will give instant keyword-based feedback.</div>', unsafe_allow_html=True)

    # ── Setup questions if not started ────────────────────────────────────────
    if not st.session_state.mock_started:
        role_key    = st.session_state.role_key
        weak_skills = st.session_state.weak_skills
        user_skills = st.session_state.user_skills
        target_skills = (weak_skills + user_skills)[:4]

        all_qs = []
        for sk in target_skills[:3]:
            qs = get_questions_for_skill(sk, 2)
            all_qs.extend(qs)
        all_qs.extend(get_hr_questions(2))

        st.session_state.mock_questions = all_qs[:8]
        st.session_state.mock_idx       = 0
        st.session_state.mock_answers   = []
        st.session_state.mock_done      = False

        col_info = st.columns([2, 1])[0]
        with col_info:
            st.markdown(f"""
            <div class="gradient-card">
                <div style="font-size:1rem;font-weight:700;color:#e6edf3">📋 Session Overview</div>
                <div style="color:#8b949e;font-size:0.9rem;margin-top:0.5rem">
                    {len(st.session_state.mock_questions)} questions covering your weak areas and HR topics.<br>
                    Type your answer, then click <strong>Submit Answer</strong>.
                </div>
            </div>""", unsafe_allow_html=True)

        if st.button("▶️  Begin Mock Interview", use_container_width=False):
            st.session_state.mock_started = True
            st.rerun()
        return

    # ── Interview in progress ─────────────────────────────────────────────────
    questions = st.session_state.mock_questions
    idx       = st.session_state.mock_idx
    total     = len(questions)

    if not st.session_state.mock_done and idx < total:
        q = questions[idx]

        # Progress
        st.progress((idx) / total)
        st.markdown(f'<div style="color:#8b949e;font-size:0.85rem;margin-bottom:1rem">Question {idx+1} of {total}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="q-card">
            <div class="q-number">Question {idx+1}</div>
            <div class="q-text">💬 {q["question"]}</div>
            <div class="q-difficulty">Difficulty: {q.get("difficulty","").title()}</div>
        </div>""", unsafe_allow_html=True)

        answer = st.text_area("Your Answer:", height=130, key=f"ans_{idx}",
                              placeholder="Type your answer here...")

        col_sub, col_skip = st.columns([2, 1])
        with col_sub:
            if st.button("✅  Submit Answer", use_container_width=True):
                result = evaluate_answer(q, answer)
                st.session_state.mock_answers.append({
                    "question": q["question"], "answer": answer, "result": result
                })
                st.session_state.mock_idx += 1
                if st.session_state.mock_idx >= total:
                    st.session_state.mock_done = True
                st.rerun()
        with col_skip:
            if st.button("⏭️  Skip", use_container_width=True):
                st.session_state.mock_answers.append({
                    "question": q["question"], "answer": "", "result": evaluate_answer(q, "")
                })
                st.session_state.mock_idx += 1
                if st.session_state.mock_idx >= total:
                    st.session_state.mock_done = True
                st.rerun()

    # ── Show previous answers inline ─────────────────────────────────────────
    if st.session_state.mock_answers and not st.session_state.mock_done:
        with st.expander("📜 See Previous Answers"):
            for i, entry in enumerate(st.session_state.mock_answers):
                res = entry["result"]
                score_val = res["score"]
                css_class = "feedback-good" if score_val >= 70 else ("feedback-ok" if score_val >= 40 else "feedback-poor")
                st.markdown(f"**Q{i+1}:** {entry['question']}")
                st.markdown(f'<div class="{css_class}">{res["feedback"]}</div>', unsafe_allow_html=True)
                st.markdown("---")

    # ── Final results ─────────────────────────────────────────────────────────
    if st.session_state.mock_done:
        answers = st.session_state.mock_answers
        scores  = [a["result"]["score"] for a in answers if a["answer"]]
        avg     = int(sum(scores) / len(scores)) if scores else 0

        st.markdown(f"""
        <div class="hero-banner" style="margin-bottom:1.5rem">
            <div class="hero-title">{get_score_emoji(avg)} Mock Interview Complete!</div>
            <div class="hero-subtitle">Average Score: {avg}/100 — {avg >= 70 and "Great Job!" or avg >= 40 and "Keep Practising!" or "More Study Needed"}</div>
        </div>""", unsafe_allow_html=True)

        st.progress(avg / 100)

        for i, entry in enumerate(answers):
            res   = entry["result"]
            sc    = res["score"]
            css   = "feedback-good" if sc >= 70 else ("feedback-ok" if sc >= 40 else "feedback-poor")
            st.markdown(f"""
            <div class="card">
                <div style="font-size:0.8rem;color:#8b949e">Question {i+1}</div>
                <div style="font-weight:600;color:#e6edf3;margin:0.3rem 0">{entry["question"]}</div>
                <div style="font-size:0.85rem;color:#8b949e;margin-bottom:0.5rem"><em>Your answer:</em> {entry["answer"] or "_(skipped)_"}</div>
                <div class="{css}">{res["feedback"]}</div>
                <div style="margin-top:0.5rem;font-size:0.82rem;color:#8b949e">
                    💡 <strong>Sample answer:</strong> {res.get("sample_answer","")}
                </div>
            </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁  Retry Mock Interview", use_container_width=True):
                st.session_state.mock_started = False
                st.rerun()
        with col2:
            if st.button("📊  View AI Results", use_container_width=True):
                go_to("results")


# ═════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═════════════════════════════════════════════════════════════════════════════
page = st.session_state.page
if page == "home":
    page_home()
elif page == "assessment":
    page_assessment()
elif page == "results":
    page_results()
elif page == "mock":
    page_mock()
