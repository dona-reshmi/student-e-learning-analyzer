import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("student_model.pkl")

st.set_page_config(page_title="Student Performance Analyzer", page_icon="🎓", layout="centered")

st.title("🎓 AI Student Performance Analyzer")
st.markdown("### Smart Academic Performance Prediction System")
st.markdown("---")

st.write("Adjust the student engagement levels below:")

# ===============================
# INPUT SECTION (2 Columns)
# ===============================

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

# Attendance Encoding (Correct)
# Above-7 -> 0
# Under-7 -> 1
if attendance_label == "Under 7 Absences":
    absence_days = 1
else:
    absence_days = 0

# ===============================
# FIXED VALUES (same as training)
# ===============================

gender = 1
nationality = 4
birthplace = 4
stage = 2
grade = 1
section = 0
topic = 7
semester = 0
relation = 0
parent_answer = 1
parent_satisfaction = 1

st.markdown("---")

# ===============================
# PREDICTION
# ===============================

if st.button("🚀 Analyze Performance"):

    input_data = np.array([[gender, nationality, birthplace, stage, grade,
                            section, topic, semester, relation,
                            participation, online_activity,
                            platform_engagement, discussion_activity,
                            parent_answer, parent_satisfaction,
                            absence_days]])

    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)

    confidence = round(np.max(probabilities) * 100, 2)

    st.markdown("## 📊 Prediction Result")

    # Correct Mapping
    # 0 -> High
    # 1 -> Low
    # 2 -> Medium

    if prediction[0] == 0:
        st.success(f"🎉 High Performance Student ({confidence}% Confidence)")
        st.progress(100)
        st.write("✅ Excellent engagement and strong academic behavior.")
        st.write("🔹 Keep maintaining participation and consistency.")

    elif prediction[0] == 2:
        st.warning(f"🙂 Medium Performance Student ({confidence}% Confidence)")
        st.progress(60)
        st.write("⚡ Moderate academic engagement detected.")
        st.write("🔹 Improve class participation and online activity.")
        st.write("🔹 Try reducing absence days.")

    else:
        st.error(f"⚠ Poor Performance Student ({confidence}% Confidence)")
        st.progress(30)
        st.write("🚨 Low engagement level detected.")
        st.write("🔹 Increase participation in discussions.")
        st.write("🔹 Access more learning resources.")
        st.write("🔹 Improve attendance consistency.")

    st.markdown("---")
    st.markdown("### 🤖 Model Accuracy: 86.45%")
