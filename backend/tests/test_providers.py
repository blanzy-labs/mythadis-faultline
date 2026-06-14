from collections.abc import Callable

import pytest

from app.config import Settings
from app.providers import (
    GeminiProvider,
    OpenAIProvider,
    ProviderCallError,
    ProviderConfigError,
    UnsupportedProviderError,
    get_provider,
)

OPENAI_FAKE_KEY = "test-openai-key-should-not-leak"
GEMINI_FAKE_KEY = "test-gemini-key-should-not-leak"


def make_settings(**overrides: str) -> Settings:
    values = {
        "OPENAI_API_KEY": "",
        "GEMINI_API_KEY": "",
        **overrides,
    }
    return Settings(_env_file=None, **values)


@pytest.mark.parametrize(
    ("name", "expected_type"),
    [
        ("openai", OpenAIProvider),
        ("gemini", GeminiProvider),
        ("OPENAI", OpenAIProvider),
        (" Gemini ", GeminiProvider),
    ],
)
def test_factory_returns_supported_provider(
    name: str,
    expected_type: type[OpenAIProvider] | type[GeminiProvider],
) -> None:
    provider = get_provider(name, make_settings())

    assert isinstance(provider, expected_type)


def test_factory_rejects_unsupported_provider() -> None:
    with pytest.raises(
        UnsupportedProviderError,
        match=r"^Unsupported provider: claude\.$",
    ):
        get_provider("claude", make_settings())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("provider_factory", "message"),
    [
        (
            lambda: OpenAIProvider(make_settings()),
            "OpenAI API key is not configured.",
        ),
        (
            lambda: GeminiProvider(make_settings()),
            "Gemini API key is not configured.",
        ),
    ],
)
async def test_missing_key_raises_safe_config_error(
    provider_factory: Callable[[], OpenAIProvider | GeminiProvider],
    message: str,
) -> None:
    provider = provider_factory()

    with pytest.raises(ProviderConfigError, match=rf"^{message}$"):
        await provider.generate("Test prompt")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("provider", "response_text"),
    [
        (
            OpenAIProvider(make_settings(OPENAI_API_KEY=OPENAI_FAKE_KEY)),
            "OpenAI response",
        ),
        (
            GeminiProvider(make_settings(GEMINI_API_KEY=GEMINI_FAKE_KEY)),
            "Gemini response",
        ),
    ],
)
async def test_mocked_provider_success_returns_text(
    monkeypatch,
    provider: OpenAIProvider | GeminiProvider,
    response_text: str,
) -> None:
    async def mock_call(prompt: str) -> str:
        assert prompt == "Test prompt"
        return response_text

    monkeypatch.setattr(provider, "_call_provider", mock_call)

    assert await provider.generate("Test prompt") == response_text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("provider", "expected_message", "fake_key"),
    [
        (
            OpenAIProvider(make_settings(OPENAI_API_KEY=OPENAI_FAKE_KEY)),
            "OpenAI provider call failed.",
            OPENAI_FAKE_KEY,
        ),
        (
            GeminiProvider(make_settings(GEMINI_API_KEY=GEMINI_FAKE_KEY)),
            "Gemini provider call failed.",
            GEMINI_FAKE_KEY,
        ),
    ],
)
async def test_mocked_provider_failure_is_sanitized(
    monkeypatch,
    provider: OpenAIProvider | GeminiProvider,
    expected_message: str,
    fake_key: str,
) -> None:
    async def mock_call(prompt: str) -> str:
        raise RuntimeError(f"SDK failure using {fake_key}")

    monkeypatch.setattr(provider, "_call_provider", mock_call)

    with pytest.raises(ProviderCallError) as exc_info:
        await provider.generate("Test prompt")

    assert str(exc_info.value) == expected_message
    assert fake_key not in str(exc_info.value)
    assert exc_info.value.__cause__ is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "provider",
    [
        OpenAIProvider(make_settings(OPENAI_API_KEY=OPENAI_FAKE_KEY)),
        GeminiProvider(make_settings(GEMINI_API_KEY=GEMINI_FAKE_KEY)),
    ],
)
async def test_empty_provider_response_is_rejected(
    monkeypatch,
    provider: OpenAIProvider | GeminiProvider,
) -> None:
    async def mock_call(prompt: str) -> str:
        return "   "

    monkeypatch.setattr(provider, "_call_provider", mock_call)

    with pytest.raises(
        ProviderCallError,
        match=r"^Provider returned an empty response\.$",
    ):
        await provider.generate("Test prompt")
