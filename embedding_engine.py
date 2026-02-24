from sentence_transformers import SentenceTransformer

class EmbeddingEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
    
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> list:
        if not text:
            return []
        
        # Generate embedding as numpy array
        embedding = self.model.encode(text)
        
        # Convert to list for database storage
        return embedding.tolist()
