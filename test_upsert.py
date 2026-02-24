from supabase_client import get_supabase_client

def test_upsert():
    supabase = get_supabase_client()
    # Try a simple upsert to see if it works or gives a specific error
    job_data = {
        "title": "Test Job",
        "company": "Test Company",
        "description": "Test"
    }
    
    print("Testing upsert with on_conflict='title, company'...")
    try:
        res = supabase.table("jobs").upsert(job_data, on_conflict="title, company").execute()
        print("Upsert successful!")
    except Exception as e:
        print(f"Upsert failed: {e}")

if __name__ == "__main__":
    test_upsert()
