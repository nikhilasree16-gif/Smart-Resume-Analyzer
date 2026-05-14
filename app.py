import streamlit as st
import pdfplumber

st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

st.title("Smart Resume Analyzer")
st.write("Upload your resume and get AI-style analysis")

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

# Skill database
skills_db = {
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "SQL", "NLP", "Data Science"],
    "Data Scientist": ["Python", "Pandas", "NumPy", "Machine Learning", "Statistics", "SQL", "Data Visualization"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB"],
    "Java Developer": ["Java", "Spring", "Hibernate", "SQL", "OOP"],
    "Python Developer": ["Python", "Django", "Flask", "SQL", "Git"]
}

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    st.subheader("Resume Content")
    st.write(text)

    # Detect all skills
    detected_skills = []

    for role, skills in skills_db.items():
        for skill in skills:
            if skill.lower() in text.lower() and skill not in detected_skills:
                detected_skills.append(skill)

    st.subheader("Detected Skills")
    st.write(detected_skills)

    # Job role prediction
    role_scores = {}

    for role, skills in skills_db.items():
        score = 0

        for skill in skills:
            if skill.lower() in text.lower():
                score += 1

        role_scores[role] = score

    predicted_role = max(role_scores, key=role_scores.get)

    st.subheader("Predicted Job Role")
    st.success(predicted_role)

    # Resume score
    total_required = len(skills_db[predicted_role])
    matched = role_scores[predicted_role]

    resume_score = int((matched / total_required) * 100)

    st.subheader("Resume Score")
    st.progress(resume_score)
    st.write(f"Resume Score: {resume_score}/100")

    # Missing skills
    missing_skills = []

    for skill in skills_db[predicted_role]:
        if skill.lower() not in text.lower():
            missing_skills.append(skill)

    st.subheader("Missing Skills")

    if missing_skills:
        st.warning(missing_skills)
    else:
        st.success("Excellent! No important skills missing")

    # ATS Check
    st.subheader("ATS Compatibility")

    if resume_score >= 80:
        st.success("ATS Friendly Resume")
    elif resume_score >= 50:
        st.warning("Resume can be improved for ATS")
    else:
        st.error("Low ATS Score")

    # Resume tips
    st.subheader("Resume Improvement Tips")

    tips = []

    if "projects" not in text.lower():
        tips.append("Add Projects section")

    if "internship" not in text.lower():
        tips.append("Add Internship Experience")

    if "github" not in text.lower():
        tips.append("Add GitHub profile")

    if "linkedin" not in text.lower():
        tips.append("Add LinkedIn profile")

    if resume_score < 70:
        tips.append("Improve technical skills")

    for tip in tips:
        st.write("•", tip)

    # Resume summary
    st.subheader("Resume Summary")

    st.info(
        f"This resume is suitable for {predicted_role}. "
        f"Detected {len(detected_skills)} technical skills with a resume score of {resume_score}/100."
    )