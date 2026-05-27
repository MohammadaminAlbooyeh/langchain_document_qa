from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    cohere_api_key: str = ""
    default_llm: str = "openai"
    chat_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    temperature: float = 0.0
    max_tokens: int = 4096

    class Config:
        env_file = ".env"
        extra = "ignore"
