import re

def calculate_keyword_score(resume_text, job_description):
    """30% Weight: Keyword overlap analysis."""
    if not job_description or not resume_text:
        return 0.0
    
    # Extract important words from job description (length > 3)
    job_words = set(re.findall(r'\w{4,}', job_description.lower()))
    resume_text_lower = resume_text.lower()
    
    if not job_words:
        return 0.0
        
    matches = sum(1 for word in job_words if word in resume_text_lower)
    score = (matches / len(job_words)) * 100
    return min(score, 100.0)

def calculate_skills_score(resume_skills, job_required_skills):
    """25% Weight: Direct skills match."""
    if not job_required_skills:
        return 100.0  # If job lists no skills, resume is a match by default
    if not resume_skills:
        return 0.0
        
    rs_norm = {s.lower().strip() for s in resume_skills if s}
    js_norm = {s.lower().strip() for s in job_required_skills if s}
    
    if not js_norm:
        return 100.0
        
    match_count = len(rs_norm.intersection(js_norm))
    score = (match_count / len(js_norm)) * 100
    return min(score, 100.0)

def calculate_experience_score(resume_years, job_experience_req):
    """15% Weight: Experience relevance."""
    # Convert inputs to float safely
    try:
        ry = float(resume_years) if resume_years is not None else 0.0
    except (ValueError, TypeError):
        ry = 0.0
        
    # Extract number from job_experience_req string (e.g., "5+ years")
    match = re.search(r'(\d+)', str(job_experience_req))
    jy = float(match.group(1)) if match else 0.0
    
    if jy == 0:
        return 100.0
        
    if ry >= jy:
        return 100.0
    
    return (ry / jy) * 100

def calculate_structure_score(resume_text):
    """15% Weight: Standard resume sections detection."""
    sections = ['summary', 'skills', 'experience', 'projects', 'education']
    resume_lower = resume_text.lower()
    
    found_count = sum(1 for section in sections if section in resume_lower)
    return (found_count / len(sections)) * 100

def calculate_impact_score(resume_text):
    """15% Weight: Detection of numbers and percentages (quantifiable results)."""
    # Regex for percentages or multi-digit numbers
    impact_patterns = [
        r'\d+%',        # Percentages
        r'\$\d+',       # Monetary values
        r'\d{2,}',      # Multi-digit numbers
        r'increased',   # Action verbs indicating impact
        r'decreased',
        r'improved',
        r'delivered'
    ]
    
    score = 0
    for pattern in impact_patterns:
        if re.search(pattern, resume_text.lower()):
            score += (100 / len(impact_patterns))
            
    return min(score, 100.0)

def get_ats_score(resume_data, resume_text, job_data):
    """
    Orchestrates the ATS scoring and provides improvement suggestions.
    """
    keyword = calculate_keyword_score(resume_text, job_data.get('description', ''))
    skills = calculate_skills_score(resume_data.get('skills', []), job_data.get('required_skills', []))
    experience = calculate_experience_score(resume_data.get('experience_years', 0), job_data.get('experience_required', '0'))
    structure = calculate_structure_score(resume_text)
    impact = calculate_impact_score(resume_text)
    
    # Calculate weighted overall score
    overall = (
        (keyword * 0.30) + 
        (skills * 0.25) + 
        (experience * 0.15) + 
        (structure * 0.15) + 
        (impact * 0.15)
    )
    
    suggestions = []
    if keyword < 60:
        suggestions.append("Incorporate more keywords from the job description into your resume.")
    if skills < 70:
        suggestions.append("Highlight specific missing technical skills: " + ", ".join(set(job_data.get('required_skills', [])) - set(resume_data.get('skills', []))))
    if structure < 80:
        suggestions.append("Ensure your resume has clearly labeled sections: Summary, Skills, Experience, Projects, and Education.")
    if impact < 50:
        suggestions.append("Quantify your achievements using numbers, percentages, or monetary values (e.g., 'Increased revenue by 20%').")
    if experience < 80:
        suggestions.append("Clarify your total years of experience if they align with the job requirements.")

    return {
        "overall_ats_score": round(overall, 2),
        "keyword_score": round(keyword, 2),
        "skills_score": round(skills, 2),
        "experience_score": round(experience, 2),
        "structure_score": round(structure, 2),
        "impact_score": round(impact, 2),
        "improvement_suggestions": suggestions
    }
