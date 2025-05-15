from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # MongoDB settings
    mongodb_uri: str = Field(..., alias="MONGODB_URI")
    mongodb_db_name: str = Field(..., alias="MONGODB_DB_NAME")

    # API settings
    api_v1_str: str = Field("/api/v1", alias="API_V1_STR")
    server_port: int = Field(8000, alias="SERVER_PORT")
    debug: bool = Field(False, alias="DEBUG")

    # Security settings
    secret_key: str = Field(..., alias="SECRET_KEY")

    # Application name and description
    title: str = "Client Management API"
    description: str = "A REST API for client management using FastAPI with async operations"
    version: str = "0.1.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()