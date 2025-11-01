from dataclasses import dataclass , field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

class MessageRole(str , Enum):
    """Message role enumeration"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT= "assistant"


@dataclass
class ChatMessage:
    """
    Domain Entity for Chat Messages  
    Represent a single message in a conversation
    """
    role:MessageRole
    content:str
    id:str=field(default_factory=lambda:str(uuid4()))
    created_at:datetime=field(default_factory=datetime.utcnow)
    metadata:Optional[dict]=field(default_factory=dict)

    def __post_init__(self):
        """Validate message after initialization"""
        if not self.content.strip():
            raise ValueError("Message content connot be empty")
        
        if isinstance(self.role , str):
            self.role = MessageRole.USER

    def is_from_user(self) -> bool:
        """Check if message is from user"""
        return self.role == MessageRole.USER
    
    def is_from_assistant(self) -> bool:
        """Check if message is from assistant"""
        return self.role == MessageRole.ASSISTANT
    
    def truncate(self, max_length: int) -> str:
        """Truncate content to max length"""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."
