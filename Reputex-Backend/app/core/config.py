"""Application settings and configuration management via Pydantic v2."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Project metadata
    PROJECT_NAME: str = "RepuTex Backend"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["*"])

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./reputex.db"
    DATABASE_URL_SYNC: str = "sqlite:///./reputex.db"

    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    INGESTION_SCHEDULE_INTERVAL_MINUTES: int = 30

    # Security & JWT
    JWT_SECRET: str = "reputex-super-secret-key-change-in-production-2026-xyz"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRATION_MINUTES: int = 60
    JWT_REFRESH_EXPIRATION_DAYS: int = 30

    # Integration modes: "mock" | "real"
    PLATFORM_MODE: str = "mock"
    AI_PROVIDER: str = "mock"
    AI_API_KEY: str = ""

    # Platform API Credentials
    GOOGLE_PLACES_API_KEY: str = ""
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_USER_AGENT: str = "reputex-app:v1.0"
    TWITTER_BEARER_TOKEN: str = ""

    # Firecrawl Acquisition Settings (Primary for Reddit & X)
    FIRECRAWL_API_KEY: str = ""
    FIRECRAWL_ENABLED: bool = False
    FIRECRAWL_BASE_URL: str = "https://api.firecrawl.dev"
    FIRECRAWL_MAX_RESULTS_PER_QUERY: int = 5
    FIRECRAWL_MAX_PAGES_PER_INGESTION: int = 3


settings = Settings()
