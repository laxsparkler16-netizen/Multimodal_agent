"""
Configuration module for Voice Translation App.
Loads environment variables and defines application settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # AWS Kiro Configuration
    KIRO_API_KEY: str
    KIRO_API_BASE_URL: str = "https://api.kiro.aws.amazon.com/v1"
    KIRO_ASR_MODEL_ID: str = "kiro-asr-multilingual-v1"
    KIRO_TRANSLATION_MODEL_ID: str = "kiro-translate-indian-languages-v1"
    
    # Demo/Mock Mode
    USE_MOCK_MODE: str = "true"
    
    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:8080,http://127.0.0.1:8080"
    
    # Audio Processing Configuration
    MAX_AUDIO_SIZE_MB: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Supported Languages
    SUPPORTED_INPUT_LANGUAGES: List[str] = [
        "en-US", "hi-IN", "ta-IN", "te-IN", 
        "kn-IN", "ml-IN", "bn-IN", "mr-IN"
    ]
    
    SUPPORTED_TARGET_LANGUAGES: List[str] = [
        "en", "hi", "ta", "te", "ml", "kn", "mr", "bn", "or"
    ]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def max_audio_size_bytes(self) -> int:
        """Convert max audio size from MB to bytes."""
        return self.MAX_AUDIO_SIZE_MB * 1024 * 1024
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
