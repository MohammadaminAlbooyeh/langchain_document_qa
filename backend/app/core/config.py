from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///{os.path.abspath('./data/dev.db')}"
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Add missing attributes for PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "house_finder"

    class Config:
        env_file = ".env"


settings = Settings()
# Force SQLite for local development
settings.DATABASE_URL = f"sqlite:///{os.path.abspath('./data/dev.db')}"
