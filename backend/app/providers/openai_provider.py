from openai import AsyncOpenAI

from app.config import Settings
from app.providers.base import BaseProvider
from app.providers.errors import ProviderCallError, ProviderConfigError


class OpenAIProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    async def generate(self, prompt: str) -> str:
        if not self.api_key.strip():
            raise ProviderConfigError("OpenAI API key is not configured.")

        try:
            response_text = await self._call_provider(prompt)
        except ProviderCallError:
            raise
        except Exception:
            raise ProviderCallError("OpenAI provider call failed.") from None

        if not isinstance(response_text, str) or not response_text.strip():
            raise ProviderCallError("Provider returned an empty response.")

        return response_text

    async def _call_provider(self, prompt: str) -> str:
        async with AsyncOpenAI(api_key=self.api_key) as client:
            response = await client.responses.create(
                model=self.model,
                input=prompt,
            )
        return response.output_text
