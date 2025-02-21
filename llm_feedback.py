<<<<<<< HEAD
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
=======
import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load GPT-2 model and tokenizer
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Add a padding token if not already present
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def clean_text(text):
    """Remove unnecessary repetition and excessive details."""
    lines = text.split("\n")
    unique_lines = list(dict.fromkeys(lines))  # Remove duplicates while preserving order
    return " ".join(unique_lines)

def generate_feedback(resume_text, job_description, resume_score):
    def truncate_text(text, max_tokens):
        """Helper function to truncate text to a specific number of tokens."""
        if not isinstance(text, str):
            text = str(text)

        tokens = tokenizer.tokenize(text)
        return tokenizer.convert_tokens_to_string(tokens[:max_tokens])

    # Preprocess inputs
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    # Maximum token limits for each part
    max_resume_tokens = 200
    max_job_desc_tokens = 200

    # Truncate inputs
    truncated_resume = truncate_text(resume_text, max_resume_tokens)
    truncated_job_desc = truncate_text(job_description, max_job_desc_tokens)

    # Construct the prompt
    prompt = f"""
You are an expert career consultant. Evaluate the quality of the given resume compared to the job description. Provide detailed feedback on the strengths, weaknesses, and areas for improvement.

Resume:
{truncated_resume}

Job Description:
{truncated_job_desc}

Resume Score: {resume_score}

Feedback:
1. Strengths:
2. Weaknesses:
3. Suggestions for Improvement:
    """

    # Encode the input prompt
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=300)
    input_length = inputs["input_ids"].shape[1]

    # Calculate remaining tokens for generation
    max_allowed_length = 1024
    available_tokens_for_generation = max_allowed_length - input_length

    if available_tokens_for_generation <= 0:
        raise ValueError("The input prompt is too long after truncation.")

    # Generate feedback
    outputs = model.generate(
        inputs["input_ids"], 
        max_new_tokens=min(available_tokens_for_generation, 300), 
        num_return_sequences=1
    )
    generated_feedback = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_feedback

>>>>>>> 9b81f7a7d3c44723808206d97a1f66adffe7e7eb
