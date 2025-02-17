from io import StringIO as cStringIO
import tensorflow_hub as hub
import numpy as np
from resume_sections import extract_skills_section, extract_work_experience
from helper import clean_text

# Load Universal Sentence Encoder (USE) model
model_path  = r"C:\Users\ashis\OneDrive\Desktop\DATA SCIENCE WORK\models\universal-sentence-encoder-tensorflow2-universal-sentence-encoder-v2"
use_model = hub.load(model_path)

def get_average_vector(text, model):
    """
    Encode the input text using the USE model to get the embedding vector.
    
    Args:
        text (str): Input text to encode.
        model (tensorflow_hub.Module): Loaded Universal Sentence Encoder model.

    Returns:
        numpy.ndarray: Embedding vector for the input text.
    """
    return model([text])[0].numpy()

def calculate_similarity_use(text1, text2, model):
    """
    Calculate cosine similarity between two pieces of text using the USE model.
    
    Args:
        text1 (str): First text.
        text2 (str): Second text.
        model (tensorflow_hub.Module): Loaded Universal Sentence Encoder model.

    Returns:
        float: Cosine similarity score between the two texts.
    """
    vec1 = get_average_vector(text1, model)
    vec2 = get_average_vector(text2, model)
    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return similarity

def calculate_skills_similarity(resume_skills, job_description, model):
    """
    Calculate the similarity score between resume skills and job description.
    
    Args:
        resume_skills (str): Extracted skills from the resume.
        job_description (str): Job description text.
        model (tensorflow_hub.Module): Loaded Universal Sentence Encoder model.

    Returns:
        float: Similarity score between skills and job description.
    """
    return calculate_similarity_use(resume_skills, job_description, model)

def calculate_experience_similarity(resume_experience, job_description, model):
    """
    Calculate the similarity score between resume work experience and job description.
    
    Args:
        resume_experience (str): Extracted work experience from the resume.
        job_description (str): Job description text.
        model (tensorflow_hub.Module): Loaded Universal Sentence Encoder model.

    Returns:
        float: Similarity score between work experience and job description.
    """
    return calculate_similarity_use(resume_experience, job_description, model)

def flatten_text(input_data):
    """
    Converts input data into a string if it's a dictionary or list of dictionaries.
    """
    if isinstance(input_data, dict):
        return " ".join([f"{k}: {v}" for k, v in input_data.items()])
    elif isinstance(input_data, list):
        return " ".join([flatten_text(item) for item in input_data])
    elif isinstance(input_data, str):
        return input_data
    else:
        return ""

def get_average_vector(text, model):
    # Ensure the text is flattened into a plain string
    text = flatten_text(text)
    return model([text])[0].numpy()

def evaluate_resume(resume_text, job_description):
    resume_text = clean_text(resume_text)
    jd_text = clean_text(job_description) if job_description else ""
    
    # Extract and flatten sections
    skills = flatten_text(extract_skills_section(resume_text))
    work_experience = flatten_text(extract_work_experience(resume_text))

    if not skills or not work_experience or not jd_text:
        return 0  # Return 0 if any critical text section is missing

    # Calculate similarity scores
    skills_score = calculate_skills_similarity(skills, jd_text, use_model)
    experience_score = calculate_experience_similarity(work_experience, jd_text, use_model)

    # Weighted average score
    total_score = 0.7*skills_score + 0.3*experience_score
    return total_score

