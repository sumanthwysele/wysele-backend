from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional
from pydantic import AnyHttpUrl, field_validator, EmailStr

class Settings(BaseSettings):
    # --- API Settings ---
    PROJECT_NAME: str = "Wysele_Backend"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # --- Security ---
    SECRET_KEY: str  
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # --- Root Admin Configuration ---
    FIRST_SUPERUSER: str = "admin@wysele.com" 
    FIRST_SUPERUSER_PASSWORD: str 

    # --- Database ---
    DATABASE_URL: str 

    # --- CORS Settings ---
    BACKEND_CORS_ORIGINS: List[str] = []

    # --- Email Settings ---
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    # This must match the key in your .env exactly
    EMAILS_FROM_EMAIL: str 
    FRONTEND_URL: str = "http://localhost:3000"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # UPDATED: Pydantic V2 uses model_config instead of class Config
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # This prevents the "Extra inputs are not permitted" error
    )

settings = Settings()