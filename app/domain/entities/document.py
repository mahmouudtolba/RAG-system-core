from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Document:
    """
    Domain Entity - Pure business object
    No framework dependencies!
    """
    id:str
    filename:str
    content:str
    created_at:datetime
    user_id:str
    chunks: List[str]= []
    
    def split_into_chunks(self, chunk_size : int = 1000) -> list[str]:
        words = self.content.split()
        chunks = []
        current_chunk = []
        current_size = 0
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1

            if current_size >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        self.chunks = chunks
        return chunks

