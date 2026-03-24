import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMAnalyzer:
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

    def analyze_resume(self, resume_text: str) -> dict:
        """
        Sends cleaned resume text to Groq and returns structured JSON.
        """
        prompt = f"""
        You are an expert HR and ATS analyzer. Extract information from the following resume text and format it into a valid JSON object.
        
        Rules:
        1. Return ONLY valid JSON. No preamble, no explanation.
        2. If information is missing, use null or an empty list.
        3. Be precise with years of experience.
        4. Structured extraction is mandatory.

        Required JSON Structure:
        {{
            "skills": ["List of overall skills"],
            "programming_languages": ["List of languages"],
            "frameworks": ["List of frameworks"],
            "tools": ["List of tools/software"],
            "experience_years": float,
            "projects": [
                {{
                    "title": "Project Name",
                    "description": "Short summary"
                }}
            ],
            "education": [
                {{
                    "degree": "Degree Name",
                    "institution": "University/School",
                    "year": "Year"
                }}
            ],
            "domain_expertise": ["Areas like FinTech, HealthTech, etc."],
            "strengths": ["Key professional strengths"]
        }}

        Resume Text:
        ---
        {resume_text}
        ---
        """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a specialized JSON extraction assistant."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except json.JSONDecodeError:
            return {"error": "Malformed JSON response from LLM"}
        except Exception as e:
            return {"error": str(e)}
