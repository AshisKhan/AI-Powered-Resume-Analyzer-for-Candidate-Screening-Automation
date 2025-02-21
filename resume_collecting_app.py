<<<<<<< HEAD
import streamlit as st


st.title("Resume Collector")
st.write("Drag and drop your file here.")

resume = st.file_uploader("Please upload a supported file of your resume", type=["pdf", "docx", "txt"])



def uploading(resume):
    submit = st.button("submit")
    try:
        if submit:
            res_name = resume.name
            with open(f'./uploaded_resumes/{res_name}', "wb") as temp_file:
                temp_file.write(resume.getbuffer())
                st.success("File submitted successfully!")
        
        
    
    except Exception as e:
        print(f"Error processing {temp_file}: {e}")
    
        
if resume:
    # Validate file size (ensure it's within the 2MB limit)
    file_size_mb = len(resume.getbuffer()) / (1024 * 1024)  # Convert bytes to MB
    if file_size_mb < 2:
        st.success("File uploaded successfully!")
        uploading(resume)
    else:
        st.text('Please select a resume with file size lesser than 2 MB')


=======
import streamlit as st


st.title("Resume Collector")
st.write("Drag and drop your file here.")

resume = st.file_uploader("Please upload a supported file of your resume", type=["pdf", "docx", "txt"])



def uploading(resume):
    submit = st.button("submit")
    try:
        if submit:
            res_name = resume.name
            with open(f'./uploaded_resumes/{res_name}', "wb") as temp_file:
                temp_file.write(resume.getbuffer())
                st.success("File submitted successfully!")
        
        
    
    except Exception as e:
        print(f"Error processing {temp_file}: {e}")
    
        
if resume:
    # Validate file size (ensure it's within the 2MB limit)
    file_size_mb = len(resume.getbuffer()) / (1024 * 1024)  # Convert bytes to MB
    if file_size_mb < 2:
        st.success("File uploaded successfully!")
        uploading(resume)
    else:
        st.text('Please select a resume with file size lesser than 2 MB')


>>>>>>> 9b81f7a7d3c44723808206d97a1f66adffe7e7eb
