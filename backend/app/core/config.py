from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Document Review AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-5.4-nano"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    MAX_SUMMARY_LENGTH: int = 500
    MAX_NEXT_STEPS_LENGTH: int = 300
    REQUIRED_OUTPUT_FIELDS: List[str] = [
        "summary",
        "classification",
        "next_steps",
        "confidence_score"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
