"""
Core configuration settings for the Home DIY API.
"""
from typing import List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Basic app config
    app_name: str = "Home DIY API"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/home_diy_db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # AI Agents Service
    agents_service_url: str = "http://localhost:8001"
    agents_service_timeout: int = 30
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File uploads
    max_file_size: int = 10485760  # 10MB
    upload_folder: str = "uploads"
    
    # External services
    openai_api_key: Optional[str] = None
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
