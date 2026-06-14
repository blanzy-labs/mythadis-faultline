from pathlib import Path


def test_prompt_design_document_contains_required_sections() -> None:
    document_path = (
        Path(__file__).resolve().parents[2] / "docs" / "prompt-design.md"
    )
    content = document_path.read_text(encoding="utf-8")

    required_phrases = [
        "Primary Faultline Scanner",
        "Independent Faultline Auditor",
        "business_idea",
        "technical_architecture",
        "product_feature",
        "security_risk_decision",
        "strategic_decision",
        "scanner JSON",
        "auditor JSON",
        "does not browse",
        "does not guarantee truth",
    ]

    for phrase in required_phrases:
        assert phrase in content
