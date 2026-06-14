import pytest
from pydantic import ValidationError

from app.faultline.modes import SCAN_MODES, ScanModeId, get_scan_mode
from app.faultline.schemas import (
    AuditReport,
    ModelsUsed,
    ScanRequest,
    ScanResponse,
    ScannerReport,
)
from tests.faultline_fixtures import AUDITOR_PAYLOAD, SCANNER_PAYLOAD


def valid_request_data() -> dict[str, str]:
    return {
        "input": "A focused business idea",
        "scan_mode": "business_idea",
        "scanner_provider": "openai",
        "auditor_provider": "gemini",
    }


def test_valid_request_is_normalized() -> None:
    request = ScanRequest(
        **{
            **valid_request_data(),
            "input": "  A focused business idea  ",
            "scanner_provider": " OPENAI ",
            "auditor_provider": "Gemini",
        }
    )

    assert request.input == "A focused business idea"
    assert request.scanner_provider == "openai"
    assert request.auditor_provider == "gemini"


@pytest.mark.parametrize("invalid_input", ["", "   "])
def test_empty_input_is_rejected(invalid_input: str) -> None:
    with pytest.raises(ValidationError):
        ScanRequest(**{**valid_request_data(), "input": invalid_input})


def test_overlong_input_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ScanRequest(**{**valid_request_data(), "input": "x" * 12001})


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("scan_mode", "unknown_mode"),
        ("scanner_provider", "claude"),
        ("auditor_provider", "claude"),
    ],
)
def test_invalid_request_enum_is_rejected(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        ScanRequest(**{**valid_request_data(), field: value})


def test_response_schema_accepts_valid_reports() -> None:
    response = ScanResponse(
        input="A focused business idea",
        scan_mode=ScanModeId.BUSINESS_IDEA,
        scanner_report=ScannerReport.model_validate(SCANNER_PAYLOAD),
        audit_report=AuditReport.model_validate(AUDITOR_PAYLOAD),
        models_used=ModelsUsed(
            scanner_provider="openai",
            scanner_model="scanner-model",
            auditor_provider="gemini",
            auditor_model="auditor-model",
        ),
    )

    assert response.scanner_report.risk_level == "high"
    assert response.audit_report.auditor_confidence == "high"


def test_all_v1_scan_modes_are_defined() -> None:
    assert set(SCAN_MODES) == set(ScanModeId)
    assert len(SCAN_MODES) == 5
    assert len({mode.id for mode in SCAN_MODES.values()}) == len(SCAN_MODES)
    for mode in SCAN_MODES.values():
        assert mode.id
        assert mode.label
        assert mode.description
        assert mode.scanner_guidance.strip()
        assert mode.auditor_guidance.strip()


def test_scan_mode_lookup_accepts_normalized_value() -> None:
    mode = get_scan_mode(" BUSINESS_IDEA ")

    assert mode.id == ScanModeId.BUSINESS_IDEA


def test_scan_mode_lookup_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="Unsupported scan mode"):
        get_scan_mode("unknown")
