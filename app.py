import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai
from pypdf import PdfReader
import docx
import io

# --- Configuration ---
# Centralized configuration at the top
load_dotenv()
try:
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API Configuration Error: {e}")
    st.stop() # Stop the app if config fails

# --- Helper Functions (from file_processing.py and analysis.py) ---

@st.cache_data(show_spinner="Processing Document...")
def process_file(uploaded_file):
    """
    Extracts content from an uploaded file.
    Returns text for PDF/DOCX or a PIL Image object for images.
    """
    if uploaded_file is None:
        return None

    file_type = uploaded_file.type
    
    # Handle PDF files
    if file_type == "application/pdf":
        text = ""
        try:
            pdf_reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return None
            
    # Handle DOCX files
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = ""
        try:
            doc = docx.Document(io.BytesIO(uploaded_file.getvalue()))
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading DOCX file: {e}")
            return None
            
    # Handle Image files
    elif file_type in ["image/png", "image/jpeg"]:
        try:
            return Image.open(uploaded_file)
        except Exception as e:
            st.error(f"Error reading image file: {e}")
            return None
            
    return None

def analyse_profile(resume_content, job_desc, user_question):
    """
    Analyzes a resume (text or image) against a job description.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    if resume_content is None or not job_desc:
        return "Error: Resume content or job description is missing."

    # --- Prepare the model input list ---
    model_input = []
    
    # --- Dynamic Prompting Logic ---
    if user_question:
        prompt_template = f"""
        You are an expert HR Executive and a professional career coach. Your task is to answer the user's specific question using the provided resume and job description as context. Provide advice as if you were guiding a candidate through the hiring process.

        **Job Description:**
        ```
        {job_desc}
        ```

        **User's Question:**
        "{user_question}"

        Please provide a direct and helpful answer to the user's question, using the resume to inform your expert response.
        """
    else:
        prompt_template = f"""
        You are an expert HR Executive and a professional career coach with deep experience in using Applicant Tracking Systems (ATS). 
        Your task is to evaluate a candidate's resume against a provided job description from a hiring manager's perspective.

        **Job Description:**
        ```
        {job_desc}
        ```
        
        Please analyze the resume and provide a detailed analysis with the following structure, using Markdown for formatting:

        **1. Overall Match Score:**
        - Provide a percentage score representing how well the resume matches the job description.
        - Briefly justify the score in one sentence.

        **2. Strengths:**
        - In bullet points, list key skills and experiences from the resume that are a strong match for the job description.

        **3. Areas for Improvement:**
        - In bullet points, identify crucial keywords or skills from the job description that are missing from the resume.

        **4. Actionable Recommendations:**
        - In bullet points, provide specific, actionable advice on how the candidate can improve their resume to better align with this job.
        """

    # Add the resume content (either image or text) and the final prompt to the model input
    if isinstance(resume_content, str):
        # It's a text resume
        final_prompt = f"{prompt_template}\n\n**Resume Text:**\n```\n{resume_content}\n```"
        model_input.append(final_prompt)
    elif isinstance(resume_content, Image.Image):
        # It's an image resume
        final_prompt = f"{prompt_template}\n\n**Resume Analysis:**\nPlease analyze the content of the provided resume image."
        model_input.append(resume_content)
        model_input.append(final_prompt)
    else:
        return "Error: Invalid resume content type."

    try:
        response = model.generate_content(model_input)
        return response.text
    except Exception as e:
        st.error(f"Error during AI analysis: {e}")
        return "Sorry, an error occurred while analyzing the profile."

# --- Main App UI ---

# App Header
st.header("📄 Scan My :blue[CV.ai]", divider="green")
st.subheader("💡 Tips for Using the Application")

notes = '''
- **Upload Your Resume:** Please upload your resume in PDF, DOCX, or Image (PNG, JPG) format.
- **Paste the Job Description:** Copy and paste the full job description for an accurate analysis.
- **Get AI-Powered Insights:** Leverage AI to see how your resume matches up against the job description.
'''
st.markdown(notes)

# Sidebar
with st.sidebar:
    st.subheader("📥 Upload Your Resume")
    # Updated file uploader to accept multiple formats
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=["pdf", "docx", "png", "jpg", "jpeg"]
    )
    st.markdown("---")
    st.markdown("👨‍💻 Created by: :red[Rajat Latwal]")

# Job Description Input
st.subheader("📝 Enter the Job Description", divider=True)
job_desc = st.text_area(
    label="Paste the job description from job boards (e.g., LinkedIn, Indeed)",
    height=300,
    placeholder="e.g., We're looking for a Data Analyst with experience in Python, SQL, and Tableau..."
)

# User Question Input
st.subheader("❓ Ask a Specific Question (Optional)", divider=True)
user_question = st.text_input(
    label="Ask a question about your resume or provide a custom instruction.",
    placeholder="e.g., How can I rephrase my experience at XYZ Corp to highlight leadership skills?"
)

submit = st.button("🚀 Get AI-Powered Insights")

if submit:
    # Input Validation
    if uploaded_file is not None and job_desc.strip() != "":
        with st.spinner("Analyzing your profile... This may take a moment."):
            try:
                # Process the uploaded file to get text or an image object
                resume_content = process_file(uploaded_file)

                # Get the analysis from the Gemini model
                analysis_result = analyse_profile(
                    resume_content=resume_content,
                    job_desc=job_desc,
                    user_question=user_question
                )

                # Display the result
                st.subheader("🔍 Analysis Report")
                st.markdown(analysis_result)

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
    else:
        st.error("⚠️ Please upload your resume and paste the job description before submitting.")
