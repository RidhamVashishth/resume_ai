import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image

# Centralized configuration at the top
load_dotenv()
try:
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    # It's better to import and configure genai here
    import google.generativeai as genai
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API Configuration Error: {e}")
    st.stop() # Stop the app if config fails

# Now, import your other modules
from file_processing import process_file
from analysis import analyse_profile

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

