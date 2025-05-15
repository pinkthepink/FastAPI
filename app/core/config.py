import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional, List

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Petshop API"
    
    # Environment settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # MongoDB settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/petshop")
    MONGODB_TEST_URI: str = os.getenv("MONGODB_TEST_URI", "mongodb://localhost:27017/petshop-test")
    
    # JWT Auth settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]  # In production, this should be limited
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Set the database URI based on environment
def get_mongodb_uri() -> str:
    if settings.ENVIRONMENT == "test":
        return settings.MONGODB_TEST_URI
    return settings.MONGODB_URI