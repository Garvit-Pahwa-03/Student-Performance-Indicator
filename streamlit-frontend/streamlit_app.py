import streamlit as st
import requests

API_URL = "https://student-performance-predictor-jpsd.onrender.com/predict_api"

st.set_page_config(page_title="Student Performance Predictor", page_icon="📊")

st.title("📊 Student Exam Performance Predictor")
st.write("Enter student details to predict their **Math Score**.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["male", "female"])
        race_ethnicity = st.selectbox(
            "Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"]
        )
        parental_level_of_education = st.selectbox(
            "Parental Level of Education",
            [
                "some high school",
                "high school",
                "some college",
                "associate's degree",
                "bachelor's degree",
                "master's degree",
            ],
        )
        lunch = st.selectbox("Lunch Type", ["standard", "free/reduced"])

    with col2:
        test_preparation_course = st.selectbox("Test Preparation Course", ["none", "completed"])
        reading_score = st.number_input("Reading Score", min_value=0, max_value=100, value=70)
        writing_score = st.number_input("Writing Score", min_value=0, max_value=100, value=70)

    submitted = st.form_submit_button("Predict Math Score")

if submitted:
    payload = {
        "gender": gender,
        "race_ethnicity": race_ethnicity,
        "parental_level_of_education": parental_level_of_education,
        "lunch": lunch,
        "test_preparation_course": test_preparation_course,
        "reading_score": reading_score,
        "writing_score": writing_score,
    }

    with st.spinner("Getting prediction..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()

            if "prediction" in result:
                st.success(f"Predicted Math Score: **{result['prediction']}**")
            else:
                st.error(f"API error: {result.get('error', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the API: {e}")