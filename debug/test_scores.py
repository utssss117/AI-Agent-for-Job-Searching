from engines.job_matcher import get_top_jobs

def check_scores():
    test_resume = "Python Developer with Machine Learning, React, and AWS experience."
    print("Fetching jobs with threshold 0.0 to see raw scores...")
    matches = get_top_jobs(test_resume, threshold=0.0, top_k=20)
    
    if not matches:
        print("No matches returned even at 0.0 threshold. Something is wrong with the DB query.")
        return
        
    print(f"Total jobs evaluated: {len(matches)}")
    for m in matches:
        print(f"Score: {m['similarity']:.4f} | Title: {m['title']} ({m['location']})")

if __name__ == "__main__":
    check_scores()
