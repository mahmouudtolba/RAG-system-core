from dataclasses import dataclass
from typing import List

@dataclass
class Embedding:
    vector: List[float]
    model:str
    text:str

    def __post_init__(self):
        object.__setattr__(self, 'vector', tuple(self.vector))
