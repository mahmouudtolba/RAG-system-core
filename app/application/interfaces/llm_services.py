from abc import ABC , abstractmethod
from typing import List
from app.domain.entities.chat_message import ChatMessage

class ILLMService(ABC):
    """
    Interface Segrefation Principle
    - small , focused interface
    - client depend only on methods they use
    """

    @abstractmethod
    async def generate_response(
        self ,
        messages: List[ChatMessage]
    ) -> str:
        """Generate response based on context"""
        pass


    @abstractmethod
    async def generate_streaming_response(
        self , messages:List[ChatMessage],
        context:str
    ):
        """Stream response"""
        pass
    