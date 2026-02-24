import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class CoverLetterGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        # Fallback for Streamlit Cloud
        if not self.api_key:
            try:
                import streamlit as st
                self.api_key = st.secrets.get("GROQ_API_KEY")
            except:
                pass

        if not self.api_key:
            raise ValueError("Groq API key not found. Set it in .env or Streamlit Secrets.")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"

    def generate_cover_letter(self, resume_data: dict, job_data: dict, applicant_name: str = "[Your Name]") -> str:
        """
        Generates a tailored cover letter using the Groq LLM based on resume and job data.
        """
        
        # Extract relevant job details
        job_title = job_data.get("title", "the open position")
        company = job_data.get("company", "your company")
        job_description = job_data.get("description", "Not provided")
        
        # Extract relevant resume details
        skills = ", ".join(resume_data.get("skills", []))
        experience = resume_data.get("experience_years", "some")
        strengths = ", ".join(resume_data.get("strengths", []))
        
        prompt = f"""
        You are an expert career coach and professional copywriter.
        Write a highly tailored, engaging, and professional cover letter.
        
        Applicant Name: {applicant_name}
        Target Role: {job_title}
        Target Company: {company}
        
        Applicant's Background:
        - Experience: {experience} years
        - Top Skills: {skills}
        - Strengths: {strengths}
        
        Job Description Context:
        {job_description[:1000]}...
        
        Instructions:
        1. Write a 3-4 paragraph cover letter.
        2. Hook the reader in the first paragraph.
        3. Connect the applicant's specific skills to the needs mentioned in the job description context.
        4. Keep the tone professional, confident, but not arrogant.
        5. Do not invent any fake experience or metrics not provided in the background.
        6. Return ONLY the text of the cover letter. Do not include any conversational preamble or placeholders other than [Your Contact Information].
        """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert professional cover letter writer."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.7 # Add a bit of creativity for the writing
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating cover letter: {str(e)}"

if __name__ == "__main__":
    # Quick test
    gen = CoverLetterGenerator()
    test_resume = {"skills": ["Python", "Machine Learning"], "experience_years": 3, "strengths": ["Problem Solving"]}
    test_job = {"title": "AI Engineer", "company": "Tech Corp", "description": "Looking for someone to build LLM pipelines"}
    print(gen.generate_cover_letter(test_resume, test_job))
