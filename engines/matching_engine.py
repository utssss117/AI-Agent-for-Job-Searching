import os
import json
from groq import Groq
from .job_matcher import get_top_jobs
from .ats_engine import get_ats_score
from dotenv import load_dotenv

load_dotenv()

def generate_recommendation_reason(resume_text: str, job_description: str, matched_skills: list, missing_skills: list) -> str:
    """
    Generates a professional recommendation reason using Groq LLM.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "API Key missing. Cannot generate recommendation."

    client = Groq(api_key=api_key)
    
    prompt = f"""
    You are an AI career coach. Analyze the candidate's fit for the following job.
    
    Resume Context: {resume_text[:1500]}
    Job Description: {job_description[:1500]}
    Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}
    Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}

    Provide a professional explanation (3-5 lines) explaining:
    1. Why this job fits the candidate's profile.
    2. Which matched skills are most relevant.
    3. A clear recommendation for improvement or focus.

    Rules:
    - Keep it concise (max 5 lines).
    - Be professional and encouraging.
    - Return ONLY the explanation text. No preamble or labels like '1. Reason:'.
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional recruiting assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Match analysis currently unavailable: {str(e)}"

def analyze_job_matches(resume_data: dict, resume_text: str):
    """
    Analyzes skill gaps, calculates match percentages, and generates LLM-based reasoning for top jobs.
    """
    try:
        top_jobs = get_top_jobs(resume_text, threshold=-1.0, top_k=5)
        if not top_jobs:
            return []

        # Extract and normalize resume skills, filtering out None/empty values
        resume_skills = set(s.lower().strip() for s in resume_data.get("skills", []) if s and isinstance(s, str))
        
        analysis_results = []

        for job in top_jobs:
            job_required_skills = job.get("required_skills") or []
            
            # Normalize job skills and filter out None
            job_skills_norm = [s.lower().strip() for s in job_required_skills if s and isinstance(s, str)]
            
            matched_skills = [s for s in job_required_skills if s and isinstance(s, str) and s.lower().strip() in resume_skills]
            missing_skills = [s for s in job_required_skills if s and isinstance(s, str) and s.lower().strip() not in resume_skills]
            
            # Calculate match percentage
            total_req = len(job_required_skills)
            match_percentage = (len(matched_skills) / total_req) * 100 if total_req > 0 else 0.0

            # Generate LLM reasoning
            recommendation = generate_recommendation_reason(
                resume_text,
                job.get("description", "No description provided."),
                matched_skills,
                missing_skills
            )

            # Generate ATS Score breakdown
            ats_analysis = get_ats_score(resume_data, resume_text, job)

            analysis_results.append({
                "job_title": job.get("title", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("location", "N/A"),
                "match_percentage": round(match_percentage, 2),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "recommendation_reason": recommendation,
                "ats_analysis": ats_analysis
            })

        return analysis_results

    except Exception as e:
        print(f"Error in matching engine: {e}")
        return []
