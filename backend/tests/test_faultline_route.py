import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.faultline.routes import get_provider_factory
from app.faultline.schemas import AuditReport, ScannerReport
from app.main import app
from app.providers import BaseProvider, ProviderCallError
from tests.faultline_fixtures import AUDITOR_JSON, SCANNER_JSON


class FakeProvider(BaseProvider):
    def __init__(self, response: str):
        self.response = response

    async def generate(self, prompt: str) -> str:
        return self.response


def route_settings() -> Settings:
    return Settings(
        _env_file=None,
        OPENAI_API_KEY="route-openai-key-should-not-leak",
        GEMINI_API_KEY="route-gemini-key-should-not-leak",
        OPENAI_MODEL="route-openai-model",
        GEMINI_MODEL="route-gemini-model",
        LOCAL_LLM_ENABLED=True,
        LOCAL_LLM_BASE_URL="http://localhost:11434/v1",
        LOCAL_LLM_MODEL="route-local-model",
        LOCAL_LLM_API_KEY="route-local-key-should-not-leak",
    )


def test_faultline_route_returns_structured_response() -> None:
    def factory(name: str, settings: Settings) -> BaseProvider:
        return FakeProvider(SCANNER_JSON if name == "openai" else AUDITOR_JSON)

    app.dependency_overrides[get_provider_factory] = lambda: factory
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None,
        OPENAI_API_KEY="",
        GEMINI_API_KEY="",
        OPENAI_MODEL="route-scanner-model",
        GEMINI_MODEL="route-auditor-model",
    )
    try:
        response = TestClient(app).post(
            "/faultline/run",
            json={
                "input": "A business concept",
                "scan_mode": "business_idea",
                "scanner_provider": "openai",
                "auditor_provider": "gemini",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "A business concept"
    assert payload["scan_mode"] == "business_idea"
    assert payload["scanner_report"]["risk_level"] == "high"
    assert payload["audit_report"]["auditor_confidence"] == "high"
    assert set(payload["scanner_report"]) == set(ScannerReport.model_fields)
    assert set(payload["audit_report"]) == set(AuditReport.model_fields)
    assert payload["models_used"] == {
        "scanner_provider": "openai",
        "scanner_model": "route-scanner-model",
        "auditor_provider": "gemini",
        "auditor_model": "route-auditor-model",
    }


def test_faultline_route_reports_local_model_when_selected() -> None:
    def factory(name: str, settings: Settings) -> BaseProvider:
        return FakeProvider(
            SCANNER_JSON if name == "openai_compatible" else AUDITOR_JSON
        )

    app.dependency_overrides[get_provider_factory] = lambda: factory
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None,
        OPENAI_API_KEY="",
        GEMINI_API_KEY="",
        OPENAI_MODEL="route-scanner-model",
        GEMINI_MODEL="route-auditor-model",
        LOCAL_LLM_MODEL="route-local-model",
    )
    try:
        response = TestClient(app).post(
            "/faultline/run",
            json={
                "input": "A business concept",
                "scan_mode": "business_idea",
                "scanner_provider": "openai_compatible",
                "auditor_provider": "gemini",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["models_used"] == {
        "scanner_provider": "openai_compatible",
        "scanner_model": "route-local-model",
        "auditor_provider": "gemini",
        "auditor_model": "route-auditor-model",
    }


@pytest.mark.parametrize(
    (
        "scanner_provider",
        "auditor_provider",
        "expected_scanner_model",
        "expected_auditor_model",
    ),
    [
        (
            "openai_compatible",
            "gemini",
            "route-local-model",
            "route-gemini-model",
        ),
        (
            "openai",
            "openai_compatible",
            "route-openai-model",
            "route-local-model",
        ),
        (
            "openai_compatible",
            "openai_compatible",
            "route-local-model",
            "route-local-model",
        ),
    ],
)
def test_faultline_route_supports_mocked_local_provider_combinations(
    scanner_provider: str,
    auditor_provider: str,
    expected_scanner_model: str,
    expected_auditor_model: str,
) -> None:
    calls: list[str] = []

    def factory(name: str, settings: Settings) -> BaseProvider:
        calls.append(name)
        return FakeProvider(SCANNER_JSON if len(calls) == 1 else AUDITOR_JSON)

    app.dependency_overrides[get_provider_factory] = lambda: factory
    app.dependency_overrides[get_settings] = route_settings
    try:
        response = TestClient(app).post(
            "/faultline/run",
            json={
                "input": "A business concept",
                "scan_mode": "business_idea",
                "scanner_provider": scanner_provider,
                "auditor_provider": auditor_provider,
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert calls == [scanner_provider, auditor_provider]
    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "A business concept"
    assert payload["scan_mode"] == "business_idea"
    assert set(payload["scanner_report"]) == set(ScannerReport.model_fields)
    assert set(payload["audit_report"]) == set(AuditReport.model_fields)
    assert payload["models_used"] == {
        "scanner_provider": scanner_provider,
        "scanner_model": expected_scanner_model,
        "auditor_provider": auditor_provider,
        "auditor_model": expected_auditor_model,
    }

    serialized = response.text
    assert "route-local-key-should-not-leak" not in serialized
    assert "route-openai-key-should-not-leak" not in serialized
    assert "route-gemini-key-should-not-leak" not in serialized
    assert "http://localhost:11434/v1" not in serialized


def test_faultline_route_rejects_invalid_request() -> None:
    response = TestClient(app).post(
        "/faultline/run",
        json={
            "input": " ",
            "scan_mode": "invalid",
            "scanner_provider": "claude",
            "auditor_provider": "gemini",
        },
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_faultline_route_returns_safe_missing_key_error() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None,
        OPENAI_API_KEY="",
        GEMINI_API_KEY="",
    )
    try:
        response = TestClient(app).post(
            "/faultline/run",
            json={
                "input": "A business concept",
                "scan_mode": "business_idea",
                "scanner_provider": "openai",
                "auditor_provider": "gemini",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json() == {
        "detail": "OpenAI API key is not configured."
    }


def test_faultline_route_returns_safe_provider_failure() -> None:
    class FailingProvider(BaseProvider):
        async def generate(self, prompt: str) -> str:
            raise ProviderCallError("OpenAI provider call failed.")

    def factory(name: str, settings: Settings) -> BaseProvider:
        return FailingProvider()

    app.dependency_overrides[get_provider_factory] = lambda: factory
    try:
        response = TestClient(app).post(
            "/faultline/run",
            json={
                "input": "A business concept",
                "scan_mode": "business_idea",
                "scanner_provider": "openai",
                "auditor_provider": "gemini",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json() == {"detail": "OpenAI provider call failed."}


def test_health_still_works_with_faultline_route() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
