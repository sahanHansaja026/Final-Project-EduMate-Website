import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from the backend/.env file
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables."""

    # Environment: development | testing | production
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development").strip().lower()
    DEBUG: bool = os.getenv("DEBUG", "True").strip().lower() == "true"

    # Database - configured exclusively through the environment, never hardcoded.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/edumate")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "sqlite://")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_RECYCLE_SECONDS: int = int(os.getenv("DB_POOL_RECYCLE_SECONDS", "3600"))

    @property
    def database_url(self) -> str:
        """Return the database URL that matches the current environment."""
        if self.ENVIRONMENT == "test":
            return self.TEST_DATABASE_URL
        return self.DATABASE_URL

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # AWS S3
    AWS_BUCKET_NAME: str = os.getenv("AWS_BUCKET_NAME", "edumate-files")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")

    # OpenAI/OpenRouter
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")


settings = Settings()
