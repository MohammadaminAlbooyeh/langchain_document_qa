from pydantic_settings import BaseSettings


class LangChainConfig(BaseSettings):
    verbose: bool = False
    tracing: bool = False
    max_retries: int = 3
    request_timeout: int = 60

    class Config:
        env_prefix = "LANGCHAIN_"
        extra = "ignore"
