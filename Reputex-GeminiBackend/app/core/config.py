"""Application configuration loaded from environment variables."""
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    APP_NAME: str = "RepuTex Intelligence Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: List[str] = ["*"]

    # Database (Default to SQLite for local development/tests, easily pointed to PostgreSQL)
    DATABASE_URL: str = "sqlite+aiosqlite:///./reputex.db"
    SYNC_DATABASE_URL: str = "sqlite:///./reputex.db"

    # JWT Security
    SECRET_KEY: str = "reputex_super_secret_jwt_key_change_in_production_32bytes!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Gemini API Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.6-flash"
    GEMINI_ENABLED: bool = True
    GEMINI_TIMEOUT_SECONDS: float = 25.0
    GEMINI_MAX_RETRIES: int = 3

    # Acquisition & Mock Mode
    USE_MOCK_ACQUISITION: bool = True
    USE_MOCK_GEMINI: bool = True

    # Search Grounding Configuration
    MAX_SEARCH_QUERIES_PER_SCAN: int = 4
    SEARCH_CACHE_TTL_HOURS: int = 6

    # Celery & Background Execution (In-process background tasks default)
    USE_CELERY: bool = False
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"


settings = Settings()
