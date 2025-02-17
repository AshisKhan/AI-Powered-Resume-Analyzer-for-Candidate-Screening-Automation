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


