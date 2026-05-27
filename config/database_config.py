from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    url: str = "sqlite+aiosqlite:///./data/langchain_qa.db"
    pool_size: int = 5
    max_overflow: int = 10
    echo: bool = False

    class Config:
        env_prefix = "DB_"
        extra = "ignore"
