"""
Configuration settings for GovSense AI
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Google Cloud Configuration
    PROJECT_ID: str = "govsense-ai-mvp"
    REGION: str = "asia-south1"
    LOCATION: str = "asia-south1"
    
    # Google Cloud Credentials
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    
    # BigQuery Configuration
    BIGQUERY_DATASET: str = "govsense"
    BIGQUERY_RAW_DATASET: str = "govsense_raw"
    BIGQUERY_METRICS_DATASET: str = "govsense_metrics"
    
    # Vertex AI Configuration
    VERTEX_AI_ENDPOINT_ID: Optional[str] = None
    VERTEX_AI_MODEL_NAME: str = "demand-forecast-model"
    
    # Gemini API Configuration
    GEMINI_API_KEY: Optional[str] = None
    
    # Cloud Storage Configuration
    GCS_BUCKET: str = "govsense-data-lake"
    GCS_ML_BUCKET: str = "govsense-ml-models"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8080
    API_RELOAD: bool = True
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # Feature Flags
    ENABLE_GEMINI: bool = True
    ENABLE_VERTEX_AI: bool = False  # Set to False for local dev without GCP
    ENABLE_BIGQUERY: bool = False  # Set to False for local dev without GCP
    USE_MOCK_DATA: bool = True  # Use mock data for demo
    
    # Database (for local development)
    DATABASE_URL: str = "sqlite:///./govsense.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env file


# Create settings instance
settings = Settings()
