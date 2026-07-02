from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LangChain Document QA"
    debug: bool = True
    log_level: str = "INFO"
    max_upload_size: int = 100

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    cohere_api_key: str = ""

    pinecone_api_key: str = ""
    pinecone_environment: str = "us-west1-gcp"
    pinecone_index_name: str = "langchain-docs"

    database_url: str = "sqlite+aiosqlite:///./data/langchain_qa.db"

    default_llm: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 4096

    vector_store_type: str = "chroma"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    chroma_db_path: str = "./chroma_db"
    api_key_prefix: str = "lq-"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
