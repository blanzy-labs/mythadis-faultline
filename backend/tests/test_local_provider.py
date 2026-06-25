import pytest

from app.config import Settings
from app.providers import (
    OpenAICompatibleProvider,
    ProviderCallError,
    ProviderConfigError,
)
from app.providers.openai_compatible_provider import LOCAL_API_KEY_PLACEHOLDER

LOCAL_FAKE_KEY = "test-local-key-should-not-leak"
PROMPT_TEXT = "Prompt text should not leak"


def make_settings(**overrides: object) -> Settings:
    values = {
        "LOCAL_LLM_ENABLED": True,
        "LOCAL_LLM_BASE_URL": "http://localhost:11434/v1",
        "LOCAL_LLM_MODEL": "test-local-model",
        "LOCAL_LLM_API_KEY": "",
        "LOCAL_LLM_TIMEOUT_SECONDS": 120,
        **overrides,
    }
    return Settings(_env_file=None, **values)


@pytest.mark.asyncio
async def test_disabled_local_provider_raises_safe_config_error() -> None:
    provider = OpenAICompatibleProvider(make_settings(LOCAL_LLM_ENABLED=False))

    with pytest.raises(
        ProviderConfigError,
        match=r"^Local LLM provider is not configured\.$",
    ):
        await provider.generate(PROMPT_TEXT)


@pytest.mark.asyncio
async def test_missing_base_url_raises_safe_config_error() -> None:
    provider = OpenAICompatibleProvider(make_settings(LOCAL_LLM_BASE_URL=""))

    with pytest.raises(
        ProviderConfigError,
        match=r"^Local LLM base URL is not configured\.$",
    ):
        await provider.generate(PROMPT_TEXT)


@pytest.mark.asyncio
async def test_missing_model_raises_safe_config_error() -> None:
    provider = OpenAICompatibleProvider(make_settings(LOCAL_LLM_MODEL=""))

    with pytest.raises(
        ProviderConfigError,
        match=r"^Local LLM model is not configured\.$",
    ):
        await provider.generate(PROMPT_TEXT)


def test_empty_api_key_uses_safe_internal_placeholder() -> None:
    provider = OpenAICompatibleProvider(make_settings(LOCAL_LLM_API_KEY=""))

    assert provider.api_key == LOCAL_API_KEY_PLACEHOLDER


def test_configured_api_key_is_used_internally() -> None:
    provider = OpenAICompatibleProvider(
        make_settings(LOCAL_LLM_API_KEY=LOCAL_FAKE_KEY)
    )

    assert provider.api_key == LOCAL_FAKE_KEY


@pytest.mark.asyncio
async def test_mocked_successful_local_response_returns_text(monkeypatch) -> None:
    provider = OpenAICompatibleProvider(make_settings())

    async def mock_call(prompt: str) -> str:
        assert prompt == PROMPT_TEXT
        return "Local response"

    monkeypatch.setattr(provider, "_call_provider", mock_call)

    assert await provider.generate(PROMPT_TEXT) == "Local response"


@pytest.mark.asyncio
async def test_mocked_empty_local_response_raises_safe_error(monkeypatch) -> None:
    provider = OpenAICompatibleProvider(make_settings())

    async def mock_call(prompt: str) -> str:
        return "   "

    monkeypatch.setattr(provider, "_call_provider", mock_call)

    with pytest.raises(
        ProviderCallError,
        match=r"^Local LLM provider returned an empty response\.$",
    ):
        await provider.generate(PROMPT_TEXT)


@pytest.mark.asyncio
async def test_mocked_provider_failure_is_sanitized(monkeypatch) -> None:
    provider = OpenAICompatibleProvider(
        make_settings(LOCAL_LLM_API_KEY=LOCAL_FAKE_KEY)
    )

    async def mock_call(prompt: str) -> str:
        raise RuntimeError(f"Failure for {LOCAL_FAKE_KEY}: {prompt}")

    monkeypatch.setattr(provider, "_call_provider", mock_call)

    with pytest.raises(ProviderCallError) as exc_info:
        await provider.generate(PROMPT_TEXT)

    assert str(exc_info.value) == "Local LLM provider call failed."
    assert LOCAL_FAKE_KEY not in str(exc_info.value)
    assert PROMPT_TEXT not in str(exc_info.value)
    assert exc_info.value.__cause__ is None


@pytest.mark.asyncio
async def test_timeout_failure_is_sanitized(monkeypatch) -> None:
    provider = OpenAICompatibleProvider(make_settings())

    async def mock_call(prompt: str) -> str:
        raise TimeoutError(f"Timeout while sending {prompt}")

    monkeypatch.setattr(provider, "_call_provider", mock_call)

    with pytest.raises(ProviderCallError) as exc_info:
        await provider.generate(PROMPT_TEXT)

    assert str(exc_info.value) == "Local LLM provider call failed."
    assert PROMPT_TEXT not in str(exc_info.value)
