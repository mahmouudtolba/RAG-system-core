from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.embedding import Embedding


class IEmbeddingService(ABC):
    @abstractmethod
    async def create_embedding(self , text:str) -> Embedding:
        pass

    @abstractmethod 
    async def create_embeddings_batch(
        self,
        texts:List[str],
    ) -> List[Embedding]:
        pass
    