import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model function
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# Extract PDF Text
def extract_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Define Prompts
def generate_prompt(text, jd):
    return f"""
    Act like a professional ATS (Application Tracking System) with expertise in software engineering, data science, data engineering and analytics, Machine Learning Engineer.
    Analyze the resume below against the provided job description.
    Be specific and provide detailed insights:
    
    Resume: {text}
    Job Description: {jd}

    Respond with JSON format:
    {{
        "JD Match": "%",
        "MissingKeywords": [],
        "Profile Summary": ""
    }}
    """

def improvise_prompt(text):
    return f"Based on this resume: {text}, how can the candidate improve their technical and soft skills to align with top industry standards?"

def missing_keywords_prompt(text, jd):
    return f"From this resume: {text} and job description: {jd}, list all missing keywords that are important for a better ATS score."

def profile_summary_prompt(text):
    return f"Read this resume: {text} and generate a crisp 4-5 line professional summary that highlights the candidate's strengths."

# Streamlit UI
st.set_page_config(page_title="Application Tracking System Insights")
st.title("Application Tracking System Insight")
st.markdown("Analyze and Improve your Resume to Match Job Descriptions using AI.")

jd = st.text_area("📌 Job Description")
uploaded_file = st.file_uploader("📎 Upload your Resume (PDF Only)", type=["pdf"])

if uploaded_file and jd:
    resume_text = extract_pdf_text(uploaded_file)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Tell Me About the Resume"):
            summary_prompt = profile_summary_prompt(resume_text)
            response = get_gemini_response(summary_prompt)
            st.subheader("🧾 Profile Summary")
            st.write(response)

        if st.button("How Can I Improvise my Skills"):
            improve_prompt = improvise_prompt(resume_text)
            response = get_gemini_response(improve_prompt)
            st.subheader("🔧 Skill Improvement Suggestions")
            st.write(response)

    with col2:
        if st.button("What are the Keywords That are Missing"):
            missing_prompt = missing_keywords_prompt(resume_text, jd)
            response = get_gemini_response(missing_prompt)
            st.subheader("❌ Missing Keywords")
            st.write(response)

        if st.button("Percentage match"):
            final_prompt = generate_prompt(resume_text, jd)
            response = get_gemini_response(final_prompt)
            st.subheader("✅ ATS Match Result")
            st.write(response)