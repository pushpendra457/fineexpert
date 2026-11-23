"""Application Settings and Environment Configuration.

Uses Pydantic BaseSettings to parse and validate all environment variables,
deriving async database connections, parsing CORS configurations, and
enforcing production security constraints.
"""

from functools import lru_cache
from typing import List, Literal, Optional, Union
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration schema."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Core Application Configuration
    PROJECT_NAME: str = "Homingo API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "staging", "production", "testing"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Security & JWT Credentials
    SECRET_KEY: str = Field(
        default="insecure-default-secret-key-replace-in-production-environment-immediately-32b",
        description="JWT cryptographic signing secret key",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/homingo",
        description="Synchronous PostgreSQL connection URL",
    )
    ASYNC_DATABASE_URL: Optional[str] = Field(
        default=None,
        description="Asynchronous PostgreSQL connection URL (asyncpg)",
    )

    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    # Google OAuth 2.0
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = "http://localhost:8000/api/v1/auth/google/callback"

    # AI Model Providers & Embeddings
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    # Cloudinary Cloud Storage
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None

    # Vector Store (Qdrant)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "homingo_docs"

    # Monitoring & Observability
    SENTRY_DSN: Optional[str] = None

    # CORS Configuration
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> List[str]:
        """Convert comma-separated origin strings into a clean list of origins."""
        if isinstance(value, str):
            if not value.strip():
                return []
            if value.startswith("[") and value.endswith("]"):
                import json

                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except Exception:
                    pass
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        elif isinstance(value, list):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        return []

    @model_validator(mode="after")
    def validate_and_compute_urls(self) -> "Settings":
        """Compute ASYNC_DATABASE_URL, Celery URLs and enforce production security constraints."""
        # Derive ASYNC_DATABASE_URL if not explicitly supplied
        if not self.ASYNC_DATABASE_URL:
            db_url = self.DATABASE_URL
            if db_url.startswith("postgresql://"):
                self.ASYNC_DATABASE_URL = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif db_url.startswith("postgresql+psycopg2://"):
                self.ASYNC_DATABASE_URL = db_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
            else:
                self.ASYNC_DATABASE_URL = db_url

        # Celery defaults
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = self.REDIS_URL
        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = self.REDIS_URL

        # Production safety checks
        if self.ENVIRONMENT == "production":
            if "insecure" in self.SECRET_KEY.lower() or len(self.SECRET_KEY) < 32:
                raise ValueError("In production, SECRET_KEY must be a cryptographically secure string with at least 32 characters.")

        return self

    @property
    def is_development(self) -> bool:
        """Helper to check if current environment is development."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Helper to check if current environment is production."""
        return self.ENVIRONMENT == "production"

    @property
    def is_testing(self) -> bool:
        """Helper to check if current environment is testing."""
        return self.ENVIRONMENT == "testing"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton provider."""
    return Settings()


settings: Settings = get_settings()
