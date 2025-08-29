import streamlit as st
from dotenv import load_dotenv
import os

# It's better to handle imports at the top
from pdf_processing import process_pdf
from analysis import analyse_profile

# Load environment variables
load_dotenv()

# App Header
st.header("📄 Scan My :blue[CV.ai]", divider="green")
st.subheader("💡 Tips for Using the Application")

notes = '''
- **Upload Your Resume (PDF only):** Please upload your resume in PDF format.
- **Paste the Job Description:** Copy and paste the full job description for an accurate analysis.
- **Get AI-Powered Insights:** Leverage AI to see how your resume matches up against the job description.
'''
st.markdown(notes)

# Sidebar
with st.sidebar:
    st.subheader("📥 Upload Your Resume")
    pdf_doc = st.file_uploader("Choose a resume (PDF format)", type=["pdf"])
    st.markdown("---")
    st.markdown("👨‍💻 Created by: :red[Rajat Latwal]")

# Job Description Input
st.subheader("📝 Enter the Job Description", divider=True)
job_desc = st.text_area(
    label="Paste the job description from job boards (e.g., LinkedIn, Indeed)",
    height=300,
    placeholder="e.g., We're looking for a Data Analyst with experience in Python, SQL, and Tableau..."
)

# --- New Feature: User Question Input ---
st.subheader("❓ Ask a Specific Question (Optional)", divider=True)
user_question = st.text_input(
    label="Ask a question about your resume or provide a custom instruction.",
    placeholder="e.g., How can I rephrase my experience at XYZ Corp to highlight leadership skills?"
)


submit = st.button("🚀 Get AI-Powered Insights")

if submit:
    # --- 1. Input Validation ---
    if pdf_doc is not None and job_desc.strip() != "":
        # --- 2. Use a Spinner for better UX ---
        with st.spinner("Analyzing your profile... This may take a moment."):
            try:
                # Extract text from the PDF
                resume_text = process_pdf(pdf_doc)

                # Get the analysis from the Gemini model, now with the user's question
                analysis_result = analyse_profile(
                    resume_text=resume_text,
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

