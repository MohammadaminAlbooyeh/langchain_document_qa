from pydantic_settings import BaseSettings
import os
from typing import Optional



class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///{os.path.abspath('./data/dev.db')}"
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    LISTINGS_API_URL: Optional[str] = None
    LISTINGS_API_TOKEN: Optional[str] = None
    LISTINGS_API_TIMEOUT_SECONDS: int = 20
    LISTINGS_API_SOURCE_NAME: str = "partner-api"

    # Apify (community/managed scrapers)
    APIFY_TOKEN: Optional[str] = None
    APIFY_IMMOBILIARE_ACTOR_ID: Optional[str] = None
    APIFY_IDEALISTA_ACTOR_ID: Optional[str] = None

    # Proxy and anti-captcha
    PROXY_URL: Optional[str] = None
    ANTICAPTCHA_API_KEY: Optional[str] = None

    # Add missing attributes for PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "house_finder"

    class Config:
        env_file = ".env"


settings = Settings()
# Force SQLite for local development
settings.DATABASE_URL = f"sqlite:///{os.path.abspath('./data/dev.db')}"
