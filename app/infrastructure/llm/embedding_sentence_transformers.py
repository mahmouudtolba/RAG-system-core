from typing import List
from sentence_transformers import SentenceTransformer
from app.application.interfaces.embedding_service import IEmbeddingService
from app.domain.entities.embedding import Embedding


class SentenceTransformerEmbeddingService(IEmbeddingService):
    """
    Local embedding service using sentence-transformers
    Free, runs on your hardware, no API costs!
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Popular models:
        - all-MiniLM-L6-v2: Fast, 384 dimensions
        - all-mpnet-base-v2: Better quality, 768 dimensions
        - multi-qa-mpnet-base-dot-v1: Good for Q&A
        """
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    async def create_embedding(self, text: str) -> Embedding:
        """Create embedding for a single text"""
        vector = self.model.encode(text , convert_to_numpy = True)

        return Embedding(
            vector=vector.tolist(),
            model=self.model_name,
            text=text
        )
    
    async def create_embeddings_batch(self, texts: List[str]) -> List[Embedding]:
        """Create embeddings for multiple texts"""
        # Batch encoding is more efficient
        vectors = self.model.encode(texts, convert_to_numpy=True)
        
        return [
            Embedding(
                vector=vector.tolist(),
                model=self.model_name,
                text=texts[i]
            )
            for i, vector in enumerate(vectors)
        ]