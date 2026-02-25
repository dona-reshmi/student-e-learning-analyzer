import streamlit as st
import joblib
import numpy as np

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="EduPulse · Student Analyzer",
    page_icon="🎓",
    layout="wide"
)

# --------------------------
# CUSTOM CSS — Luxury Academic Dark Theme
# --------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background-color: #080c14;
    background-image:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(99,179,237,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 40% 40% at 85% 80%, rgba(159,122,234,0.08) 0%, transparent 60%);
    font-family: 'DM Sans', sans-serif;
    color: #e8eaf0;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1100px; }

/* ---- HERO ---- */
.hero-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 20px 20px;
    position: relative;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(42px, 6vw, 72px);
    font-weight: 900;
    line-height: 1.05;
    text-align: center;
    background: linear-gradient(135deg, #ffffff 30%, #63b3ed 70%, #9f7aea 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px;
}
.hero-sub {
    font-size: 16px;
    color: #8892a4;
    text-align: center;
    max-width: 520px;
    line-height: 1.6;
    font-weight: 300;
    margin-bottom: 40px;
}

/* ---- DIVIDER ---- */
.divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,179,237,0.3), transparent);
    margin: 10px 0 36px;
}

/* ---- SECTION LABELS ---- */
.section-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(99,179,237,0.2);
}

/* ---- METRIC CARDS (above sliders) ---- */
.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px 22px;
    transition: border-color 0.3s;
}
.metric-card:hover { border-color: rgba(99,179,237,0.3); }
.metric-icon { font-size: 22px; margin-bottom: 8px; }
.metric-title { font-size: 11px; color: #8892a4; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }
.metric-hint { font-size: 13px; color: #c5cad8; font-weight: 300; }

/* ---- GLASS PANEL ---- */
.glass-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 32px 32px 24px;
    margin-bottom: 28px;
    backdrop-filter: blur(10px);
}

/* ---- SLIDERS ---- */
div[data-baseweb="slider"] label,
.stSlider label { color: #c5cad8 !important; font-size: 14px !important; }
div[data-baseweb="slider"] [data-testid="stThumbValue"] { color: #63b3ed !important; }

/* ---- SELECTBOX ---- */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8eaf0 !important;
}

/* ---- BUTTON ---- */
.stButton > button {
    background: linear-gradient(135deg, #2b6cb0, #4299e1, #7b5ea7);
    background-size: 200% 200%;
    animation: gradshift 4s ease infinite;
    color: white;
    border: none;
    padding: 14px 44px;
    font-size: 15px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border-radius: 50px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    width: 100%;
    margin-top: 10px;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(66,153,225,0.35);
}
@keyframes gradshift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ---- RESULT CARDS ---- */
.result-high {
    background: linear-gradient(135deg, rgba(72,187,120,0.12), rgba(56,161,105,0.05));
    border: 1px solid rgba(72,187,120,0.3);
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    animation: fadeUp 0.5s ease;
}
.result-mid {
    background: linear-gradient(135deg, rgba(236,201,75,0.1), rgba(214,158,46,0.05));
    border: 1px solid rgba(236,201,75,0.3);
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    animation: fadeUp 0.5s ease;
}
.result-low {
    background: linear-gradient(135deg, rgba(252,129,74,0.12), rgba(229,62,62,0.05));
    border: 1px solid rgba(229,62,62,0.3);
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    animation: fadeUp 0.5s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-icon { font-size: 56px; margin-bottom: 12px; }
.result-label {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 8px;
    color: #f0f4ff;
}
.result-conf {
    font-size: 13px;
    color: #8892a4;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.conf-bar-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 50px;
    height: 6px;
    margin: 16px auto;
    max-width: 260px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #63b3ed, #9f7aea);
    transition: width 1s ease;
}

/* ---- FOOTER ---- */
.footer {
    text-align: center;
    padding: 40px 0 10px;
    font-size: 12px;
    color: #3d4a5c;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# HERO
# --------------------------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">EduPulse</div>
    <div class="hero-sub">Intelligent analysis of student engagement patterns to predict academic performance with precision.</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# --------------------------
# METRIC HINT CARDS
# --------------------------
st.markdown("""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-title">Engagement Metrics</div>
        <div class="metric-hint">Rate classroom & online activity levels</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🧠</div>
        <div class="metric-title">AI Prediction</div>
        <div class="metric-hint">Model trained on thousands of student records</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🎯</div>
        <div class="metric-title">Instant Results</div>
        <div class="metric-hint">Get performance tier + confidence score</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------
# LOAD MODEL
# --------------------------
model = joblib.load("student_model.pkl")

# --------------------------
# INPUT PANEL
# --------------------------
st.markdown('<div class="section-label">Student Input Parameters</div>', unsafe_allow_html=True)

_, mid, _ = st.columns([0.5, 2, 0.5])

with mid:
    participation = st.slider("📌 Class Participation", 0, 100, 50,
                              help="How actively the student participates in class")
    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    online_activity = st.slider("💻 Online Study Activity", 0, 100, 50,
                                help="Hours or frequency of online study sessions")
    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    platform_engagement = st.slider("📢 Platform Engagement", 0, 50, 25,
                                    help="Activity score on the learning platform")
    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    discussion_activity = st.slider("🗣 Discussion Activity", 0, 100, 50,
                                    help="Forum posts, Q&A participation, and peer interaction")
    st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)

    attendance_label = st.selectbox(
        "📅 Attendance Record",
        ["Under 7 Absences ✅", "More than 7 Absences ⚠️"]
    )

absence_days = 1 if "Under 7" in attendance_label else 0

# --------------------------
# PREDICT
# --------------------------
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze = st.button("⚡ Analyze Performance")

if analyze:
    input_data = np.array([[1, 4, 4, 2, 1,
                            0, 7, 0, 0,
                            participation, online_activity,
                            platform_engagement, discussion_activity,
                            1, 1,
                            absence_days]])

    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)
    confidence = round(np.max(probabilities) * 100, 2)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Analysis Result</div>', unsafe_allow_html=True)

    if prediction[0] == 0:
        css_class = "result-high"
        icon = "🌟"
        label = "High Performance"
        bar_color = "#48bb78"
        message = "This student shows excellent engagement and is on track for outstanding academic outcomes."
    elif prediction[0] == 2:
        css_class = "result-mid"
        icon = "📈"
        label = "Medium Performance"
        bar_color = "#ecc94b"
        message = "This student shows moderate engagement. Targeted support could elevate their outcomes."
    else:
        css_class = "result-low"
        icon = "⚠️"
        label = "Needs Improvement"
        bar_color = "#fc814a"
        message = "This student may benefit from immediate intervention and personalized support strategies."

    st.markdown(f"""
    <div class="{css_class}">
        <div class="result-icon">{icon}</div>
        <div class="result-label">{label}</div>
        <div class="conf-bar-wrap">
            <div class="conf-bar-fill" style="width:{confidence}%; background: linear-gradient(90deg, {bar_color}, #9f7aea);"></div>
        </div>
        <div class="result-conf">Confidence: {confidence}%</div>
        <p style="margin-top:18px; color:#8892a4; font-size:14px; max-width:420px; margin-left:auto; margin-right:auto; line-height:1.6;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------
# FOOTER
# --------------------------
st.markdown("""
<div class="footer">
    EDUPULSE · STUDENT E-LEARNING ANALYZER · BUILT WITH STREAMLIT & SCIKIT-LEARN
</div>
""", unsafe_allow_html=True)
