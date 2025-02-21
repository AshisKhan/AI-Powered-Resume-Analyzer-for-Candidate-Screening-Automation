import re

def extract_name(text):
    try:
        # Regex pattern to capture capitalized names
        name_pattern = r"^[A-Z][a-z]+\s[A-Z][a-z]+"

        match = re.search(name_pattern, text)
        if match:
            return  match.group()
        else:
            return None
    except Exception as e:
        return "No name found (Error: {})".format(e)

def extract_contact_info(text):
    try:
        # Extract email
        email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        email = email.group() if email else None
        
        # Extract phone number
        phone = re.search(r'\+?[0-9][0-9\s.-]{8,15}', text)
        phone = phone.group() if phone else None
        
        # Extract LinkedIn/GitHub URLs
        urls = re.findall(r'(https?://(www\.)?(linkedin|github)\.com/[^\s]+)', text)
        urls = [url[0] for url in urls] if urls else None
        
        return {"email": email, "phone": phone, "urls": urls}
    except Exception as e:
        return "No contact info found (Error: {})".format(e)
    

def extract_education(text):
    try:
        # Simple education extraction based on degrees
        education_keywords = ["Bachelor", "Master", "B.Sc", "M.Sc", "Ph.D", "BE", "BTech", "MTech", "MBA"]
        education = [line for line in text.split("\n") if any(degree in line for degree in education_keywords)]
        return education
    except Exception as e:
        return "No education found (Error: {})".format(e)
    

def extract_skills_section(text):
    try:
        # Define patterns for the "Skills" section start and end
        start_pattern = r'\bSkills\b[:\-]?'  # Look for "Skills" (case-insensitive)
        end_patterns = [r'\bWork Experience\b', r'\bEducation\b', r'\bProjects\b', r'\bCertifications\b']  # Common section names
        
        # Search for the start of the skills section
        start_match = re.search(start_pattern, text, re.IGNORECASE)
        
        if not start_match:
            return None  # Return None if no "Skills" section is found
        
        start_index = start_match.end()  # Start extracting after "Skills"

        # Search for the first occurrence of any end section after the skills section
        end_index = len(text)  # Default end index is the end of the text
        for end_pattern in end_patterns:
            end_match = re.search(end_pattern, text[start_index:], re.IGNORECASE)
            if end_match:
                end_index = start_index + end_match.start()
                break
        
        # Extract and clean the skills section
        skills_section = text[start_index:end_index].strip()
        
        # Optional: Clean up the extracted skills (e.g., remove bullets, extra spaces)
        skills_section = re.sub(r'[\n\r\t•\-]', ' ', skills_section)  # Replace bullets and newlines with spaces
        skills_section = re.sub(r'\s+', ' ', skills_section)  # Remove extra spaces
        
        return skills_section
    except Exception as e:
        return "No skills found (Error: {})".format(e)



def extract_work_experience(text):
    try:
        # Split the resume into lines for processing
        lines = text.split("\n")
        
        # Initialize an empty list for work experience
        work_experience = []
        
        # Define keywords for job titles and work-related sections
        job_keywords = ["Engineer", "Developer", "Scientist", "Manager", "Consultant", "Analyst", "Intern",'Specialist','lead']
        duration_pattern = r'\b(?:Jan|Feb|Mar|Apr|May| Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s?\d{4} - \s?(?:Present|\d{4})\b'
        
        for i, line in enumerate(lines):
            # Look for a duration
            duration = re.search(duration_pattern, line)
            duration = duration.group() if duration else None
            # Check if line contains job-related keywords
            if any(keyword in line for keyword in job_keywords):
                # Capture job title
                job_title = line
                
                # Capture responsibilities (next few lines until a new section)
                responsibilities = []
                for j in range(i + 1, len(lines)):
                    if any(section in lines[j].lower() for section in ["education", "skills", "certifications", "projects"]):
                        break
                    if lines[j].strip():  # Add non-empty lines
                        responsibilities.append(lines[j+1].strip())
                
                # Add extracted work experience
                work_experience.append({
                    "job_title": job_title,
                    "duration": duration,
                    "responsibilities": responsibilities
                })
        
        return work_experience
    except Exception as e:
        return "No work experiences found (Error: {})".format(e)


