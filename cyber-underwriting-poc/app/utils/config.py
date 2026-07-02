import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str | None = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./cyber_underwriting.db")
    environment: str = os.getenv("ENVIRONMENT", "development")


def get_settings() -> Settings:
    return Settings()
