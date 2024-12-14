from pydantic_settings import BaseSettings
from typing import Optional
import os
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "Digital Twin Medical System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Data Integration Settings
    DATA_LAKE_PATH: str = "data/lake"
    EHR_API_ENDPOINT: str
    EHR_API_KEY: str
    IMAGING_STORAGE_PATH: str = "data/imaging"
    
    # ML and Simulation Settings
    ML_MODEL_PATH: str = "models/ml_pipeline.joblib"
    SIMULATION_OUTPUT_PATH: str = "data/simulations"
    
    # Security Settings
    MASTER_KEY: str = secrets.token_urlsafe(32)
    ENCRYPTION_SALT: str = secrets.token_urlsafe(16)
    
    # JWT Settings
    JWT_ALGORITHM: str = "HS256"
    
    # CORS Settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://your-production-frontend.com"
    ]
    
    # Compliance Settings
    ENABLE_AUDIT_LOGS: bool = True
    ENABLE_DATA_ENCRYPTION: bool = True
    ENABLE_ANONYMIZATION: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings() 