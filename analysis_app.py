import streamlit as st
from helper import clean_text, read_file
from nltk_work import lemmatize_text
from resume_sections import extract_work_experience, extract_skills_section, extract_contact_info, extract_education, extract_name
import os
from score_pred import evaluate_resume
from llm_feedback import generate_feedback
import base64
from docx import Document

st.set_page_config(layout="wide")
st.title("Resume Analyzer")

path_of_resume_folder = './uploaded_resumes'
path_of_jd_folder = './job_description_datasets'

job_description = st.file_uploader("Please upload a job description (PDF)", type=["pdf"]) # Input Job Description

def display_file(file_path):
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>', unsafe_allow_html=True)

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        content = "\n".join([para.text for para in doc.paragraphs])
        st.markdown(f"<div style='text-align: justify;'>{content.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    elif file_path.endswith(".txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        st.markdown(f"<div style='text-align: justify;'>{content.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    else:
        st.warning("Unsupported file format. Download instead.")
        with open(file_path, "rb") as f:
            file_data = f.read()
        b64 = base64.b64encode(file_data).decode()
        file_name = os.path.basename(file_path)
        st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download {file_name}</a>', unsafe_allow_html=True)


# Extract Information
def extract_information(file_path):
    original_text = read_file(file_path)
    cleaned_text = clean_text(original_text)

    return {
        "Name": extract_name(original_text),
        "Contact Info": extract_contact_info(original_text),
        "Skills": extract_skills_section(cleaned_text),
        "Education": extract_education(original_text),
        "Work Experience": extract_work_experience(original_text),
    }


if os.path.exists(path_of_resume_folder) and os.path.exists(path_of_jd_folder):
    files = os.listdir(path_of_resume_folder)
    jd_files = os.listdir(path_of_jd_folder)

    if files and jd_files:
        st.write("Uploaded Resumes:")

        jd_path = os.path.join(path_of_jd_folder, jd_files[0])
        jd_text = read_file(jd_path) if job_description else None

        for file in files:
            file_path = os.path.join(path_of_resume_folder, file)
            resume_text = read_file(file_path)
            score_percentage = f"{evaluate_resume(resume_text, jd_text) * 100:.2f}%" if jd_text and resume_text else "N/A"

            with st.expander(f"📄 {file} – **Score: {score_percentage}**", expanded=False):
                col1, col2, col3 = st.columns([1, 1, 1])

                if col1.button("Generate Content", key=f"content_{file}"):
                    st.session_state[f"action_{file}"] = "content"

                if col2.button("View Resume", key=f"view_{file}"):
                    st.session_state[f"action_{file}"] = "view"

                if col3.button("Generate Feedback", key=f"feedback_{file}") and job_description:
                    st.session_state[f"action_{file}"] = "feedback"

                # Display Results
                action = st.session_state.get(f"action_{file}")

                if action == "content":
                    st.subheader("Extracted Information")
                    st.json(extract_information(file_path))

                elif action == "view":
                    display_file(file_path)

                elif action == "feedback" and job_description:
                    score = evaluate_resume(resume_text, jd_text)
                    feedback = generate_feedback(resume_text, jd_text, score)
                    st.subheader("Feedback")
                    st.markdown(f"<div style='text-align: justify;'>{feedback.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    else:
        st.error(f"No resumes or job descriptions found.")
else:
    st.error(f"Folder(s) missing: '{path_of_resume_folder}' or '{path_of_jd_folder}'")
