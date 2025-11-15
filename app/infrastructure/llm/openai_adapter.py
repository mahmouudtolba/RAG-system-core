from typing import Any, List
import openai
from app.application.interfaces.llm_services import ILLMService
from app.domain.entities.chat_message import ChatMessage


class OpenAIAdapter(ILLMService):
    def __init__(self, api_key :str , model:str="gpt-4-mini"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

    def generate_response(self, messages: List[ChatMessage] , context:str):
        system_message = {
            "role":"system",
            "content": f"Answer questions based on the following context:\n\n{context}"
        }
        formatted_messages = [system_message] + [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages
        )
        
        return response.choices[0].message.content
    
    async def generate_streaming_response(
        self,
        messages: List[ChatMessage],
        context: str
    ):
        """Streaming implementation"""
        system_message = {
            "role": "system",
            "content": f"Answer questions based on the following context:\n\n{context}"
        }
        
        formatted_messages = [system_message] + [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        stream = await self.client.chat.completions.create(model=self.model,
            messages=formatted_messages,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
