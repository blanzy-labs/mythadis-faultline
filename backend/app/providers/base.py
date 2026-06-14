from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a plain-text response for a plain-text prompt."""
