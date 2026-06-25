from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4.1-mini"
    GEMINI_MODEL: str = "gemini-2.5-flash"
    LOCAL_LLM_ENABLED: bool = False
    LOCAL_LLM_BASE_URL: str = ""
    LOCAL_LLM_MODEL: str = ""
    LOCAL_LLM_API_KEY: str = ""
    LOCAL_LLM_TIMEOUT_SECONDS: int = 120

    model_config = SettingsConfigDict(
        env_file=(REPOSITORY_ROOT / ".env", BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
