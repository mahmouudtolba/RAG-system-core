from typing import List , Dict
from app.application.interfaces.llm_services import ILLMService
from app.application.interfaces.embedding_service import IEmbeddingService
from app.application.interfaces.vector_store import IvectorStore
from app.domain.entities.chat_message import ChatMessage , MessageRole


class ChatService:
    """
    RAG Pipeline Business Logic
    Orchestrates multiple services
    """
    def __init__(
        self , 
        llm_service : ILLMService,
        embedding_service : IEmbeddingService,
        vector_store : IvectorStore):
        self.llm_serve = llm_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store


    async def ask_question(self, question:str , user_id:str,
                conversation_history: List[ChatMessage] = []) ->str:
        """
        RAG Pipeline:
        1. Create question embedding
        2. Search vector store
        3. Build context
        4. Generate reponse with LLM
        """
        # 1. Embed the question
        question_embeddings = await self.embedding_service.create_embedding(question)

        # 2. search vector store
        search_results = await self.vector_store.search(query_embedding=question_embeddings,
                                                        top_k=5,
                                                        filter={"user_id":user_id})
        # 3. build context form results
        context = self._build_context(search_results)


        # 4. prepare messages
        messages = conversation_history or []
        messages.append(ChatMessage(role=MessageRole.USER , content=question))

        # 5. Generate response
        response = await self.llm_serve.generate_response(messages)

        return response


    def _build_context(self , search_results:List[Dict]) -> str:
        """Build context from search results"""
        context_parts = []
        for result in search_results:
            context_parts.append(result['metadata']['text'])
        return "\n\n".join(context_parts)

