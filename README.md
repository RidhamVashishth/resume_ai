# **Scan My Resume \- AI-Powered Resume Analyzer**

An intelligent web application built with Streamlit that analyzes a user's resume against a specific job description, providing an ATS-style match score, detailed feedback, and answers to custom questions.
You can access the app here https://analyseuresume.streamlit.app/

## **Overview**

Scan My CV.ai is designed to help job seekers optimize their resumes for specific job applications. By leveraging the multimodal capabilities of Google's Gemini Pro model, the tool can process resumes in various formats (PDF, DOCX, and even images) and deliver a comprehensive analysis. Users receive actionable insights, including a percentage match score, identified strengths and weaknesses, and concrete recommendations for improvement, bridging the gap between their qualifications and the employer's needs.

### **Features**

* **Multi-Format Resume Upload**: Accepts resumes in the most common formats: PDF, Microsoft Word (.docx), and images (.png, .jpg, .jpeg).  
* **Comprehensive ATS Analysis**: Provides a detailed report that includes an overall match score, a breakdown of strengths, and areas for improvement.  
* **Actionable Recommendations**: Offers specific, AI-generated suggestions to help users tailor their resume to better match the job description.  
* **Interactive Q\&A**: Allows users to ask specific questions about their resume in the context of the job description (e.g., "How can I better highlight my leadership skills?").  
* **User-Friendly Interface**: A clean and intuitive web interface built with Streamlit for a seamless user experience.  
* **Powered by Google Gemini**: Utilizes the advanced reasoning and multimodal capabilities of the gemini-1.5-flash model.

## **Technology Stack**

* **Language**: Python  
* **Framework**: Streamlit  
* **AI Model**: Google Gemini (gemini-1.5-flash)  
* **Core Libraries**:  
  * google-generativeai  
  * pypdf for PDF text extraction  
  * python-docx for Word document processing  
  * Pillow for image handling  
  * python-dotenv for environment variable management

## **Local Setup and Installation**

To run this project on your local machine, please follow these steps.

### **Prerequisites**

* Python 3.8 or higher  
* A Google API Key with the Generative Language API enabled. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### **1\. Clone the Repository**

git clone \<your-repository-url\>  
cd \<repository-directory\>

### **2\. Create a Virtual Environment**

It is highly recommended to use a virtual environment to manage project dependencies.

\# For Windows  
python \-m venv venv  
venv\\Scripts\\activate

\# For macOS/Linux  
python3 \-m venv venv  
source venv/bin/activate

### **3\. Install Dependencies**

Create a requirements.txt file in the root of your project with the following content, and then run the installation command.

**requirements.txt**:

streamlit  
python-dotenv  
pypdf  
google-generativeai  
python-docx  
Pillow

**Installation Command**:

pip install \-r requirements.txt

### **4\. Configure Environment Variables**

Create a file named .env in the root directory and add your Google API key.

GOOGLE\_API\_KEY='YOUR\_API\_KEY\_HERE'

### **5\. Run the Application**

Launch the Streamlit app from your terminal.

streamlit run app.py

The application should now be running and accessible in your web browser, typically at http://localhost:8501.

## **Usage**

1. Open the application in your web browser.  
2. In the sidebar, click the "Choose a resume file" button to upload your resume (PDF, DOCX, or image).  
3. Paste the full job description into the "Enter the Job Description" text area.  
4. (Optional) If you have a specific question, type it into the "Ask a Specific Question" text box.  
5. Click the "Get AI-Powered Insights" button to generate your analysis.  
6. The detailed report will appear on the main page.

## **License**

This project is licensed under the MIT License. See the LICENSE file for more details.
