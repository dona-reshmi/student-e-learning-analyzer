import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("student_model.pkl")

st.set_page_config(page_title="Student Performance Analyzer", page_icon="🎓")

st.title("🎓 Student Academic Performance Analyzer")
st.write("Fill in the student engagement details below to predict performance level.")

st.markdown("---")

# ===============================
# USER-FRIENDLY INPUTS
# ===============================

participation = st.slider("📌 Class Participation Level", 0, 100)
online_activity = st.slider("💻 Online Study Activity", 0, 100)
platform_engagement = st.slider("📢 Platform Engagement (Announcements Checked)", 0, 50)
discussion_activity = st.slider("🗣 Group Discussion Activity", 0, 100)

attendance_label = st.selectbox(
    "📅 Attendance Category",
    ["Under 7 Absences", "More than 7 Absences"]
)

# Convert attendance to encoded value
if attendance_label == "Under 7 Absences":
    absence_days = 0
else:
    absence_days = 1

# ===============================
# FIXED VALUES (Same as training)
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
# PREDICTION BUTTON
# ===============================

if st.button("🔍 Predict Performance"):

    input_data = np.array([[gender, nationality, birthplace, stage, grade,
                            section, topic, semester, relation,
                            participation, online_activity,
                            platform_engagement, discussion_activity,
                            parent_answer, parent_satisfaction,
                            absence_days]])

    prediction = model.predict(input_data)

    st.markdown("## 📊 Prediction Result")

    if prediction[0] == 2:
        st.success("🎉 High Performance Student")
        st.write("This student shows strong academic engagement and learning behavior.")

    elif prediction[0] == 1:
        st.warning("🙂 Medium Performance Student")
        st.write("This student has moderate engagement and can improve with more participation.")

    else:
        st.error("⚠ Low Performance Student")
        st.write("This student may need additional academic support and guidance.")
