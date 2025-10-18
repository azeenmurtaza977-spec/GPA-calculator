import streamlit as st
import pandas as pd

# --------------------------------
# 🌐 Page Configuration
# --------------------------------
st.set_page_config(page_title="🎓 Weighted CGPA Calculator", layout="centered")

# --------------------------------
# 🎨 Custom Styling
# --------------------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #2196f3, #64b5f6);
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #e3f2fd;
        padding: 2rem 3rem;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    h1, h2, h3, h4 {
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
        color: white;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------
# 🎓 App Header
# --------------------------------
st.title("🎓 Advanced Weighted CGPA Calculator")
st.markdown("""
Welcome to the **Professional CGPA Calculator**.  
Enter your **semester GPA** and **credit hours** — the app will automatically compute your **weighted CGPA**.  
""")

# --------------------------------
# 🧑‍🎓 Student Details
# --------------------------------
st.sidebar.header("🎓 Student Information")
student_name = st.sidebar.text_input("Enter Student Name:")
completed_semesters = st.sidebar.number_input("Number of Semesters Completed:", 1, 8, 1)

if not student_name:
    st.warning("👉 Please enter your name in the sidebar to begin.")
    st.stop()

# --------------------------------
# 📚 GPA & Credit Hour Input
# --------------------------------
semester_data = []

st.subheader(f"📘 Enter Semester Details for {student_name}")

for sem in range(1, completed_semesters + 1):
    with st.expander(f"Semester {sem}", expanded=(sem == 1)):
        gpa = st.number_input(f"GPA for Semester {sem}:", 0.0, 4.0, step=0.01, key=f"gpa_{sem}")
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

    # Progress Bar Visualization
    st.progress(min(weighted_cgpa / 4.0, 1.0))

    # Final Grade
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

    # Data Summary
    st.markdown("### 📄 Semester Summary")
    st.dataframe(df, use_container_width=True)

    # CSV Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CGPA Report (CSV)",
        data=csv,
        file_name=f"{student_name}_Weighted_CGPA_Report.csv",
        mime='text/csv'
    )

# --------------------------------
# 🧠 Notes
# --------------------------------
st.markdown("""
---
### 📘 Notes:
- **Weighted CGPA Formula:**
  \[
  CGPA = \frac{\sum(GPA_i \times CreditHours_i)}{\sum(CreditHours_i)}
  \]
- Ensures fair averaging when semesters have **different credit loads**.
- Based on the **4.0 GPA scale** (HEC & international standards).
""")

