from app.faultline.modes import ScanModeDefinition
from app.faultline.schemas import ScannerReport


SCANNER_JSON_CONTRACT = """{
  "faultline_summary": "string",
  "surface_claim": "string",
  "hidden_assumptions": ["string"],
  "pressure_points": ["string"],
  "collapse_risks": ["string"],
  "weak_evidence": ["string"],
  "what_would_break_this": ["string"],
  "validation_tests": ["string"],
  "questions_before_commitment": ["string"],
  "risk_level": "low | medium | high | critical",
  "recommended_next_move": "string"
}"""

AUDITOR_JSON_CONTRACT = """{
  "audit_summary": "string",
  "missed_risks": ["string"],
  "weak_or_vague_findings": ["string"],
  "validation_plan_gaps": ["string"],
  "risk_level_challenge": "string",
  "recommended_report_improvements": ["string"],
  "auditor_confidence": "low | medium | high",
  "final_caution": "string"
}"""


def build_scanner_prompt(
    user_input: str,
    scan_mode: ScanModeDefinition,
) -> str:
    return f"""You are the Primary Faultline Scanner.

Expose hidden assumptions, pressure points, weak evidence, and collapse risks.
Be direct, practical, and skeptical. Do not be vague, motivational, or polite
at the expense of accuracy.

Scan mode: {scan_mode.label}
Mode guidance: {scan_mode.guidance}

Produce concrete findings and practical validation tests. Avoid generic advice
such as "do more research" unless it includes a specific test. Include at least
three items in major list fields when the evidence supports them. Set the risk
level from uncertainty and downside, not optimism.

Return JSON only. Follow this contract exactly:
{SCANNER_JSON_CONTRACT}

Do not wrap the JSON in Markdown fences. Do not include commentary outside the
JSON.

User input:
{user_input}"""


def build_auditor_prompt(
    user_input: str,
    scan_mode: ScanModeDefinition,
    scanner_report: ScannerReport,
) -> str:
    return f"""You are the independent Faultline Auditor.

Challenge the Primary Scanner report. Find missed risks, vague findings, weak
reasoning, soft conclusions, and validation gaps. Do not merely agree with the
scanner. Be direct, practical, and skeptical.

Scan mode: {scan_mode.label}
Mode guidance: {scan_mode.guidance}

Identify two or three missed risks when possible. Directly challenge weak or
vague findings. Challenge the assigned risk level if it appears too low or too
high. Recommend practical report improvements and end with a caution a human
can act on.

Return JSON only. Follow this contract exactly:
{AUDITOR_JSON_CONTRACT}

Do not wrap the JSON in Markdown fences. Do not include commentary outside the
JSON.

Original user input:
{user_input}

Primary Scanner report:
{scanner_report.model_dump_json(indent=2)}"""
