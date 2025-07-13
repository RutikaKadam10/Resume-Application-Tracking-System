import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🚫 GOOGLE_API_KEY not set. Please set it in app.yaml or GCP secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Gemini model function
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"

# Extract PDF Text
def extract_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompts
def generate_prompt(text, jd):
    return f"""
    Act like a professional ATS system. Analyze the resume below against the provided job description.

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
    return f"Based on this resume: {text}, how can the candidate improve their technical and soft skills?"

def missing_keywords_prompt(text, jd):
    return f"From this resume: {text} and job description: {jd}, list all missing keywords."

def profile_summary_prompt(text):
    return f"Summarize this resume into 4-5 lines highlighting the candidate's strengths: {text}"

# Streamlit App UI
st.set_page_config(page_title="Application Tracking System")
st.title("📄 Application Tracking System Insight")
st.markdown("Analyze and Improve your Resume to Match Job Descriptions using Gemini AI.")

jd = st.text_area("📌 Paste the Job Description here")
uploaded_file = st.file_uploader("📎 Upload your Resume (PDF Only)", type=["pdf"])

if not jd or not uploaded_file:
    st.info("ℹ️ Please provide both Job Description and Resume to proceed.")

if uploaded_file and jd:
    resume_text = extract_pdf_text(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Tell Me About the Resume"):
            response = get_gemini_response(profile_summary_prompt(resume_text))
            st.subheader("🧾 Profile Summary")
            st.write(response)

        if st.button("How Can I Improvise my Skills"):
            response = get_gemini_response(improvise_prompt(resume_text))
            st.subheader("🔧 Skill Improvement Suggestions")
            st.write(response)

    with col2:
        if st.button("What are the Keywords That are Missing"):
            response = get_gemini_response(missing_keywords_prompt(resume_text, jd))
            st.subheader("❌ Missing Keywords")
            st.write(response)

        if st.button("Percentage match"):
            response = get_gemini_response(generate_prompt(resume_text, jd))
            st.subheader("✅ ATS Match Result")
            st.write(response)
