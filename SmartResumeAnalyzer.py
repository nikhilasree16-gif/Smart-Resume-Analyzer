import streamlit as st
import pdfplumber

st.title("Smart Resume Analyzer")

uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume Uploaded Successfully!")

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    st.subheader("Resume Content")
    st.write(text)

    skills = ["Python", "Java", "C", "Machine Learning", "AI", "SQL"]

    st.subheader("Detected Skills")

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    if found_skills:
        st.write(found_skills)
    else:
        st.write("No skills detected")