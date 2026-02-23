import streamlit as st
import joblib
import numpy as np

model = joblib.load("student_model.pkl")

st.title("Student E-Learning Analyzer")

st.write("Enter student data values separated by comma")

input_data = st.text_input("Input")

if st.button("Predict"):
    try:
        data = np.array([list(map(int, input_data.split(",")))])
        prediction = model.predict(data)
        st.success(f"Predicted Class: {prediction[0]}")
    except:
        st.error("Please enter valid numeric values.")
