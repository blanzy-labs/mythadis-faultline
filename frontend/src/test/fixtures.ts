import type { ScanResponse } from "../types";

export const fakeScanResponse: ScanResponse = {
  input: "Launch a focused local-first product",
  scan_mode: "business_idea",
  scanner_report: {
    faultline_summary:
      "The plan depends on unvalidated demand and fragile distribution assumptions.",
    surface_claim: "A local-first product can win with a focused launch.",
    hidden_assumptions: [
      "Buyers care enough about local-first operation to switch.",
    ],
    pressure_points: ["The first acquisition channel is not proven."],
    collapse_risks: ["No clear buying audience emerges."],
    weak_evidence: [],
    what_would_break_this: ["Prospects will not pay the minimum viable price."],
    validation_tests: ["Run ten buyer interviews and a paid-intent test."],
    questions_before_commitment: ["Who is the exact first buyer?"],
    risk_level: "high",
    recommended_next_move: "Test paid intent before building the full product.",
  },
  audit_report: {
    audit_summary:
      "The scanner found demand risk but underplayed founder capacity.",
    missed_risks: ["The founder may not be able to sell and build at once."],
    weak_or_vague_findings: ["The acquisition channel needs a specific test."],
    validation_plan_gaps: ["The plan lacks a competitor displacement test."],
    risk_level_challenge: "High is appropriate but still weakly evidenced.",
    recommended_report_improvements: ["Define the first customer profile."],
    auditor_confidence: "high",
    final_caution: "Do not build until a buyer demonstrates paid intent.",
  },
  models_used: {
    scanner_provider: "openai",
    scanner_model: "gpt-4.1-mini",
    auditor_provider: "gemini",
    auditor_model: "gemini-2.5-flash",
  },
};
