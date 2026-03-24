from core.supabase_client import get_supabase_client
from core.embedding_engine import EmbeddingEngine

def get_top_jobs(resume_text: str, threshold: float = 0.0, top_k: int = 5):
    """
    Searches for the top-k matching jobs in Supabase using vector similarity.
    """
    try:
        supabase = get_supabase_client()
        engine = EmbeddingEngine()
        
        # Generate embedding for the resume
        resume_embedding = engine.generate_embedding(resume_text)
        
        # Call the Supabase RPC function for similarity search
        response = supabase.rpc(
            "match_jobs",
            {
                "query_embedding": resume_embedding,
                "match_threshold": threshold,
                "match_count": top_k
            }
        ).execute()
        
        return response.data
    except Exception as e:
        print(f"Error matching jobs: {e}")
        return []

if __name__ == "__main__":
    # Test with sample text
    test_resume = "I am a Senior React developer with TypeScript experience."
    matches = get_top_jobs(test_resume)
    for match in matches:
        print(f"Title: {match['title']} | Score: {match['similarity']:.4f}")
