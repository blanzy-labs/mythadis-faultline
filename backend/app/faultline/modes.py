from dataclasses import dataclass
from enum import StrEnum


class ScanModeId(StrEnum):
    BUSINESS_IDEA = "business_idea"
    TECHNICAL_ARCHITECTURE = "technical_architecture"
    PRODUCT_FEATURE = "product_feature"
    SECURITY_RISK_DECISION = "security_risk_decision"
    STRATEGIC_DECISION = "strategic_decision"


@dataclass(frozen=True)
class ScanModeDefinition:
    id: ScanModeId
    label: str
    description: str
    guidance: str


SCAN_MODES: dict[ScanModeId, ScanModeDefinition] = {
    ScanModeId.BUSINESS_IDEA: ScanModeDefinition(
        id=ScanModeId.BUSINESS_IDEA,
        label="Business Idea",
        description="Stress-test the viability and execution assumptions of a business.",
        guidance=(
            "Focus on market assumptions, customer willingness to pay, "
            "differentiation, distribution, pricing, operational burden, and "
            "reasons the business may fail."
        ),
    ),
    ScanModeId.TECHNICAL_ARCHITECTURE: ScanModeDefinition(
        id=ScanModeId.TECHNICAL_ARCHITECTURE,
        label="Technical Architecture",
        description="Find structural weaknesses and failure modes in a system design.",
        guidance=(
            "Focus on system dependencies, scalability limits, resilience, "
            "integration risks, operational complexity, security weaknesses, "
            "and failure modes."
        ),
    ),
    ScanModeId.PRODUCT_FEATURE: ScanModeDefinition(
        id=ScanModeId.PRODUCT_FEATURE,
        label="Product Feature",
        description="Challenge whether a proposed feature creates durable user value.",
        guidance=(
            "Focus on user value, adoption friction, edge cases, maintenance "
            "cost, usability, false assumptions, and whether the feature solves "
            "a real problem."
        ),
    ),
    ScanModeId.SECURITY_RISK_DECISION: ScanModeDefinition(
        id=ScanModeId.SECURITY_RISK_DECISION,
        label="Security / Risk Decision",
        description="Assess exposure, controls, misuse, and consequences.",
        guidance=(
            "Focus on threat exposure, control gaps, compliance risk, "
            "operational risk, misuse cases, recovery assumptions, and blast "
            "radius."
        ),
    ),
    ScanModeId.STRATEGIC_DECISION: ScanModeDefinition(
        id=ScanModeId.STRATEGIC_DECISION,
        label="Strategic Decision",
        description="Examine the evidence, incentives, and consequences of a decision.",
        guidance=(
            "Focus on incentives, timing, opportunity cost, second-order "
            "consequences, stakeholder resistance, evidence quality, and "
            "reversibility."
        ),
    ),
}


def get_scan_mode(mode_id: str | ScanModeId) -> ScanModeDefinition:
    try:
        normalized_id = ScanModeId(str(mode_id).strip().lower())
    except ValueError as exc:
        raise ValueError(f"Unsupported scan mode: {mode_id}.") from exc
    return SCAN_MODES[normalized_id]
