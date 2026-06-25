from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from app.faultline.modes import ScanModeId


class ProviderName(StrEnum):
    OPENAI = "openai"
    GEMINI = "gemini"
    OPENAI_COMPATIBLE = "openai_compatible"


class ScanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input: Annotated[str, StringConstraints(max_length=12000)]
    scan_mode: ScanModeId
    scanner_provider: ProviderName
    auditor_provider: ProviderName

    @field_validator("input")
    @classmethod
    def validate_input(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Input must not be empty.")
        return stripped

    @field_validator("scanner_provider", "auditor_provider", mode="before")
    @classmethod
    def normalize_provider(cls, value: object) -> object:
        return value.strip().lower() if isinstance(value, str) else value


class ScannerReport(BaseModel):
    model_config = ConfigDict(extra="ignore")

    faultline_summary: str = (
        "The scanner response did not include a faultline summary."
    )
    surface_claim: str = "The scanner response did not include a surface claim."
    hidden_assumptions: list[str] = Field(default_factory=list)
    pressure_points: list[str] = Field(default_factory=list)
    collapse_risks: list[str] = Field(default_factory=list)
    weak_evidence: list[str] = Field(default_factory=list)
    what_would_break_this: list[str] = Field(default_factory=list)
    validation_tests: list[str] = Field(default_factory=list)
    questions_before_commitment: list[str] = Field(default_factory=list)
    risk_level: Literal["low", "medium", "high", "critical"] = "high"
    recommended_next_move: str = (
        "Review the available findings before making a commitment."
    )


class AuditReport(BaseModel):
    model_config = ConfigDict(extra="ignore")

    audit_summary: str = "The auditor response did not include an audit summary."
    missed_risks: list[str] = Field(default_factory=list)
    weak_or_vague_findings: list[str] = Field(default_factory=list)
    validation_plan_gaps: list[str] = Field(default_factory=list)
    risk_level_challenge: str = (
        "The auditor did not provide a risk level challenge."
    )
    recommended_report_improvements: list[str] = Field(default_factory=list)
    auditor_confidence: Literal["low", "medium", "high"] = "low"
    final_caution: str = "Treat this audit cautiously until it can be reviewed."


class ModelsUsed(BaseModel):
    scanner_provider: ProviderName
    scanner_model: str
    auditor_provider: ProviderName
    auditor_model: str


class ScanResponse(BaseModel):
    input: str
    scan_mode: ScanModeId
    scanner_report: ScannerReport
    audit_report: AuditReport
    models_used: ModelsUsed
