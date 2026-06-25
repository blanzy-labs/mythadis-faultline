from openai import AsyncOpenAI

from app.config import Settings
from app.providers.base import BaseProvider
from app.providers.errors import ProviderCallError, ProviderConfigError

LOCAL_API_KEY_PLACEHOLDER = "local-not-required"


class OpenAICompatibleProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        self.enabled = settings.LOCAL_LLM_ENABLED
        self.base_url = settings.LOCAL_LLM_BASE_URL
        self.model = settings.LOCAL_LLM_MODEL
        self.api_key = settings.LOCAL_LLM_API_KEY or LOCAL_API_KEY_PLACEHOLDER
        self.timeout_seconds = settings.LOCAL_LLM_TIMEOUT_SECONDS

    async def generate(self, prompt: str) -> str:
        if not self.enabled:
            raise ProviderConfigError("Local LLM provider is not configured.")
        if not self.base_url.strip():
            raise ProviderConfigError("Local LLM base URL is not configured.")
        if not self.model.strip():
            raise ProviderConfigError("Local LLM model is not configured.")

        try:
            response_text = await self._call_provider(prompt)
        except ProviderCallError:
            raise
        except Exception:
            raise ProviderCallError("Local LLM provider call failed.") from None

        if not isinstance(response_text, str) or not response_text.strip():
            raise ProviderCallError("Local LLM provider returned an empty response.")

        return response_text

    async def _call_provider(self, prompt: str) -> str:
        async with AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=self.timeout_seconds,
        ) as client:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )

        if not response.choices:
            return ""

        return response.choices[0].message.content or ""
