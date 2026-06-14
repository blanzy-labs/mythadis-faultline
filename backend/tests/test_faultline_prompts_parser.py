import json

import pytest

from app.faultline.modes import get_scan_mode
from app.faultline.parser import parse_audit_report, parse_scanner_report
from app.faultline.prompts import (
    AUDITOR_JSON_CONTRACT,
    SCANNER_JSON_CONTRACT,
    build_auditor_prompt,
    build_scanner_prompt,
)
from app.faultline.schemas import ScannerReport
from tests.faultline_fixtures import (
    AUDITOR_JSON,
    AUDITOR_PAYLOAD,
    SCANNER_JSON,
    SCANNER_PAYLOAD,
)


def test_scanner_prompt_contains_input_guidance_and_contract() -> None:
    mode = get_scan_mode("technical_architecture")
    prompt = build_scanner_prompt("A multi-region API design", mode)

    assert "A multi-region API design" in prompt
    assert mode.guidance in prompt
    assert SCANNER_JSON_CONTRACT in prompt
    assert "Return JSON only" in prompt


def test_auditor_prompt_contains_input_guidance_report_and_contract() -> None:
    mode = get_scan_mode("business_idea")
    report = ScannerReport.model_validate(SCANNER_PAYLOAD)
    prompt = build_auditor_prompt("A subscription product", mode, report)

    assert "A subscription product" in prompt
    assert mode.guidance in prompt
    assert report.faultline_summary in prompt
    assert AUDITOR_JSON_CONTRACT in prompt
    assert "Return JSON only" in prompt


@pytest.mark.parametrize(
    "raw_response",
    [
        SCANNER_JSON,
        f"```json\n{SCANNER_JSON}\n```",
        f"Scanner result follows:\n{SCANNER_JSON}\nEnd of result.",
    ],
)
def test_scanner_parser_recovers_common_json_formats(raw_response: str) -> None:
    report = parse_scanner_report(raw_response)

    assert report.faultline_summary == SCANNER_PAYLOAD["faultline_summary"]
    assert report.risk_level == "high"


def test_scanner_parser_uses_defaults_for_missing_fields() -> None:
    report = parse_scanner_report('{"risk_level": "medium"}')

    assert report.risk_level == "medium"
    assert report.hidden_assumptions == []
    assert "did not include" in report.faultline_summary


@pytest.mark.parametrize(
    "raw_response",
    [
        "not json",
        json.dumps({**SCANNER_PAYLOAD, "risk_level": "extreme"}),
    ],
)
def test_scanner_parser_returns_fallback_for_invalid_output(
    raw_response: str,
) -> None:
    report = parse_scanner_report(raw_response)

    assert report.risk_level == "high"
    assert report.collapse_risks == [
        "Scanner output was malformed or incomplete."
    ]


@pytest.mark.parametrize(
    "raw_response",
    [
        AUDITOR_JSON,
        f"```json\n{AUDITOR_JSON}\n```",
        f"Audit result:\n{AUDITOR_JSON}\nReview complete.",
    ],
)
def test_auditor_parser_recovers_common_json_formats(raw_response: str) -> None:
    report = parse_audit_report(raw_response)

    assert report.audit_summary == AUDITOR_PAYLOAD["audit_summary"]
    assert report.auditor_confidence == "high"


def test_auditor_parser_uses_defaults_for_missing_fields() -> None:
    report = parse_audit_report('{"auditor_confidence": "medium"}')

    assert report.auditor_confidence == "medium"
    assert report.missed_risks == []
    assert "did not include" in report.audit_summary


@pytest.mark.parametrize(
    "raw_response",
    [
        "{broken",
        json.dumps({**AUDITOR_PAYLOAD, "auditor_confidence": "certain"}),
    ],
)
def test_auditor_parser_returns_fallback_for_invalid_output(
    raw_response: str,
) -> None:
    report = parse_audit_report(raw_response)

    assert report.auditor_confidence == "low"
    assert report.missed_risks == ["Auditor output was malformed or incomplete."]
