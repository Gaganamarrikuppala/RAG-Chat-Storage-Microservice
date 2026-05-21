from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Chat Storage Service"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "local"
    API_PREFIX: str = "/api/v1"

    DATABASE_URL: str = Field(default="postgresql+psycopg2://rag_user:rag_password@postgres:5432/rag_chat")
    API_KEY: str = Field(default="change-me")
    API_KEY_HEADER_NAME: str = "X-API-Key"

    RATE_LIMIT_DEFAULT: str = "100/minute"
    RATE_LIMIT_WRITE: str = "30/minute"

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    AUTO_CREATE_TABLES: bool = True
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
