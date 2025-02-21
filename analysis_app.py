<<<<<<< HEAD
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
=======
import streamlit as st
from helper import clean_text, read_file
from nltk_work import lemmatize_text
from resume_sections import extract_work_experience, extract_skills_section, extract_contact_info, extract_education, extract_name
import os
from score_pred import evaluate_resume
from llm_feedback import generate_feedback

st.title("Resume Analyzer")

# Function to show the content of the selected resume
def show_content(file_path):
    try:
        st.write(f"Processing file: {file_path}")
        original_text = read_file(file_path)
        if not original_text:
            st.error("Failed to extract content from the file.")
            return

        cleaned_text = clean_text(original_text)
        st.text_area("Original Text", original_text, height=200)
        st.text_area("Cleaned Text", cleaned_text, height=200)

        # Additional processing
        lem_text = lemmatize_text(cleaned_text)
        skills = extract_skills_section(cleaned_text)
        work_exp = extract_work_experience(original_text)
        person = extract_name(original_text)
        education = extract_education(original_text)
        contact_info = extract_contact_info(original_text)

        # Display extracted information
        st.text_area("Lemmatized Text", lem_text, height=200)
        st.json({
            "Name": person,
            "Contact Info": contact_info,
            "Skills": skills,
            "Education": education,
            "Work Experience": work_exp,
        })
    except Exception as e:
        st.error(f"Error displaying content: {e}")

# Load resumes and job description from the folder
path_of_resume_folder = './uploaded_resumes'  # Path to the resume folder
path_of_jd_folder = './job_description_datasets'  # Path to the jd folder
# Job description input
job_description = st.file_uploader("Please upload a job description in pdf format", type=["pdf"])


# Check if the folders exist
if os.path.exists(path_of_resume_folder):
    # Get the list of files in the folder
    files = os.listdir(path_of_resume_folder)
    jd_file = os.listdir(path_of_jd_folder)
    if files:
        st.write("Uploaded Resumes:")
        # Display the list of file names
        for file in files:
            # Create a button for each file
            if st.button(f"Show Content: {file}", key=f"btn_{file}"):
                file_path = os.path.join(path_of_resume_folder, file)
                show_content(file_path)  # Call the function to display the resume content
                # Calculate Resume-Job Match Score
            if job_description:
                file_path = os.path.join(path_of_resume_folder, file)
                original_text = read_file(file_path)
                jd_path = os.path.join(path_of_jd_folder, str(jd_file[0]))
                jd_text = read_file(jd_path)
                if not original_text:
                    st.error("Failed to extract content from the file.")
                resume_score = evaluate_resume(original_text, jd_text)
                st.write(f"**Resume-Job Match Score**: {resume_score * 100:.2f}%")
                cleaned_text = clean_text(original_text)
                skills = extract_skills_section(cleaned_text)
                work_exp = extract_work_experience(original_text)
                if st.button(f"Show Feedback:{file}", key = f'feedback{file}'):
                    feedback = generate_feedback(original_text, jd_text, resume_score)
                    st.write(f"Your feedback is ready! just look into it {feedback}")                   

                #st.write(type(original_text), type(jd_text))
                
    else:
        st.error(f"No resumes found in the folder '{path_of_resume_folder}'.")
else:
    st.error(f"The folder '{path_of_resume_folder}' does not exist.")


>>>>>>> 9b81f7a7d3c44723808206d97a1f66adffe7e7eb
