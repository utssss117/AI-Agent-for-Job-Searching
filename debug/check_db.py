from core.supabase_client import get_supabase_client

def check_db():
    try:
        supabase = get_supabase_client()
        response = supabase.table("jobs").select("id", count="exact").execute()
        count = response.count
        print(f"Total jobs in database: {count}")
        
        # Also check if any job has embeddings
        if count > 0:
            first_job = supabase.table("jobs").select("title, embedding").limit(1).execute()
            emb = first_job.data[0].get("embedding")
            if emb:
                print("Embeddings are present.")
            else:
                print("CRITICAL: Jobs exist but embeddings are MISSING.")
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_db()
