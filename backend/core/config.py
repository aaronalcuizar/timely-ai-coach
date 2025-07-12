import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application configuration settings"""
    
    # App Info
    app_name: str = "Timely"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./timely.db"
    
    # LLM APIs
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Auth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    jwt_secret_key: str = "your-super-secret-key-change-this"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Vector DB
    chroma_db_path: str = "./data/vectors/chroma_db"
    
    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"
    
    def __init__(self):
        """Load settings from environment variables"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", self.jwt_secret_key)
        self.database_url = os.getenv("DATABASE_URL", self.database_url)
        
        # Convert string 'true'/'false' to boolean
        debug_env = os.getenv("DEBUG", "true").lower()
        self.debug = debug_env in ("true", "1", "yes")

# Create global settings instance
settings = Settings()