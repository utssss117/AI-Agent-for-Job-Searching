from matching_engine import analyze_job_matches

def check_engine():
    resume_data = {"skills": ["Python"]}
    resume_text = "I am a Python developer. That is all."
    
    print("Testing analyze_job_matches with threshold -1.0...")
    results = analyze_job_matches(resume_data, resume_text)
    
    print(f"Total jobs returned: {len(results)}")
    if results:
        print(f"Top match: {results[0]['job_title']} at {results[0]['company']} (Score: {results[0]['match_percentage']})")
    else:
        print("Still returning 0 jobs.")

if __name__ == "__main__":
    check_engine()
