import json
import re
from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from app.faultline.schemas import AuditReport, ScannerReport

ReportT = TypeVar("ReportT", bound=BaseModel)


def scanner_fallback_report() -> ScannerReport:
    return ScannerReport(
        faultline_summary=(
            "The scanner response could not be fully parsed into the expected "
            "structure."
        ),
        surface_claim=(
            "Unable to reliably extract the surface claim from the scanner response."
        ),
        collapse_risks=["Scanner output was malformed or incomplete."],
        validation_tests=["Retry the scan or simplify the input."],
        questions_before_commitment=[
            "Was the original input specific enough for a structured risk review?"
        ],
        risk_level="high",
        recommended_next_move=(
            "Retry with a clearer input or a different provider."
        ),
    )


def auditor_fallback_report() -> AuditReport:
    return AuditReport(
        audit_summary=(
            "The auditor response could not be fully parsed into the expected "
            "structure."
        ),
        missed_risks=["Auditor output was malformed or incomplete."],
        validation_plan_gaps=[
            "The audit validation gaps could not be reliably extracted."
        ],
        risk_level_challenge=(
            "Unable to reliably assess whether the scanner risk level should be "
            "challenged."
        ),
        recommended_report_improvements=[
            "Retry the audit or simplify the input."
        ],
        auditor_confidence="low",
        final_caution=(
            "Do not treat this audit as complete; rerun with clearer input or "
            "another provider."
        ),
    )


def parse_scanner_report(raw_response: str) -> ScannerReport:
    return _parse_report(raw_response, ScannerReport, scanner_fallback_report)


def parse_audit_report(raw_response: str) -> AuditReport:
    return _parse_report(raw_response, AuditReport, auditor_fallback_report)


def _parse_report(
    raw_response: str,
    report_type: type[ReportT],
    fallback_factory: Callable[[], ReportT],
) -> ReportT:
    try:
        payload = _extract_json_object(raw_response)
        return report_type.model_validate(payload)
    except (TypeError, ValueError, json.JSONDecodeError, ValidationError):
        return fallback_factory()


def _extract_json_object(raw_response: str) -> dict[str, Any]:
    if not isinstance(raw_response, str):
        raise TypeError("Provider response must be text.")

    candidate = raw_response.strip()
    fence_match = re.fullmatch(
        r"```(?:json)?\s*(.*?)\s*```",
        candidate,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if fence_match:
        candidate = fence_match.group(1).strip()

    try:
        parsed = json.loads(candidate)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    for index, character in enumerate(candidate):
        if character != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(candidate[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed

    raise json.JSONDecodeError("No JSON object found.", candidate, 0)
