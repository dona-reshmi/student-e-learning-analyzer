import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("student_model.pkl")

st.title("🎓 Student E-Learning Performance Predictor")

st.write("Enter student details below:")

# User Inputs
raisedhands = st.slider("Raised Hands", 0, 100)
visited_resources = st.slider("Visited Resources", 0, 100)
announcements_view = st.slider("Announcements View", 0, 50)
discussion = st.slider("Discussion Participation", 0, 100)
absence_days = st.selectbox("Student Absence Days", [0, 1])

# Fixed encoded values (same format used during training)
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

# Prediction
if st.button("Predict Performance"):

    input_data = np.array([[gender, nationality, birthplace, stage, grade,
                            section, topic, semester, relation,
                            raisedhands, visited_resources,
                            announcements_view, discussion,
                            parent_answer, parent_satisfaction,
                            absence_days]])

    prediction = model.predict(input_data)

    if prediction[0] == 2:
        st.success("Predicted Class: High Performance 🎉")
    elif prediction[0] == 1:
        st.warning("Predicted Class: Medium Performance 🙂")
    else:
        st.error("Predicted Class: Low Performance ⚠️")