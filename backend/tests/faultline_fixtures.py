import json

SCANNER_PAYLOAD = {
    "faultline_summary": (
        "The plan depends on unvalidated demand and fragile execution assumptions."
    ),
    "surface_claim": "This idea can succeed if launched quickly.",
    "hidden_assumptions": [
        "Customers have a painful enough problem to switch.",
        "The team can reach buyers cheaply.",
        "The product can be delivered without heavy support burden.",
    ],
    "pressure_points": [
        "Customer acquisition cost may exceed early revenue.",
        "The value proposition may be too broad.",
        "Operational effort may scale faster than income.",
    ],
    "collapse_risks": [
        "No clear buying audience emerges.",
        "The product is easy to copy.",
        "Delivery requires more manual work than expected.",
    ],
    "weak_evidence": [
        "No direct customer interviews are cited.",
        "No pricing test has been run.",
        "No competitor comparison is provided.",
    ],
    "what_would_break_this": [
        "Customers will not pay.",
        "Competitors solve the problem well enough.",
        "The product cannot be delivered profitably.",
    ],
    "validation_tests": [
        "Run 10 customer interviews.",
        "Create a paid-intent landing page.",
        "Manually deliver the service to 3 pilot users.",
    ],
    "questions_before_commitment": [
        "Who is the exact first buyer?",
        "What painful event triggers purchase?",
        "What evidence shows people will pay now?",
    ],
    "risk_level": "high",
    "recommended_next_move": "Run a paid-intent test before building.",
}

AUDITOR_PAYLOAD = {
    "audit_summary": (
        "The scanner underplayed distribution and founder capacity risk."
    ),
    "missed_risks": [
        "The founder may not have enough time to sell and build.",
        "The sales cycle may be longer than the runway.",
        "The target buyer may not trust a new entrant.",
    ],
    "weak_or_vague_findings": [
        "The acquisition channel assumption is not specific.",
        "Profitable delivery is not defined.",
    ],
    "validation_plan_gaps": [
        "Willingness to pay is not tested strongly enough.",
        "There is no competitor displacement test.",
    ],
    "risk_level_challenge": (
        "High is appropriate, but critical may be justified."
    ),
    "recommended_report_improvements": [
        "Add a first customer profile.",
        "Add a channel-specific acquisition test.",
        "Add a minimum price threshold.",
    ],
    "auditor_confidence": "high",
    "final_caution": "Do not build until a buyer shows paid intent.",
}

SCANNER_JSON = json.dumps(SCANNER_PAYLOAD)
AUDITOR_JSON = json.dumps(AUDITOR_PAYLOAD)
