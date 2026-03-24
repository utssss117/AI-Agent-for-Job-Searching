import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    """
    Initializes and returns the Supabase client using environment variables.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    # Fallback for Streamlit Cloud Secrets
    if not url or not key:
        try:
            import streamlit as st
            url = st.secrets.get("SUPABASE_URL")
            key = st.secrets.get("SUPABASE_KEY")
        except:
            pass

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY are missing. "
            "Local: Add them to your .env file. "
            "Streamlit Cloud: Add them to 'Secrets' in the app settings."
        )
    
    if "your_supabase" in url or "your_supabase" in key:
        raise ValueError(
            "Supabase credentials are still set to placeholders in .env! "
            "Please replace 'your_supabase_url_here' and 'your_supabase_anon_key_here' "
            "with your actual credentials from the Supabase dashboard."
        )
    
    return create_client(url, key)
