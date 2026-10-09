"""
Configuration settings for Thathvamasi HR Consultancy backend
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Thathvamasi HR Consultancy"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # CORS
    @property
    def CORS_ORIGINS(self) -> List[str]:
        default_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://thathvamasi.com",
            "https://www.thathvamasi.com",
        ]
        raw = os.getenv("CORS_ORIGINS")
        if not raw:
            return default_origins
        import json
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return list(set(default_origins + parsed))
        except Exception:
            pass
        custom = [item.strip() for item in raw.split(",") if item.strip()]
        return list(set(default_origins + custom))
    
    # PostgreSQL Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "thathvamasi_hr")
    
    # Database URL for SQLAlchemy
    @property
    def DATABASE_URL(self) -> str:
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            if env_url.startswith("postgresql://"):
                return env_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif env_url.startswith("postgres://"):
                return env_url.replace("postgres://", "postgresql+asyncpg://", 1)
            return env_url
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def DATABASE_URL_SYNC(self) -> str:
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            if env_url.startswith("postgresql+asyncpg://"):
                return env_url.replace("postgresql+asyncpg://", "postgresql://", 1)
            elif env_url.startswith("postgres://"):
                return env_url.replace("postgres://", "postgresql://", 1)
            return env_url
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Pool configuration
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    
    # JWT Authentication
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif", "image/webp",
        "application/pdf", 
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: Optional[str] = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: Optional[str] = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: Optional[str] = os.getenv("CLOUDINARY_API_SECRET")
    CLOUDINARY_FOLDER: str = "thathvamasi"
    
    # Email
    EMAIL_HOST: Optional[str] = os.getenv("EMAIL_HOST")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USERNAME: Optional[str] = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD: Optional[str] = os.getenv("EMAIL_PASSWORD")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@thathvamasi.com")
    EMAIL_USE_TLS: bool = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
    
    # WhatsApp
    WHATSAPP_NUMBER: str = os.getenv("WHATSAPP_NUMBER", "+919876543210")
    WHATSAPP_MESSAGE: str = "Hello Thathvamasi HR Consultancy, I'm interested in..."
    
    # Security
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    LOG_MAX_SIZE_MB: int = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    # Admin
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@thathvamasi.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Redis (optional for caching)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()