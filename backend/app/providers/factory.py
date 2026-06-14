from app.config import Settings
from app.providers.base import BaseProvider
from app.providers.errors import UnsupportedProviderError
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider


def get_provider(name: str, settings: Settings) -> BaseProvider:
    normalized_name = name.strip().lower()

    if normalized_name == "openai":
        return OpenAIProvider(settings)
    if normalized_name == "gemini":
        return GeminiProvider(settings)

    raise UnsupportedProviderError(f"Unsupported provider: {name}.")
