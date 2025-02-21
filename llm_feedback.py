import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


API_TOKEN = os.getenv("API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def clean_text(text):
    """Remove duplicates and reduce excessive content."""
    lines = text.split("\n")
    unique_lines = list(dict.fromkeys(lines))
    return " ".join(lines)

def truncate_text(text, max_length=3000):
    return text[:max_length]


def estimate_token_count(text):
    """Rough estimate of token count based on words and symbols."""
    return len(text.split()) + text.count('\n') + text.count('.')

def generate_feedback(resume_text, job_description, resume_score):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    truncated_resume = truncate_text(resume_text, 1500)
    truncated_job_desc = truncate_text(job_description, 1500)

    prompt = f"""
You are an expert resume analyzer assisting recruiters in evaluating candidates. Analyze the given resume against the job description and the resume score. Extract the candidate's **name, email, and phone number** from the resume text to personalize the email communication. Any how do not make the feedback as same as content

Your goal is to provide the following:

1. **Evaluation for the Recruiter:**  
   - Highlight key strengths that match the job description.
   - Identify gaps or weaknesses relevant to the role.
   - Make a hiring recommendation:
     - "Proceed to Interview" → If the candidate is a strong match.
     - "Reject with Feedback" → If the candidate is not suitable.

2. **Extract Contact Details:**  
   Extract the candidate's:
   - Full Name (if available)
   - Email Address (if available)
   - Phone Number (if available)  
   Use this information to personalize the email.

3. **Generate ONE Email Template (Based on Hiring Recommendation):**
   - **If "Proceed to Interview":** Draft a professional interview invitation email, including next steps and interview details.
   - **If "Reject with Feedback":** Draft a polite rejection email, providing brief, constructive feedback on why the application was unsuccessful.

**IMPORTANT INSTRUCTIONS:**
- Avoid redundancy; be concise and professional.
- Output only ONE email based on your hiring recommendation.
- Use the extracted candidate's name, email, and phone number in the email if available.
- If contact details are not found, address the candidate as "Applicant".

---

Resume Score: {resume_score}

Resume:
{truncated_resume}

Job Description:
{truncated_job_desc}

Evaluation, Hiring Recommendation, Extracted Contact Details, and Personalized Email Template:
"""




    # Estimate prompt size in tokens (Mistral context limit is 4096 tokens)
    estimated_prompt_tokens = estimate_token_count(prompt)
    remaining_tokens = 4096 - estimated_prompt_tokens

    # Allocate tokens for output (but not too large to avoid wasting resources)
    max_new_tokens = min(max(remaining_tokens, 200), 500)

    # API Request
    payload = {
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 500,
        "temperature": 0.5,
        "top_p": 0.8,
    }
}


    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise ValueError(f"Request failed: {response.status_code}, {response.text}")

    result = response.json()
    feedback_text = result[0]["generated_text"]

    feedback_text = feedback_text.replace(prompt, "").strip()
    return feedback_text
