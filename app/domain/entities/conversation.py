from dataclasses import dataclass , field
from datetime import datetime
from typing import List ,Optional
from uuid import uuid4

from app.domain.entities.chat_message import ChatMessage, MessageRole


@dataclass
class Conversation:
    """
    Domain Entity for conversations 
    Represents a chat session with multiple messages
    """

    id :str= field(default_factory=lambda:str(uuid4()))
    user_id :str = ""
    title:str = "New Conversation"
    messages:List[ChatMessage] = field(default_factory=list)
    created_at:datetime = field(default_factory=datetime.utcnow)
    updated_at:datetime=field(default_factory=datetime.utcnow)
    metadata:dict = field(default_factory=dict)
    


    def add_message(self , role:MessageRole , content:str) -> ChatMessage:

        message = ChatMessage(role = role , content=content)
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
        if self.title == "New Conversation" and role == MessageRole.USER:
            self.title = self._generate_title(content)

        return message
    
    def add_user_message(self , content:str) -> ChatMessage:
        return self.add_message(MessageRole.USER,content)
    
    def add_assistant_message(self , content:str) -> ChatMessage:
        return self.add_message(MessageRole.ASSISTANT , content)
    
    def get_message_count(self) -> int:
        """Get total message count"""
        return len(self.messages)
    

    def get_last_user_message(self) -> Optional[ChatMessage]:
        """Get the last message from user"""
        for message in reversed(self.messages):
            if message.is_from_user():
                return message
            
        return None