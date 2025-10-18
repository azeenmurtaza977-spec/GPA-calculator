import streamlit as st
import pandas as pd

# --------------------------------
# 🌐 Page Configuration & Styling
# --------------------------------
st.set_page_config(page_title="🎓 Advanced CGPA Calculator", layout="wide")

# Add custom CSS for background and styling
st.markdown("""
    <style>
        body {
            background-color: #e3f2fd;
        }
        .main {
            background-color: #bbdefb;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background-color: #1976d2;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #1565c0;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------
# 🎓 Title and Intro
# --------------------------------
st.title("🎓 University CGPA Calculator (Weighted Mean System)")
st.markdown("""
This calculator computes your **Overall CGPA** using **weighted GPA averaging**.  
Simply enter your **semester GPAs** and **credit hours** — the system will handle the rest.
""")

# --------------------------------
# 🧑‍🎓 Student Information
# --------------------------------
st.sidebar.header("🎓 Student Information")
student_name = st.sidebar.text_input("Student Name:")
completed_semesters = st.sidebar.number_input("Number of semesters completed:", 1, 8, 1)

st.markdown("---")

if not student_name:
    st.warning("Please enter your name in the sidebar to begin.")
    st.stop()

st.header(f"📘 CGPA Calculation for {student_name}")

# --------------------------------
# 📊 GPA and Credit Hour Inputs
# --------------------------------
semester_data = []

for sem in range(1, completed_semesters + 1):
    with st.expander(f"Semester {sem}", expanded=(sem == 1)):
        gpa = st.number_input(f"Semester {sem} GPA:", 0.0, 4.0, step=0.01, key=f"gpa_sem{sem}")
        credit_hours = st.number_input(f"Total Credit Hours in Semester {sem}:", 1, 25, step=1, key=f"ch_sem{sem}")
        semester_data.append({"Semester": f"Semester {sem}", "GPA": gpa, "CreditHours": credit_hours})

# --------------------------------
# 🎯 Weighted CGPA Calculation
# --------------------------------
if st.button("Calculate Overall CGPA"):
    df = pd.DataFrame(semester_data)
    total_weighted = (df["GPA"] * df["CreditHours"]).sum()
    total_credits = df["CreditHours"].sum()
    weighted_cgpa = round(total_weighted / total_credits, 2)

    st.balloons()
    st.markdown(f"## 🏆 {student_name}'s Overall CGPA: **{weighted_cgpa}**")

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
    st.markdown(f"### 🎯 Final Grade: **{final_grade}**")

    # Summary Table
    st.subheader("📄 Semester Summary")
    st.dataframe(df.style.highlight_max(subset=["GPA"], color="#90caf9"), use_container_width=True)

    # Download Option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CGPA Report (CSV)",
        data=csv,
        file_name=f"{student_name}_CGPA_Report.csv",
        mime="text/csv"
    )

# --------------------------------
# 📝 Notes
# --------------------------------
st.markdown("""
---
### 📘 Notes:
- CGPA is calculated using the **Weighted Mean Formula**:  
  \[
  \text{CGPA} = \frac{\sum (GPA_i \times CreditHours_i)}{\sum CreditHours_i}
  \]
- This method ensures semesters with more credit hours have **greater impact**.
- GPA scale used: **4.0 system** (HEC & International Standard).
""")
