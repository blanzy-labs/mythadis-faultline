from google import genai

from app.config import Settings
from app.providers.base import BaseProvider
from app.providers.errors import ProviderCallError, ProviderConfigError


class GeminiProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL

    async def generate(self, prompt: str) -> str:
        if not self.api_key.strip():
            raise ProviderConfigError("Gemini API key is not configured.")

        try:
            response_text = await self._call_provider(prompt)
        except ProviderCallError:
            raise
        except Exception:
            raise ProviderCallError("Gemini provider call failed.") from None

        if not isinstance(response_text, str) or not response_text.strip():
            raise ProviderCallError("Provider returned an empty response.")

        return response_text

    async def _call_provider(self, prompt: str) -> str:
        client = genai.Client(api_key=self.api_key)
        async_client = client.aio
        try:
            response = await async_client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        finally:
            await async_client.aclose()
