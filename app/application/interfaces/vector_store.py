from abc import ABC, abstractmethod
from typing import List, Dict
from app.domain.entities.embedding import Embedding

class IvectorStore(ABC):
    """Interface for vector database operations - Embeddings (array of floats)"""
    @abstractmethod
    async def upsert(
        self,
        id:str,
        embedding:Embedding,
        metadata:Dict
    ) ->None:
        pass

    @abstractmethod
    async def search(
        self , query_embedding:Embedding,
        top_k:int = 5,
        filter:Dict={}
    ) -> List[Dict]:
        pass

    @abstractmethod
    async def delete(self , id:str) -> None:
        pass