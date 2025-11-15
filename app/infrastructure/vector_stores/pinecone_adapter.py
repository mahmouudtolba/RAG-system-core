# app/infrastructure/vector_stores/pinecone_adapter.py
from typing import List, Dict
from pinecone import Pinecone, ServerlessSpec
from app.application.interfaces.vector_store import IVectorStore
from app.domain.entities.embedding import Embedding

class PineconeAdapter(IVectorStore):
    """Pinecone implementation"""
    
    def __init__(self, api_key: str, index_name: str):
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        self.index = self.pc.Index(index_name)
    
    async def upsert(
        self,
        id: str,
        embedding: Embedding,
        metadata: Dict
    ) -> None:
        """Pinecone-specific upsert"""
        self.index.upsert(vectors=[{
            "id": id,
            "values": list(embedding.vector),
            "metadata": metadata
        }])
    
    async def search(
        self,
        query_embedding: Embedding,
        top_k: int = 5,
        filter: Dict = None
    ) -> List[Dict]:
        """Pinecone-specific search"""
        results = self.index.query(
            vector=list(query_embedding.vector),
            top_k=top_k,
            include_metadata=True,
            filter=filter
        )
        
        return [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in results.matches
        ]
    
    async def delete(self, id: str) -> None:
        """Delete vector"""
        self.index.delete(ids=[id])