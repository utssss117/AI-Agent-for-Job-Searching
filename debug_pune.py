import os
import requests
import json
from dotenv import load_dotenv
from supabase_client import get_supabase_client
from live_job_fetcher import LiveJobFetcher

load_dotenv()

def diagnostic():
    print("--- Diagnostic Start ---")
    
    # 1. Check API directly
    app_id = os.getenv('ADZUNA_APP_ID')
    app_key = os.getenv('ADZUNA_APP_KEY')
    url = 'https://api.adzuna.com/v1/api/jobs/in/search/1'
    params = {
        'app_id': app_id, 
        'app_key': app_key, 
        'what': 'Python Developer', 
        'where': 'pune', 
        'results_per_page': 5
    }
    
    print(f"Testing Adzuna IN endpoint for 'Python Developer' in 'pune'...")
    try:
        res = requests.get(url, params=params)
        print(f"API HTTP Status: {res.status_code}")
        data = res.json()
        results = data.get("results", [])
        print(f"API found {len(results)} jobs.")
        for j in results:
            print(f" - {j['title']} @ {j['location'].get('display_name')}")
    except Exception as e:
        print(f"API Error: {e}")

    # 2. Test LiveJobFetcher class
    print("\nTesting LiveJobFetcher.fetch_live_jobs...")
    fetcher = LiveJobFetcher()
    fetched = fetcher.fetch_live_jobs("Python Developer", "pune", country="India", results=5)
    print(f"Fetcher returned {len(fetched)} jobs.")

    # 3. Check DB
    print("\nChecking Supabase 'jobs' table...")
    try:
        supabase = get_supabase_client()
        res = supabase.table("jobs").select("id, title, location").execute()
        print(f"Total jobs in DB: {len(res.data)}")
        # Check for Pune jobs
        pune_jobs = [j for j in res.data if 'Pune' in str(j.get('location', '')) or 'pune' in str(j.get('location', ''))]
        print(f"Pune jobs in DB: {len(pune_jobs)}")
    except Exception as e:
        print(f"DB Error: {e}")
        
    print("--- Diagnostic End ---")

if __name__ == "__main__":
    diagnostic()
