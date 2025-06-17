import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Resume Critiquer", page_icon="🤖", layout="centered")

st.title("AI Resume Critiquer 🤖")
st.markdown("Upload your resume in PDF format and get AI feedback on how to improve it.")

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
job_role = st.text_input("Enter the job role you are applying for (optional)", placeholder="e.g., Software Engineer")

analyze_button = st.button("Analyze Resume")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze_button and uploaded_file:
    st.write("Analyzing your resume... Please wait.")
    if not OPENAI_API_KEY:
        st.error("OpenAI API key is not set. Please set it in the .env file.")
    else:
        try:
            file_content = extract_text_from_file(uploaded_file)

            if not file_content.strip():
                st.error("The uploaded file is empty or could not be read. Please upload a valid PDF file.")
                st.stop()
            
            prompt = f"""Please analyze this resume and provide constructive feedback. 
            Focus on the following aspects:
            1. Content clarity and impact
            2. Skills presentation
            3. Experience descriptions
            4. Specific improvements for {job_role if job_role else 'general job applications'}
            
            Resume content:
            {file_content}
            
            Please provide your analysis in a clear, structured format with specific recommendations."""

            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are an expert resume reviewer with years of experience in hiring."},
                          {"role": "user", "content": prompt}],
                          temperature=0.5,
                          max_tokens=1500)
            st.markdown("### AI Feedback:")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred while processing your resume: {e}")
else:
    st.info("Please upload your resume and click 'Analyze Resume' to get feedback.")
