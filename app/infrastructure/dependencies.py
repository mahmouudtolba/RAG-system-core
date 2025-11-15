# app/infrastructure/dependencies.py
from functools import lru_cache
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.infrastructure.database.session import get_db_session

# Adapters
from app.infrastructure.llm.openai_adapter import OpenAIAdapter
from app.infrastructure.llm.embedding_sentence_transformers import SentenceTransformerEmbeddingService
from app.infrastructure.vector_stores.pinecone_adapter import PineconeAdapter

# Services
from app.application.services.document_service import DocumentService
from app.application.services.chat_service import ChatService

# Interfaces
from app.application.interfaces.llm_services import ILLMService
from app.application.interfaces.embedding_service import IEmbeddingService
from app.application.interfaces.vector_store import IvectorStore
from app.application.interfaces.storage_service import IStorageService
from app.application.interfaces.document_repository import IDocumentRepositroy


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# --- Infrastructure Providers ---

def get_llm_service(settings:Settings = Depends(get_settings)) -> ILLMService:
    """
    Factory pattern + Dependency Injection
    Easy to switch between providers based on config
    """
    if settings.LLM_PROVIDER == "openai":
        return OpenAIAdapter(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL)
        
    else:
        raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")


def get_embedding_service(
    settings: Settings = Depends(get_settings)
) -> IEmbeddingService:
    return OpenAIEmbeddingService(
        api_key=settings.OPENAI_API_KEY,
        model="text-embedding-3-small"
    )


def get_vector_store(
    settings: Settings = Depends(get_settings)
) -> IvectorStore:
    return PineconeAdapter(
        api_key=settings.PINECONE_API_KEY,
        index_name=settings.PINECONE_INDEX_NAME
    )



def get_document_repository(
    session: AsyncSession = Depends(get_db_session)
) -> IDocumentRepositroy:
    return DocumentRepository(session)


# --- Application Service Providers ---

def get_document_service(
    document_repo: IDocumentRepository = Depends(get_document_repository),
    embedding_service: IEmbeddingService = Depends(get_embedding_service),
    vector_store: IVectorStore = Depends(get_vector_store),
    storage_service: IStorageService = Depends(get_storage_service)
) -> DocumentService:
    """
    All dependencies injected automatically!
    No manual wiring needed
    """
    return DocumentService(
        document_repo=document_repo,
        embedding_service=embedding_service,
        vector_store=vector_store,
        storage_service=storage_service
    )


def get_chat_service(
    llm_service: ILLMService = Depends(get_llm_service),
    embedding_service: IEmbeddingService = Depends(get_embedding_service),
    vector_store: IVectorStore = Depends(get_vector_store)
) -> ChatService:
    return ChatService(
        llm_service=llm_service,
        embedding_service=embedding_service,
        vector_store=vector_store
    )