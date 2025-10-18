import streamlit as st
import pandas as pd

# --------------------------------
# 🌐 Page Setup
# --------------------------------
st.set_page_config(page_title="🎓 CGPA & GPA Calculator", layout="centered")

# --------------------------------
# 🎨 Custom Styling (Full Blue Theme)
# --------------------------------
st.markdown("""
    <style>
        body {
            background-color: #bbdefb;
            color: #0d47a1;
            font-family: 'Segoe UI', sans-serif;
        }
        .main {
            background-color: #e3f2fd;
            padding: 2rem 3rem;
            border-radius: 15px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        }
        h1, h2, h3, h4, h5 {
            color: #0d47a1 !important;
        }
        .stButton>button {
            background-color: #1565c0;
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0d47a1;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------
# 🎓 Title
# --------------------------------
st.title("🎓 Weighted CGPA & GPA Calculator")
st.markdown("""
Easily calculate your **GPA (per semester)** or your **Overall Weighted CGPA**.  
Choose your preferred calculation method from the sidebar.
""")

# --------------------------------
# 🧑‍🎓 Sidebar Information
# --------------------------------
st.sidebar.header("🎓 Student Information")
student_name = st.sidebar.text_input("Enter Student Name:")
completed_semesters = st.sidebar.number_input("Number of Semesters Completed:", 1, 8, 1)
calculation_mode = st.sidebar.radio("Choose Mode:", ["Enter GPA Directly", "Enter Marks per Subject"])

# Stop if no name entered
if not student_name:
    st.warning("👉 Please enter your name in the sidebar to begin.")
    st.stop()

# --------------------------------
# 📊 Function for Marks → GPA Conversion
# --------------------------------
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

# --------------------------------
# 📘 Main Section
# --------------------------------
st.subheader(f"📘 CGPA Calculation for {student_name}")

semester_data = []

for sem in range(1, completed_semesters + 1):
    with st.expander(f"Semester {sem}", expanded=(sem == 1)):

        # Option 1: GPA entered directly
        if calculation_mode == "Enter GPA Directly":
            gpa = st.number_input(f"GPA for Semester {sem}:", 0.0, 4.0, step=0.01, key=f"gpa_{sem}")
        
        # Option 2: GPA calculated from marks
        else:
            num_subjects = st.number_input(f"Number of subjects in Semester {sem}:", 1, 10, 1, key=f"subs_{sem}")
            total_gpa = 0
            for subj in range(1, num_subjects + 1):
                marks = st.number_input(f"Subject {subj} Marks (0–100):", 0, 100, step=1, key=f"sem{sem}_sub{subj}")
                total_gpa += marks_to_gpa(marks)
            gpa = round(total_gpa / num_subjects, 2)
            st.info(f"🎯 Calculated GPA for Semester {sem}: **{gpa}**")

        credit_hours = st.number_input(f"Total Credit Hours for Semester {sem}:", 1, 25, step=1, key=f"ch_{sem}")
        semester_data.append({
            "Semester": f"Semester {sem}",
            "GPA": gpa,
            "Credit Hours": credit_hours
        })

# --------------------------------
# 🎯 Weighted CGPA Calculation
# --------------------------------
if st.button("Calculate Weighted CGPA 🎯"):
    df = pd.DataFrame(semester_data)
    total_weight = (df["GPA"] * df["Credit Hours"]).sum()
    total_credits = df["Credit Hours"].sum()
    weighted_cgpa = round(total_weight / total_credits, 2)

    st.success(f"🏆 **{student_name}'s Overall Weighted CGPA: {weighted_cgpa}**")

    # Progress Bar
    st.progress(min(weighted_cgpa / 4.0, 1.0))

    # Grade Conversion
    def gpa_to_grade(gpa):
        if gpa >= 4.0: return "A+"
        elif gpa >= 3.7: return "A"
        elif gpa >= 3.3: return "B+"
        elif gpa >= 3.0: return "B"
        elif gpa >= 2.7: return "C+"
        elif gpa >= 2.3: return "C"
        elif gpa >= 2.0: return "D"
        else: return "F"

    final_grade = gpa_to_grade(weighted_cgpa)
    st.markdown(f"### 🎓 Final Grade: **{final_grade}**")

    # Display Summary Table
    st.markdown("### 📄 Semester Summary")
    st.dataframe(df, use_container_width=True)

    # Download Option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CGPA Report (CSV)",
        data=csv,
        file_name=f"{student_name}_Weighted_CGPA_Report.csv",
        mime="text/csv"
    )

# --------------------------------
# 🧠 Notes
# --------------------------------
st.markdown("""
---
### 📘 Notes:
- **GPA (Grade Point Average):** measures performance for a single semester.  
- **CGPA (Cumulative GPA):** average of all semester GPAs, weighted by credit hours.  
- CGPA Formula:  
  \[
  CGPA = \frac{\sum(GPA_i \times CreditHours_i)}{\sum(CreditHours_i)}
  \]
- Based on **4.0 GPA scale** (HEC & international standard).
""")


