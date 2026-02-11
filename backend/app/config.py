"""
Application Configuration
Reads settings from .env file
"""

from typing import List, Union
import json

from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """All application settings"""

    # ======================
    # Database
    # ======================
    DATABASE_URL: str

    # ======================
    # Security
    # ======================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    # ======================
    # API Keys
    # ======================
    OPENWEATHER_API_KEY: str = ""
    AGMARKNET_API_KEY: str = ""

    # ======================
    # Application
    # ======================
    APP_NAME: str = "Krishi-Net API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # ======================
    # CORS
    # ======================
    # Accepts:
    # - JSON list: ["http://localhost:3000"]
    # - Comma string: http://localhost:3000,http://localhost:8081
    CORS_ORIGINS: Union[List[str], str] = []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None or v == "":
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Try JSON list first
            try:
                return json.loads(v)
            except Exception:
                # Fallback: comma-separated string
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # ======================
    # File Upload
    # ======================
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB
    UPLOAD_DIR: str = "uploads"

    # ======================
    # ML Models
    # ======================
    DISEASE_MODEL_PATH: str = "../ai-models/trained_models/disease_model.h5"
    PRICE_MODEL_PATH: str = "../ai-models/trained_models/price_model.h5"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

