import streamlit as st
import pandas as pd

st.set_page_config(page_title="GPA & CGPA Calculator", layout="centered")

st.title("🎓 University GPA & CGPA Calculator")
st.markdown("Enter your grades or marks for each subject below. The app will calculate your GPA for each semester and overall CGPA automatically.")

# --- Helper function ---
def calculate_gpa(marks):
    """
    Convert marks to GPA based on standard scale.
    """
    if marks >= 85:
        return 4.0
    elif marks >= 80:
        return 3.7
    elif marks >= 75:
        return 3.3
    elif marks >= 70:
        return 3.0
    elif marks >= 65:
        return 2.7
    elif marks >= 60:
        return 2.3
    elif marks >= 55:
        return 2.0
    elif marks >= 50:
        return 1.7
    else:
        return 0.0

# --- Semester Subjects ---
semesters = {
    "1st Semester": [
        "Application of Information and Communication Technologies",
        "Functional English",
        "Fundamentals of Philosophy",
        "Exploring Quantitative Skills",
        "Applied Physics",
        "Introductory Statistics"
    ],
    "2nd Semester": [
        "Fundamentals of Computer Programming",
        "Islamic Studies",
        "Expository Writing",
        "Fundamentals of Psychology",
        "Tools for Quantitative Reasoning",
        "Introduction to Probability Theory"
    ],
    "3rd Semester": [
        "Ideology and Constitution of Pakistan",
        "Civics and Community Engagement",
        "Introduction to Entrepreneurship",
        "Probability and Probability Distribution",
        "Survey Sampling",
        "Computing Statistics I"
    ],
    "4th Semester": [
        "Data Science Fundamentals",
        "Data Visualization Techniques",
        "Statistical Inference",
        "Regression Analysis I",
        "Sampling and Sampling Distributions",
        "Mathematical Tools for Statistics"
    ]
}

# --- GPA Calculation UI ---
semester_gpas = []
st.header("📘 Enter Marks / Grades for Each Semester")

for sem, subjects in semesters.items():
    st.subheader(sem)
    marks_list = []
    for subj in subjects:
        marks = st.number_input(f"{subj} Marks (0–100):", min_value=0, max_value=100, step=1, key=subj)
        marks_list.append(marks)
    
    gpa_list = [calculate_gpa(m) for m in marks_list]
    sem_gpa = round(sum(gpa_list) / len(gpa_list), 2)
    semester_gpas.append(sem_gpa)
    st.success(f"{sem} GPA: **{sem_gpa}**")

# --- Overall CGPA ---
if st.button("Calculate Overall CGPA"):
    overall_cgpa = round(sum(semester_gpas) / len(semester_gpas), 2)
    st.balloons()
    st.markdown(f"### 🎯 Your Overall CGPA is: **{overall_cgpa}**")

# --- Display Summary Table ---
if st.checkbox("Show Semester Summary"):
    df = pd.DataFrame({
        "Semester": list(semesters.keys()),
        "GPA": semester_gpas
    })
    st.table(df)
