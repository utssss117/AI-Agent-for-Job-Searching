import json
import os
from supabase_client import get_supabase_client
from embedding_engine import EmbeddingEngine

def load_jobs_to_supabase(json_file_path: str):
    """
    Reads jobs from JSON, generates embeddings, and inserts them into Supabase.
    """
    supabase = get_supabase_client()
    engine = EmbeddingEngine()

    try:
        with open(json_file_path, "r") as f:
            jobs = json.load(f)

        print(f"Loading {len(jobs)} jobs into Supabase...")

        for job in jobs:
            # Combine title and description for a richer embedding context
            rich_text = f"{job['title']} - {job['description']}"
            embedding = engine.generate_embedding(rich_text)
            
            data = {
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "description": job["description"],
                "required_skills": job["required_skills"],
                "experience_required": job["experience_required"],
                "embedding": embedding
            }

            response = supabase.table("jobs").insert(data).execute()
            print(f"Inserted: {job['title']} at {job['company']}")

        print("Finished loading all jobs.")

    except Exception as e:
        print(f"Error during job loading: {e}")

if __name__ == "__main__":
    sample_data_path = "sample_jobs.json"
    if os.path.exists(sample_data_path):
        load_jobs_to_supabase(sample_data_path)
    else:
        print(f"Error: {sample_data_path} not found.")
