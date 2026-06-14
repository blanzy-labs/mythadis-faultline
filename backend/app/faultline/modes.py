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
    scanner_guidance: str
    auditor_guidance: str


SCAN_MODES: dict[ScanModeId, ScanModeDefinition] = {
    ScanModeId.BUSINESS_IDEA: ScanModeDefinition(
        id=ScanModeId.BUSINESS_IDEA,
        label="Business Idea",
        description="Stress-test the viability and execution assumptions of a business.",
        scanner_guidance=(
            "Focus on market assumptions, customer pain, willingness to pay, "
            "buyer clarity, pricing, differentiation, competition, distribution, "
            "sales friction, operating burden, margin risk, and reasons the "
            "business may fail."
        ),
        auditor_guidance=(
            "Challenge whether a real buyer is defined, willingness to pay is "
            "actually tested, the distribution path is credible, founder effort "
            "can scale, and competition or substitutes were understated."
        ),
    ),
    ScanModeId.TECHNICAL_ARCHITECTURE: ScanModeDefinition(
        id=ScanModeId.TECHNICAL_ARCHITECTURE,
        label="Technical Architecture",
        description="Find structural weaknesses and failure modes in a system design.",
        scanner_guidance=(
            "Focus on system dependencies, scaling limits, resilience assumptions, "
            "single points of failure, data flow risk, integration risk, "
            "operational complexity, recovery assumptions, security weaknesses, "
            "observability gaps, and failure modes."
        ),
        auditor_guidance=(
            "Challenge hidden coupling, unclear ownership boundaries, untested "
            "failover assumptions, missing rollback paths, underestimated "
            "operational burden, weak security assumptions, and vague resilience "
            "claims."
        ),
    ),
    ScanModeId.PRODUCT_FEATURE: ScanModeDefinition(
        id=ScanModeId.PRODUCT_FEATURE,
        label="Product Feature",
        description="Challenge whether a proposed feature creates durable user value.",
        scanner_guidance=(
            "Focus on user value, adoption friction, usability risk, edge cases, "
            "maintenance cost, workflow fit, whether the feature solves a real "
            "problem, whether it adds complexity without value, and false "
            "assumptions about user behavior."
        ),
        auditor_guidance=(
            "Challenge whether the feature is actually needed, a simpler solution "
            "exists, it creates long-term support burden, users will understand "
            "or adopt it, and important edge cases were ignored."
        ),
    ),
    ScanModeId.SECURITY_RISK_DECISION: ScanModeDefinition(
        id=ScanModeId.SECURITY_RISK_DECISION,
        label="Security / Risk Decision",
        description="Assess exposure, controls, misuse, and consequences.",
        scanner_guidance=(
            "Focus on threat exposure, control gaps, compliance risk, operational "
            "risk, misuse cases, blast radius, recovery assumptions, identity and "
            "access risk, logging and monitoring gaps, residual risk, and the "
            "quality of risk acceptance."
        ),
        auditor_guidance=(
            "Challenge whether the threat model is explicit, compensating controls "
            "are credible, blast radius is understated, monitoring and recovery "
            "are sufficient, compliance language hides operational weakness, and "
            "risk acceptance is justified."
        ),
    ),
    ScanModeId.STRATEGIC_DECISION: ScanModeDefinition(
        id=ScanModeId.STRATEGIC_DECISION,
        label="Strategic Decision",
        description="Examine the evidence, incentives, and consequences of a decision.",
        scanner_guidance=(
            "Focus on incentives, timing, opportunity cost, reversibility, "
            "stakeholder resistance, second-order consequences, dependency risk, "
            "evidence quality, downside risk, execution risk, and decision lock-in."
        ),
        auditor_guidance=(
            "Challenge whether the decision is reversible, timing assumptions are "
            "valid, stakeholder incentives are aligned, opportunity cost is "
            "understated, second-order effects are ignored, and the evidence is "
            "strong enough to commit."
        ),
    ),
}


def get_scan_mode(mode_id: str | ScanModeId) -> ScanModeDefinition:
    try:
        normalized_id = ScanModeId(str(mode_id).strip().lower())
    except ValueError as exc:
        raise ValueError(f"Unsupported scan mode: {mode_id}.") from exc
    return SCAN_MODES[normalized_id]
