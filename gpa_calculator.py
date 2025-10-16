import streamlit as st
import pandas as pd

# -------------------------------
# 🎓 Page Setup
# -------------------------------
st.set_page_config(page_title="University GPA & CGPA Calculator", layout="wide")

st.title("🎓 University GPA & CGPA Calculator (8-Semester System)")
st.markdown("""
This calculator allows students to compute their **Semester-wise GPA** and **Overall CGPA** for up to **8 semesters**.  
Simply enter your name, completed semesters, and marks or grades for each course.
""")

# -------------------------------
# 🧮 GPA Conversion Function
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
    if gpa >= 4.0: return "A+"
    elif gpa >= 3.7: return "A"
    elif gpa >= 3.3: return "B+"
    elif gpa >= 3.0: return "B"
    elif gpa >= 2.7: return "C+"
    elif gpa >= 2.3: return "C"
    elif gpa >= 2.0: return "D"
    else: return "F"

# -------------------------------
# 🧑‍🎓 Student Info
# -------------------------------
st.sidebar.header("🎓 Student Information")
student_name = st.sidebar.text_input("Student Name:")
completed_semesters = st.sidebar.number_input("Number of semesters completed:", 1, 8, 1)

st.markdown("---")
if not student_name:
    st.warning("Please enter your name in the sidebar to begin.")
    st.stop()

st.header(f"📘 GPA Calculation for {student_name}")

# -------------------------------
# 📊 Semester GPA Entry
# -------------------------------
semester_gpas = []
all_semester_data = {}

for sem in range(1, completed_semesters + 1):
    with st.expander(f"Semester {sem}", expanded=(sem == 1)):
        num_courses = st.number_input(
            f"Number of courses registered in Semester {sem}:",
            min_value=1,
            max_value=10,
            step=1,
            key=f"num_courses_sem{sem}"
        )

        course_marks = []
        total_gpa = 0

        for i in range(1, num_courses + 1):
            marks = st.number_input(f"Course {i} Marks (0–100):", 0, 100, step=1, key=f"sem{sem}_course{i}")
            gpa = marks_to_gpa(marks)
            total_gpa += gpa
            course_marks.append((f"Course {i}", marks, gpa, gpa_to_grade(gpa)))

        semester_gpa = round(total_gpa / num_courses, 2)
        semester_gpas.append(semester_gpa)
        all_semester_data[f"Semester {sem}"] = {
            "courses": course_marks,
            "semester_gpa": semester_gpa
        }
        st.success(f"**Semester {sem} GPA:** {semester_gpa}")

# -------------------------------
# 🎯 CGPA Calculation
# -------------------------------
if st.button("Calculate Overall CGPA"):
    overall_cgpa = round(sum(semester_gpas) / len(semester_gpas), 2)
    st.balloons()
    st.markdown(f"## 🏆 {student_name}'s Overall CGPA: **{overall_cgpa}**")
    st.markdown(f"### 🎯 Final Grade: **{gpa_to_grade(overall_cgpa)}**")

    # Summary Table
    summary_df = pd.DataFrame({
        "Semester": [f"Semester {i+1}" for i in range(len(semester_gpas))],
        "Semester GPA": semester_gpas
    })
    st.subheader("📄 Semester Summary")
    st.dataframe(summary_df, use_container_width=True)

# -------------------------------
# 📥 Optional: Download GPA Report
# -------------------------------
if st.checkbox("📥 Download Detailed Report"):
    all_rows = []
    for sem, info in all_semester_data.items():
        for course, marks, gpa, grade in info["courses"]:
            all_rows.append([sem, course, marks, gpa, grade])
    report_df = pd.DataFrame(all_rows, columns=["Semester", "Course", "Marks", "GPA", "Grade"])
    csv = report_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download GPA Report (CSV)",
        data=csv,
        file_name=f"{student_name}_GPA_Report.csv",
        mime="text/csv"
    )

# -------------------------------
# 📝 Notes Section
# -------------------------------
st.markdown("""
---
### 📘 Notes:
- GPA is based on the **standard 4.0 scale** used by most universities.
- You can calculate your CGPA after **completing 1 or more semesters**.
- The system automatically averages semester GPAs to compute CGPA.
- Marks thresholds follow **HEC Pakistan** and **international GPA standards**.
""")

