<<<<<<< HEAD
# Advanced Resume Analyzer

## Project Overview
The Advanced Resume Analyzer is a two-part application designed to streamline the resume evaluation process. It consists of two integrated applications:

1. **Upload Resume App:** Designed for candidates to upload their resumes.
2. **Analysis App:** Built to analyze collected resumes, score them based on job requirements, and provide constructive feedback.

## Key Features
- Resume Upload Portal for candidates. And uploaded resumes will be automatically   reflected in uploaded_resume folder.
- Resume Scoring Algorithm using Word2Vec similarity with job descriptions.
- Detailed Feedback highlighting strengths and gaps in resumes.
- Evaluation based on skills, work experience, and alignment with job requirements.

## Technologies Used
- **Python**
-**Document reader** (PyMuPDF, textract, docx.Document)
- **WordNetLemmatizer, word_tokenize** (from nltk library)
-**regular expression**(pattern serching for contact details, skills, job experiences and else)
**"universal-sentence-encoder-tensorflow2-universal-sentence-encoder-v2" and tensorflow hub**(for loading sentence encoder and encoding sentences)
- **NLP Libraries** (spaCy, NLTK)
- **Streamlit** (for interactive web application)
- **GPT2** (for feedback section)
## How It Works
### Upload Resume App
- Candidates can upload their resumes through a simple interface.


## Contributing
Feel free to contribute to this project by submitting issues or pull requests.


## Contact
For questions or suggestions, contact **Ashis Khan** via GitHub or LinkedIn.

=======
**Advanced Resume Analyzer**

**Project Overview**

The Advanced Resume Analyzer is an AI-powered evaluation system that automates resume assessment, scores candidates based on job requirements, and generates professional feedback emails with selection decisions.


**It comprises two integrated applications:**

**Resume Collecting App:** Collects resumes from candidates and saves them to the uploaded_resumes folder.

**Resume Analysis App:** Analyzes collected resumes, evaluates their alignment with the provided job description, and generates personalized feedback for recruiters and candidates.

**Key Features:**

- **Resume Upload Interface:** Candidates can easily upload their resumes.

- **Automated Resume Scoring:** Uses advanced NLP techniques and Word2Vec similarity to match resumes with job descriptions.

- **Candidate Evaluation**: Extracts contact details, skills, and work experience to evaluate resume content.

- **Professional Feedback Generation**: Produces recruiter insights and auto-generates email drafts (decision of selection or rejection) with constructive feedback.

**Technologies Used**

- Python

- PyMuPDF, textract, docx.Document – For resume extraction from various document formats.

- Regular Expressions (re) – For extracting contact details, skills, and work experience.

- NLTK (WordNetLemmatizer, word_tokenize) – Text preprocessing and tokenization.

- TensorFlow Hub – Universal Sentence Encoder – For semantic similarity evaluation.

- Streamlit – Interactive web-based interface.

- Hugging Face

- Mistral-7B-Instruct-v0.2 – For generating professional feedback and email content.

- Langchain

**Application Structure**

- 1. **Resume Collecting App**

- File: resume_collecting_app.py

- Function: Provides an interface for candidates to upload resumes.

- Resumes are saved automatically to the uploaded_resumes folder.

2. **Resume Analysis App**

- Files:

- analysis_app.py – Main application file for analysis and feedback.

- scor_pred.py – Logic for resume scoring based on skills and experience.

- resume_section.py – Extracts details like skills, work experience, and contact information.

- llm_feedback.py – Calls Hugging Face API to generate recruiter feedback and email drafts.

- job_description_datasets: uploaded job description file in pdf format
- uploaded_resumes: collected resumes from resume_collecting_app application
- nltk_work: preprocessing of resumes
- helper.py: resume loading and cleaning

**How It Works**

- Upload Resumes: Candidates upload resumes via the collecting app.

- Analyze Resumes: Recruiters input a job description, and the analysis app evaluates each uploaded resume.

- Score and Feedback: Resumes are scored based on alignment with the job description, and professional feedback is generated for each candidate.

- Email Drafts: Selection or rejection email templates are auto-generated with candidate-specific feedback.

**Contributing**

Contributions are welcome! Feel free to submit issues or pull requests.

**Contact**

For inquiries or suggestions, reach out to Ashis Khan via GitHub or LinkedIn.

>>>>>>> 9b81f7a7d3c44723808206d97a1f66adffe7e7eb
