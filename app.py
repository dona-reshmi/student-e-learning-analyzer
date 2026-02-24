import streamlit as st
import joblib
import numpy as np

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(
    page_title="AI Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)

# ------------------------
# CUSTOM CSS (Landing Page Style)
# ------------------------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1f4037, #99f2c8);
    }
    .hero {
        text-align: center;
        padding: 60px 20px 30px 20px;
    }
    .hero h1 {
        font-size: 48px;
        color: white;
    }
    .hero p {
        font-size: 20px;
        color: white;
        opacity: 0.9;
    }
    .card {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
        margin-top: 30px;
    }
    .stButton>button {
        background-color: #1f4037;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 25px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------
# HERO SECTION
# ------------------------
st.markdown("""
    <div class="hero">
        <h1>🎓 AI Student Performance Analyzer</h1>
        <p>Smart Academic Insights Powered by Machine Learning</p>
    </div>
""", unsafe_allow_html=True)

# ------------------------
# LOAD MODEL
# ------------------------
model = joblib.load("student_model.pkl")

# ------------------------
# INPUT CARD
# ------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📊 Enter Student Engagement Details")

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

# Attendance Encoding
absence_days = 1 if attendance_label == "Under 7 Absences" else 0

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------
# PREDICTION BUTTON
# ------------------------
if st.button("🚀 Analyze Now"):

    # Fixed values (same as training)
    input_data = np.array([[1, 4, 4, 2, 1,
                            0, 7, 0, 0,
                            participation, online_activity,
                            platform_engagement, discussion_activity,
                            1, 1,
                            absence_days]])

    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)
    confidence = round(np.max(probabilities) * 100, 2)

    st.markdown("---")
    st.subheader("📈 Prediction Result")

    if prediction[0] == 0:
        st.success(f"🌟 High Performance Student")
        st.progress(100)
        st.write(f"Confidence Level: {confidence}%")
        st.write("Excellent academic engagement and consistency detected.")

    elif prediction[0] == 2:
        st.warning(f"🙂 Medium Performance Student")
        st.progress(60)
        st.write(f"Confidence Level: {confidence}%")
        st.write("Moderate performance. Improving participation can boost results.")

    else:
        st.error(f"⚠ Poor Performance Student")
        st.progress(30)
        st.write(f"Confidence Level: {confidence}%")
        st.write("Low engagement detected. Increasing activity and attendance is recommended.")

st.markdown('</div>', unsafe_allow_html=True)
