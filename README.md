Advanced Resume Analyzer

Project Overview

The Advanced Resume Analyzer is an AI-powered evaluation system that automates resume assessment, scores candidates based on job requirements, and generates professional feedback emails with selection decisions.

It comprises two integrated applications:

Resume Collecting App: Collects resumes from candidates and saves them to the uploaded_resumes folder.

Resume Analysis App: Analyzes collected resumes, evaluates their alignment with the provided job description, and generates personalized feedback for recruiters and candidates.

Key Features

Resume Upload Interface: Candidates can easily upload their resumes.

Automated Resume Scoring: Uses advanced NLP techniques and Word2Vec similarity to match resumes with job descriptions.

Candidate Evaluation: Extracts contact details, skills, and work experience to evaluate resume content.

Professional Feedback Generation: Produces recruiter insights and auto-generates email drafts (decision of selection or rejection) with constructive feedback.

Technologies Used

Python

PyMuPDF, textract, docx.Document – For resume extraction from various document formats.

Regular Expressions (re) – For extracting contact details, skills, and work experience.

NLTK (WordNetLemmatizer, word_tokenize) – Text preprocessing and tokenization.

TensorFlow Hub – Universal Sentence Encoder – For semantic similarity evaluation.

Streamlit – Interactive web-based interface.

Hugging Face

Mistral-7B-Instruct-v0.2 – For generating professional feedback and email content.

Langchain

Application Structure

1. Resume Collecting App

File: resume_collecting_app.py

Function: Provides an interface for candidates to upload resumes.

Resumes are saved automatically to the uploaded_resumes folder.

2. Resume Analysis App

Files:

app.py – Main application file for analysis and feedback.

resume_scoring.py – Logic for resume scoring based on skills and experience.

resume_extraction.py – Extracts details like skills, work experience, and contact information.

feedback_generation.py – Calls Hugging Face API to generate recruiter feedback and email drafts.

requirements.txt – Lists required libraries and dependencies.

How It Works

Upload Resumes: Candidates upload resumes via the collecting app.

Analyze Resumes: Recruiters input a job description, and the analysis app evaluates each uploaded resume.

Score and Feedback: Resumes are scored based on alignment with the job description, and professional feedback is generated for each candidate.

Email Drafts: Selection or rejection email templates are auto-generated with candidate-specific feedback.

Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

Contact

For inquiries or suggestions, reach out to Ashis Khan via GitHub or LinkedIn.

