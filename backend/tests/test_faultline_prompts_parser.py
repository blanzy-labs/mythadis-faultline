import json

import pytest

from app.faultline.modes import get_scan_mode
from app.faultline.parser import parse_audit_report, parse_scanner_report
from app.faultline.prompts import (
    AUDITOR_JSON_CONTRACT,
    SAFETY_AND_LIMITATIONS,
    SCANNER_JSON_CONTRACT,
    build_auditor_prompt,
    build_scanner_prompt,
)
from app.faultline.schemas import AuditReport, ScannerReport
from tests.faultline_fixtures import (
    AUDITOR_JSON,
    AUDITOR_PAYLOAD,
    SCANNER_JSON,
    SCANNER_PAYLOAD,
)


def test_scanner_prompt_contains_role_input_guidance_and_contract() -> None:
    mode = get_scan_mode("technical_architecture")
    prompt = build_scanner_prompt("A multi-region API design", mode)

    assert "Primary Faultline Scanner" in prompt
    assert "A multi-region API design" in prompt
    assert mode.label in prompt
    assert mode.scanner_guidance in prompt
    assert SCANNER_JSON_CONTRACT in prompt
    assert "Return JSON only" in prompt
    assert "Do not wrap JSON in Markdown fences" in prompt
    assert SAFETY_AND_LIMITATIONS in prompt
    assert "Do not invent citations" in prompt
    assert "Do not claim to have browsed the web" in prompt
    assert "practical validation tests" in prompt
    assert "API key" not in prompt


def test_auditor_prompt_contains_role_input_guidance_report_and_contract() -> None:
    mode = get_scan_mode("business_idea")
    report = ScannerReport.model_validate(SCANNER_PAYLOAD)
    prompt = build_auditor_prompt("A subscription product", mode, report)

    assert "Independent Faultline Auditor" in prompt
    assert "A subscription product" in prompt
    assert mode.label in prompt
    assert mode.auditor_guidance in prompt
    assert report.faultline_summary in prompt
    assert AUDITOR_JSON_CONTRACT in prompt
    assert "Return JSON only" in prompt
    assert "Do not wrap JSON in Markdown fences" in prompt
    assert SAFETY_AND_LIMITATIONS in prompt
    assert "Do not invent citations" in prompt
    assert "Do not claim to have browsed the web" in prompt
    assert "Do not merely agree" in prompt
    assert "API key" not in prompt


def test_scanner_prompt_contract_matches_schema_fields() -> None:
    contract_fields = set(json.loads(SCANNER_JSON_CONTRACT))

    assert contract_fields == set(ScannerReport.model_fields)


def test_auditor_prompt_contract_matches_schema_fields() -> None:
    contract_fields = set(json.loads(AUDITOR_JSON_CONTRACT))

    assert contract_fields == set(AuditReport.model_fields)


@pytest.mark.parametrize(
    ("case_name", "raw_response"),
    [
        ("valid_json", SCANNER_JSON),
        ("markdown_fence", f"```\n{SCANNER_JSON}\n```"),
        ("json_fence", f"```json\n{SCANNER_JSON}\n```"),
        ("text_before_json", f"Scanner result follows:\n{SCANNER_JSON}"),
        ("text_after_json", f"{SCANNER_JSON}\nEnd of result."),
        (
            "text_before_and_after_json",
            f"Scanner result follows:\n{SCANNER_JSON}\nEnd of result.",
        ),
        (
            "unsupported_extra_field",
            json.dumps({**SCANNER_PAYLOAD, "local_model_note": "ignored"}),
        ),
    ],
)
def test_scanner_parser_recovers_common_json_formats(
    case_name: str,
    raw_response: str,
) -> None:
    report = parse_scanner_report(raw_response)

    assert report.faultline_summary == SCANNER_PAYLOAD["faultline_summary"]
    assert report.risk_level == "high"


def test_scanner_parser_uses_defaults_for_missing_fields() -> None:
    report = parse_scanner_report('{"risk_level": "medium"}')

    assert report.risk_level == "medium"
    assert report.hidden_assumptions == []
    assert "did not include" in report.faultline_summary


@pytest.mark.parametrize(
    ("case_name", "raw_response"),
    [
        ("overly_chatty_non_json", "I can help! Here is a broad risk review."),
        (
            "partial_json",
            '{"faultline_summary": "Half done", "risk_level": "medium"',
        ),
        ("empty_string", ""),
        (
            "invalid_risk_level",
            json.dumps({**SCANNER_PAYLOAD, "risk_level": "extreme"}),
        ),
    ],
)
def test_scanner_parser_returns_fallback_for_invalid_output(
    case_name: str,
    raw_response: str,
) -> None:
    report = parse_scanner_report(raw_response)

    assert report.risk_level == "high"
    assert report.collapse_risks == [
        "Scanner output was malformed or incomplete."
    ]
    if raw_response:
        assert raw_response[:30] not in report.faultline_summary


@pytest.mark.parametrize(
    ("case_name", "raw_response"),
    [
        ("valid_json", AUDITOR_JSON),
        ("markdown_fence", f"```\n{AUDITOR_JSON}\n```"),
        ("json_fence", f"```json\n{AUDITOR_JSON}\n```"),
        ("text_before_json", f"Audit result:\n{AUDITOR_JSON}"),
        ("text_after_json", f"{AUDITOR_JSON}\nReview complete."),
        (
            "text_before_and_after_json",
            f"Audit result:\n{AUDITOR_JSON}\nReview complete.",
        ),
        (
            "unsupported_extra_field",
            json.dumps({**AUDITOR_PAYLOAD, "local_model_note": "ignored"}),
        ),
    ],
)
def test_auditor_parser_recovers_common_json_formats(
    case_name: str,
    raw_response: str,
) -> None:
    report = parse_audit_report(raw_response)

    assert report.audit_summary == AUDITOR_PAYLOAD["audit_summary"]
    assert report.auditor_confidence == "high"


def test_auditor_parser_uses_defaults_for_missing_fields() -> None:
    report = parse_audit_report('{"auditor_confidence": "medium"}')

    assert report.auditor_confidence == "medium"
    assert report.missed_risks == []
    assert "did not include" in report.audit_summary


@pytest.mark.parametrize(
    ("case_name", "raw_response"),
    [
        ("overly_chatty_non_json", "Looks good overall, with a few caveats."),
        (
            "partial_json",
            '{"audit_summary": "Half done", "auditor_confidence": "medium"',
        ),
        ("empty_string", ""),
        (
            "invalid_auditor_confidence",
            json.dumps({**AUDITOR_PAYLOAD, "auditor_confidence": "certain"}),
        ),
    ],
)
def test_auditor_parser_returns_fallback_for_invalid_output(
    case_name: str,
    raw_response: str,
) -> None:
    report = parse_audit_report(raw_response)

    assert report.auditor_confidence == "low"
    assert report.missed_risks == ["Auditor output was malformed or incomplete."]
    if raw_response:
        assert raw_response[:30] not in report.audit_summary


def test_risk_and_confidence_scales_remain_constrained() -> None:
    scanner_schema = ScannerReport.model_json_schema()
    auditor_schema = AuditReport.model_json_schema()

    assert scanner_schema["properties"]["risk_level"]["enum"] == [
        "low",
        "medium",
        "high",
        "critical",
    ]
    assert auditor_schema["properties"]["auditor_confidence"]["enum"] == [
        "low",
        "medium",
        "high",
    ]
