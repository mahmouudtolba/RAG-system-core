# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application Settings
    All configuration loaded from environment variables
    """
    
    # ==================== Application Settings ====================
    APP_NAME: str = "RAG Chatbot API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # ==================== API Settings ====================
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # ==================== Security Settings ====================
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ==================== Database Settings ====================
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/rag_db"
    DB_ECHO: bool = False  # Set to True to see SQL queries in logs
    
    # ==================== Redis Settings ====================
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    
    # ==================== LLM Provider Settings ====================
    LLM_PROVIDER: str = "openai"  # openai, anthropic, local
    
    # OpenAI Settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Anthropic Settings
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    ANTHROPIC_MAX_TOKENS: int = 2000
    
    # ==================== Embedding Settings ====================
    EMBEDDING_PROVIDER: str = "openai"  # openai, cohere, local
    
    # OpenAI Embeddings
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Cohere Embeddings
    COHERE_API_KEY: str = ""
    COHERE_EMBEDDING_MODEL: str = "embed-english-v3.0"
    
    # Local Embeddings
    LOCAL_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # ==================== Vector Store Settings ====================
    VECTOR_STORE_PROVIDER: str = "pinecone"  # pinecone, weaviate, qdrant
    
    # Pinecone Settings
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "documents"
    
    # Weaviate Settings
    WEAVIATE_URL: str = "http://localhost:8080"
    WEAVIATE_API_KEY: Optional[str] = None
    
    # Qdrant Settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "documents"
    
    # ==================== Storage Settings ====================
    STORAGE_PROVIDER: str = "local"  # s3, gcs, azure, local
    
    # AWS S3 Settings
    S3_BUCKET_NAME: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    
    # Local Storage Settings
    LOCAL_STORAGE_PATH: str = "./storage"
    
    # ==================== Document Processing Settings ====================
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_FILE_EXTENSIONS: list = ["pdf", "docx", "txt", "md"]
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # ==================== Rate Limiting Settings ====================
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # ==================== CORS Settings ====================
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # ==================== Logging Settings ====================
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT: str = "json"  # json or text
    
    # ==================== Monitoring Settings ====================
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # ==================== Worker Settings ====================
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    # ==================== Computed Properties ====================
    @property
    def database_url_sync(self) -> str:
        """Get synchronous database URL (for Alembic migrations)"""
        return self.DATABASE_URL.replace("+asyncpg", "")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Uses lru_cache to avoid re-reading .env file on every call
    """
    return Settings()


# For convenience
settings = get_settings()