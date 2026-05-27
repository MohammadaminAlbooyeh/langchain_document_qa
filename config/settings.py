from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LangChain Document QA"
    debug: bool = False
    log_level: str = "INFO"
    max_upload_size_mb: int = 100

    openai_api_key: str = ""
    anthropic_api_key: str = ""

    database_url: str = "sqlite+aiosqlite:///./data/langchain_qa.db"
    vector_store_type: str = "chroma"
    default_llm: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    class Config:
        env_file = ".env"
        extra = "ignore"
