"""
Configuration settings for the orchestrator
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"
    
    # Database Settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "rfp_automation")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Redis Settings
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    
    # Qdrant Settings
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "products")
    
    # AI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    
    # Application Settings
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    
    # File Upload Settings
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")
    MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10485760))  # 10MB


settings = Settings()
