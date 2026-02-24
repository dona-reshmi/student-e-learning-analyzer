import streamlit as st
import joblib
import numpy as np

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="AI Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)

# --------------------------
# CUSTOM CSS (Modern Glass UI)
# --------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

.hero {
    text-align: center;
    padding-top: 80px;
    padding-bottom: 30px;
}

.hero h1 {
    font-size: 55px;
    font-weight: 700;
}

.hero p {
    font-size: 20px;
    opacity: 0.85;
}

div[data-baseweb="slider"] > div {
    color: white;
}

.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border: none;
    padding: 12px 35px;
    font-size: 18px;
    border-radius: 30px;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 5px 20px rgba(0,0,0,0.4);
}

.result-box {
    text-align: center;
    padding: 30px;
    margin-top: 30px;
    font-size: 24px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# HERO SECTION
# --------------------------
st.markdown("""
<div class="hero">
    <h1>🎓 AI Student Performance Analyzer</h1>
    <p>Predict Academic Success with Intelligent Insights</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------
# LOAD MODEL
# --------------------------
model = joblib.load("student_model.pkl")

# --------------------------
# INPUT SECTION (Clean Layout)
# --------------------------
col1, col2 = st.columns(2)

with col1:
    participation = st.slider("📌 Class Participation", 0, 100)
    online_activity = st.slider("💻 Online Study Activity", 0, 100)
    attendance_label = st.selectbox(
        "📅 Attendance",
        ["Under 7 Absences", "More than 7 Absences"]
    )

with col2:
    platform_engagement = st.slider("📢 Platform Engagement", 0, 50)
    discussion_activity = st.slider("🗣 Discussion Activity", 0, 100)

absence_days = 1 if attendance_label == "Under 7 Absences" else 0

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------
# PREDICT BUTTON
# --------------------------
if st.button("🚀 Analyze Performance"):

    input_data = np.array([[1, 4, 4, 2, 1,
                            0, 7, 0, 0,
                            participation, online_activity,
                            platform_engagement, discussion_activity,
                            1, 1,
                            absence_days]])

    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)
    confidence = round(np.max(probabilities) * 100, 2)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    if prediction[0] == 0:
        st.markdown("### 🌟 High Performance Student")
        st.progress(100)
        st.write(f"Confidence: {confidence}%")

    elif prediction[0] == 2:
        st.markdown("### 🙂 Medium Performance Student")
        st.progress(60)
        st.write(f"Confidence: {confidence}%")

    else:
        st.markdown("### ⚠ Poor Performance Student")
        st.progress(30)
        st.write(f"Confidence: {confidence}%")

    st.markdown('</div>', unsafe_allow_html=True)
