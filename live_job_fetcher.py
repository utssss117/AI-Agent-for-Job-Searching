import os
import requests
import re
from supabase_client import get_supabase_client
from embedding_engine import EmbeddingEngine
from utils import clean_text
from dotenv import load_dotenv

load_dotenv()

class LiveJobFetcher:
    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")
        
        # Fallback for Streamlit Cloud
        if not self.app_id or not self.app_key:
            try:
                import streamlit as st
                self.app_id = self.app_id or st.secrets.get("ADZUNA_APP_ID")
                self.app_key = self.app_key or st.secrets.get("ADZUNA_APP_KEY")
            except:
                pass
        self.supabase = get_supabase_client()
        self.engine = EmbeddingEngine()
        
        # Adzuna supported country codes
        self.country_map = {
            "United Kingdom": "gb",
            "India": "in",
            "United States": "us",
            "Canada": "ca",
            "Germany": "de",
            "France": "fr",
            "Australia": "au",
            "United Arab Emirates": "ae"
        }

    def _strip_html(self, text):
        """Removes HTML tags from a string."""
        if not text:
            return ""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def fetch_live_jobs(self, query: str, location: str, country: str = "United Kingdom", results=10):
        """
        Fetches live jobs from Adzuna API, cleans them, and stores them in Supabase.
        """
        if not self.app_id or not self.app_key:
            print("Error: ADZUNA_APP_ID or ADZUNA_APP_KEY not set.")
            return []

        country_code = self.country_map.get(country, "gb")
        base_url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"

        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": query,
            "where": location,
            "results_per_page": results,
            "content-type": "application/json"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            jobs = data.get("results", [])
            processed_jobs = []

            for job in jobs:
                # Extract and clean data
                raw_description = job.get("description", "")
                clean_description = clean_text(self._strip_html(raw_description))
                
                job_data = {
                    "title": job.get("title", "N/A"),
                    "company": job.get("company", {}).get("display_name", "N/A"),
                    "location": job.get("location", {}).get("display_name", "N/A"),
                    "description": clean_description,
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "experience_required": "Not specified" # Adzuna doesn't always provide this clearly
                }

                # Generate embedding for storage and matching
                # We combine title and description for a better semantic representation
                embedding_text = f"{job_data['title']} {job_data['description']}"
                embedding = self.engine.generate_embedding(embedding_text)

                # Store temporarily in Supabase
                # Note: We use upsert if we had a clear unique ID, but here we just insert
                try:
                    self.supabase.table("jobs").upsert({
                        "title": job_data["title"],
                        "company": job_data["company"],
                        "location": job_data["location"],
                        "description": job_data["description"],
                        "experience_required": job_data["experience_required"],
                        "embedding": embedding
                    }, on_conflict="title, company").execute() # Simple conflict resolution
                except Exception as db_err:
                    print(f"Database insertion error: {db_err}")

                processed_jobs.append(job_data)

            return processed_jobs

        except requests.exceptions.RequestException as e:
            print(f"Adzuna API Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

if __name__ == "__main__":
    # Quick test
    fetcher = LiveJobFetcher()
    test_jobs = fetcher.fetch_live_jobs("Python Developer", "London", results=2)
    for j in test_jobs:
        print(f"Fetched: {j['title']} @ {j['company']}")
