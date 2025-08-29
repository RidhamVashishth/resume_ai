import streamlit as st
import google.generativeai as genai
import os

# Configure the Gemini API key
try:
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API Configuration Error: {e}")

# Set up the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def analyse_profile(resume_text, job_desc, user_question):
    """
    Analyzes a resume against a job description using the Gemini model.
    Handles both a default analysis and specific user questions.

    Args:
        resume_text: The text content of the resume.
        job_desc: The text content of the job description.
        user_question: A specific question from the user (can be empty).

    Returns:
        A formatted string containing the AI's analysis.
    """
    if not resume_text or not job_desc:
        return "Error: Resume text or job description is missing."

    # --- Dynamic Prompting Logic ---
    if user_question:
        # If the user asked a specific question, use the HR Executive persona to answer.
        input_prompt = f"""
        You are an expert HR Executive and a professional career coach. Your task is to answer the user's specific question using their resume and the provided job description as context. Provide advice as if you were guiding a candidate through the hiring process.

        **Resume Text:**
        ```
        {resume_text}
        ```

        **Job Description:**
        ```
        {job_desc}
        ```

        **User's Question:**
        "{user_question}"

        Please provide a direct and helpful answer to the user's question, using the resume and job description to inform your expert response.
        """
    else:
        # If no specific question is asked, perform the default, comprehensive analysis from an HR perspective.
        input_prompt = f"""
        You are an expert HR Executive and a professional career coach with deep experience in using Applicant Tracking Systems (ATS). 
        Your task is to evaluate a candidate's resume against a provided job description from a hiring manager's perspective.

        **Resume Text:**
        ```
        {resume_text}
        ```

        **Job Description:**
        ```
        {job_desc}
        ```

        Please provide a detailed analysis with the following structure, using Markdown for formatting:

        **1. Overall Match Score:**
        - Provide a percentage score representing how well the resume matches the job description (e.g., 85%).
        - Briefly justify the score in one sentence.

        **2. Strengths:**
        - In bullet points, list the key skills, experiences, or qualifications from the resume that are a strong match for the job description.

        **3. Areas for Improvement:**
        - In bullet points, identify crucial keywords, skills, or experiences mentioned in the job description that are missing from the resume.

        **4. Actionable Recommendations:**
        - In bullet points, provide specific, actionable advice on how the candidate can improve their resume to better align with this job description. For example, suggest adding specific project details, quantifying achievements, or incorporating missing keywords.
        """

    try:
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error during AI analysis: {e}")
        return "Sorry, an error occurred while analyzing the profile."

