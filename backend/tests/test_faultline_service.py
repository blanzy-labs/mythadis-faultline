import pytest

from app.config import Settings
from app.faultline.schemas import ScanRequest
from app.faultline.service import run_faultline
from app.providers import BaseProvider, ProviderCallError, ProviderConfigError
from tests.faultline_fixtures import AUDITOR_JSON, SCANNER_JSON

FAKE_SECRET = "workflow-test-key-should-not-leak"
pytestmark = pytest.mark.asyncio


def make_settings(**overrides: str) -> Settings:
    values = {
        "OPENAI_API_KEY": "",
        "GEMINI_API_KEY": "",
        "OPENAI_MODEL": "scanner-model",
        "GEMINI_MODEL": "auditor-model",
        **overrides,
    }
    return Settings(_env_file=None, **values)


class FakeProvider(BaseProvider):
    def __init__(self, response: str, calls: list[tuple[str, str]], name: str):
        self.response = response
        self.calls = calls
        self.name = name

    async def generate(self, prompt: str) -> str:
        self.calls.append((self.name, prompt))
        return self.response


async def test_workflow_uses_selected_providers_in_order() -> None:
    calls: list[tuple[str, str]] = []

    def factory(name: str, settings: Settings) -> BaseProvider:
        response = SCANNER_JSON if name == "openai" else AUDITOR_JSON
        return FakeProvider(response, calls, name)

    response = await run_faultline(
        ScanRequest(
            input="A business concept",
            scan_mode="business_idea",
            scanner_provider="openai",
            auditor_provider="gemini",
        ),
        make_settings(),
        factory,
    )

    assert [name for name, _ in calls] == ["openai", "gemini"]
    assert response.scanner_report.risk_level == "high"
    assert response.audit_report.auditor_confidence == "high"
    assert response.models_used.scanner_model == "scanner-model"
    assert response.models_used.auditor_model == "auditor-model"
    assert response.scanner_report.faultline_summary in calls[1][1]


async def test_scanner_fallback_still_runs_auditor() -> None:
    calls: list[tuple[str, str]] = []

    def factory(name: str, settings: Settings) -> BaseProvider:
        response = "malformed" if name == "openai" else AUDITOR_JSON
        return FakeProvider(response, calls, name)

    response = await run_faultline(
        ScanRequest(
            input="A business concept",
            scan_mode="business_idea",
            scanner_provider="openai",
            auditor_provider="gemini",
        ),
        make_settings(),
        factory,
    )

    assert len(calls) == 2
    assert "could not be fully parsed" in response.scanner_report.faultline_summary
    assert response.scanner_report.faultline_summary in calls[1][1]


async def test_auditor_fallback_returns_full_response() -> None:
    def factory(name: str, settings: Settings) -> BaseProvider:
        response = SCANNER_JSON if name == "openai" else "malformed"
        return FakeProvider(response, [], name)

    response = await run_faultline(
        ScanRequest(
            input="A business concept",
            scan_mode="business_idea",
            scanner_provider="openai",
            auditor_provider="gemini",
        ),
        make_settings(),
        factory,
    )

    assert response.scanner_report.risk_level == "high"
    assert response.audit_report.auditor_confidence == "low"
    assert response.models_used.auditor_provider == "gemini"


async def test_missing_key_error_is_safe() -> None:
    from app.providers import get_provider

    request = ScanRequest(
        input="A business concept",
        scan_mode="business_idea",
        scanner_provider="openai",
        auditor_provider="gemini",
    )

    try:
        await run_faultline(request, make_settings(), get_provider)
    except ProviderConfigError as exc:
        assert str(exc) == "OpenAI API key is not configured."
        assert FAKE_SECRET not in str(exc)
    else:
        raise AssertionError("Expected missing provider configuration.")


async def test_provider_failure_does_not_leak_secret() -> None:
    class FailingProvider(BaseProvider):
        async def generate(self, prompt: str) -> str:
            raise ProviderCallError("OpenAI provider call failed.")

    def factory(name: str, settings: Settings) -> BaseProvider:
        return FailingProvider()

    request = ScanRequest(
        input="A business concept",
        scan_mode="business_idea",
        scanner_provider="openai",
        auditor_provider="gemini",
    )

    try:
        await run_faultline(
            request,
            make_settings(OPENAI_API_KEY=FAKE_SECRET),
            factory,
        )
    except ProviderCallError as exc:
        assert str(exc) == "OpenAI provider call failed."
        assert FAKE_SECRET not in str(exc)
    else:
        raise AssertionError("Expected provider call failure.")
