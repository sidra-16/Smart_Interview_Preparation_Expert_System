"""
styles.py  – All CSS injected into the Streamlit app.
"""

DARK_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ─── Global Reset ─── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.main { background: #0d1117; }
section[data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #30363d; }
section[data-testid="stSidebar"] * { color: #e6edf3 !important; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ─── Hide Streamlit Branding ─── */
#MainMenu, footer, header { visibility: hidden; }

/* ─── Sidebar nav label ─── */
.sidebar-title {
    font-size: 1.3rem; font-weight: 700;
    background: linear-gradient(135deg, #6C63FF, #43C6AC);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.sidebar-subtitle { font-size: 0.78rem; color: #8b949e; margin-bottom: 1.5rem; }

/* ─── Cards ─── */
.card {
    background: #161b22; border: 1px solid #30363d; border-radius: 14px;
    padding: 1.4rem 1.6rem; margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.card-accent {
    background: linear-gradient(135deg, #1a1f2e, #1e2433);
    border: 1px solid #6C63FF55; border-radius: 14px;
    padding: 1.4rem 1.6rem; margin-bottom: 1rem;
}
.gradient-card {
    background: linear-gradient(135deg, #6C63FF22, #43C6AC22);
    border: 1px solid #6C63FF44; border-radius: 14px;
    padding: 1.4rem 1.6rem; margin-bottom: 1rem;
}

/* ─── Hero Banner ─── */
.hero-banner {
    background: linear-gradient(135deg, #6C63FF, #43C6AC);
    border-radius: 16px; padding: 2.5rem 2rem; margin-bottom: 2rem;
    text-align: center;
}
.hero-title { font-size: 2.2rem; font-weight: 800; color: #fff; margin: 0; }
.hero-subtitle { font-size: 1rem; color: rgba(255,255,255,0.88); margin-top: 0.5rem; }

/* ─── Section Headers ─── */
.section-header {
    font-size: 1.25rem; font-weight: 700; color: #e6edf3;
    border-left: 4px solid #6C63FF; padding-left: 0.75rem;
    margin-bottom: 1rem; margin-top: 0.5rem;
}

/* ─── Metric Tiles ─── */
.metric-tile {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 1.2rem; text-align: center;
}
.metric-value { font-size: 2rem; font-weight: 800; color: #6C63FF; }
.metric-label { font-size: 0.8rem; color: #8b949e; margin-top: 0.2rem; }

/* ─── Skill Tags ─── */
.skill-tag {
    display: inline-block; background: #21262d; border: 1px solid #30363d;
    border-radius: 20px; padding: 0.25rem 0.75rem; margin: 0.2rem;
    font-size: 0.8rem; color: #e6edf3;
}
.skill-tag-weak {
    display: inline-block; background: #3d1a1a; border: 1px solid #FF6584;
    border-radius: 20px; padding: 0.25rem 0.75rem; margin: 0.2rem;
    font-size: 0.8rem; color: #FF6584;
}
.skill-tag-strong {
    display: inline-block; background: #1a3d2b; border: 1px solid #43C6AC;
    border-radius: 20px; padding: 0.25rem 0.75rem; margin: 0.2rem;
    font-size: 0.8rem; color: #43C6AC;
}

/* ─── Score Ring ─── */
.score-ring {
    width: 130px; height: 130px; border-radius: 50%;
    background: conic-gradient(#6C63FF var(--score-deg), #21262d 0);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 0.5rem;
    box-shadow: 0 0 30px #6C63FF44;
}
.score-inner {
    width: 100px; height: 100px; border-radius: 50%;
    background: #161b22; display: flex; align-items: center;
    justify-content: center; flex-direction: column;
}
.score-number { font-size: 1.6rem; font-weight: 800; color: #e6edf3; }
.score-pct { font-size: 0.7rem; color: #8b949e; }

/* ─── Explanation Box ─── */
.explanation-box {
    background: #1a1f2e; border-left: 4px solid #6C63FF;
    border-radius: 0 10px 10px 0; padding: 1rem 1.2rem;
    margin-bottom: 0.75rem; color: #c9d1d9; font-size: 0.9rem;
    line-height: 1.6;
}

/* ─── Rec Card ─── */
.rec-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 1rem 1.2rem; margin-bottom: 0.75rem;
}
.rec-skill { font-size: 0.75rem; font-weight: 600; color: #6C63FF; text-transform: uppercase; letter-spacing: 0.5px; }
.rec-text { font-size: 0.92rem; color: #c9d1d9; margin-top: 0.3rem; }

/* ─── Question Card ─── */
.q-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 1.2rem 1.4rem; margin-bottom: 1rem;
}
.q-number { font-size: 0.72rem; color: #6C63FF; font-weight: 600; text-transform: uppercase; }
.q-text { font-size: 1rem; font-weight: 600; color: #e6edf3; margin-top: 0.3rem; line-height: 1.5; }
.q-difficulty { font-size: 0.72rem; color: #8b949e; margin-top: 0.4rem; }

/* ─── Feedback Box ─── */
.feedback-good  { background:#1a3d2b; border:1px solid #43C6AC; border-radius:10px; padding:1rem; color:#43C6AC; }
.feedback-ok    { background:#2d2d1a; border:1px solid #F7971E; border-radius:10px; padding:1rem; color:#F7971E; }
.feedback-poor  { background:#3d1a1a; border:1px solid #FF6584; border-radius:10px; padding:1rem; color:#FF6584; }

/* ─── Buttons ─── */
div.stButton > button {
    background: linear-gradient(135deg, #6C63FF, #43C6AC) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    padding: 0.55rem 1.4rem !important; font-size: 0.95rem !important;
    transition: opacity 0.2s ease !important;
}
div.stButton > button:hover { opacity: 0.88 !important; }

/* ─── Inputs ─── */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextArea textarea {
    background: #161b22 !important; border: 1px solid #30363d !important;
    border-radius: 10px !important; color: #e6edf3 !important;
}
label[data-testid="stWidgetLabel"] { color: #c9d1d9 !important; font-weight: 500 !important; }

/* ─── Progress bar ─── */
.stProgress > div > div > div { background: linear-gradient(90deg, #6C63FF, #43C6AC) !important; border-radius: 10px; }

/* ─── Info / Warning ─── */
.stInfo, .stSuccess, .stWarning, .stError { border-radius: 10px !important; }

/* ─── Divider ─── */
.custom-divider { border: none; border-top: 1px solid #30363d; margin: 1.5rem 0; }
</style>
"""
