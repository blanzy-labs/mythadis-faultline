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
