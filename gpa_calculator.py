import streamlit as st
import pandas as pd

# -------------------------------
# 🎓 Streamlit Page Configuration
# -------------------------------
st.set_page_config(page_title="University GPA & CGPA Calculator", layout="wide")
st.markdown("""
<style>
    .main {
        background-color: #f9f9f9;
    }
    h1, h2, h3, h4 {
        color: #004080;
    }
    .stButton>button {
        background-color: #004080;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
    }
    .stButton>button:hover {
        background-color: #0066cc;
        color: white;
    }
    .css-1d391kg p {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🎓 Title & Description
# -------------------------------
st.title("🎓 University GPA & CGPA Calculator")
st.markdown("""
This app helps students calculate their **semester-wise GPA** and **overall CGPA** across four semesters.
Enter your obtained marks for each subject, and the calculator will automatically compute your performance based on the university's GPA scale.
""")

# -------------------------------
# 📘 GPA Scale Function
# -------------------------------
def marks_to_gpa(marks):
    if marks >= 85: return 4.0
    elif marks >= 80: return 3.7
    elif marks >= 75: return 3.3
    elif marks >= 70: return 3.0
    elif marks >= 65: return 2.7
    elif marks >= 60: return 2.3
    elif marks >= 55: return 2.0
    elif marks >= 50: return 1.7
    else: return 0.0

def gpa_to_grade(gpa):
    if gpa == 4.0: return "A+"
    elif gpa >= 3.7: return "A"
    elif gpa >= 3.3: return "B+"
    elif gpa >= 3.0: return "B"
    elif gpa >= 2.7: return "C+"
    elif gpa >= 2.3: return "C"
    elif gpa >= 2.0: return "D"
    else: return "F"

# -------------------------------
# 📚 Subjects by Semester
# -------------------------------
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

# -------------------------------
# 📊 GPA Calculation UI
# -------------------------------
st.header("📋 Semester-wise Marks Entry")

semester_results = {}
all_sem_gpas = []

for sem, subjects in semesters.items():
    with st.expander(f"📘 {sem}", expanded=False):
        st.write("Enter marks for each subject (0–100).")
        marks_data = []
        total_gpa = 0

        for subj in subjects:
            marks = st.number_input(f"{subj}", 0, 100, step=1, key=f"{sem}-{subj}")
            gpa = marks_to_gpa(marks)
            total_gpa += gpa
            marks_data.append([subj, marks, gpa, gpa_to_grade(gpa)])
        
        sem_gpa = round(total_gpa / len(subjects), 2)
        semester_results[sem] = {"subjects": marks_data, "gpa": sem_gpa}
        all_sem_gpas.append(sem_gpa)
        st.success(f"{sem} GPA: **{sem_gpa}**")

# -------------------------------
# 🎯 Overall CGPA
# -------------------------------
st.markdown("---")
if st.button("Calculate Overall CGPA"):
    cgpa = round(sum(all_sem_gpas) / len(all_sem_gpas), 2)
    st.balloons()
    st.markdown(f"## 🏆 Your Overall CGPA: **{cgpa}**")
    st.markdown(f"### Grade: **{gpa_to_grade(cgpa)}**")

    # Summary Table
    summary_df = pd.DataFrame({
        "Semester": list(semester_results.keys()),
        "Semester GPA": all_sem_gpas
    })
    st.subheader("📄 Semester Summary")
    st.dataframe(summary_df, use_container_width=True)

# -------------------------------
# 📑 Optional: Download Results
# -------------------------------
if st.checkbox("📥 Download Detailed Report"):
    report_rows = []
    for sem, details in semester_results.items():
        for subj, marks, gpa, grade in details["subjects"]:
            report_rows.append([sem, subj, marks, gpa, grade])
    report_df = pd.DataFrame(report_rows, columns=["Semester", "Subject", "Marks", "GPA", "Grade"])
    
    csv = report_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download GPA Report (CSV)", csv, "GPA_Report.csv", "text/csv")

# -------------------------------
# ℹ️ Notes Section
# -------------------------------
st.markdown("""
---
### 📘 Notes:
- GPA is calculated using a **standard 4.0 scale** used by most universities.
- Marks thresholds follow the **HEC Pakistan recommended scheme**.
- CGPA = average of all semester GPAs.
- This tool is designed for educational institutions to provide accurate GPA analytics.
""")
