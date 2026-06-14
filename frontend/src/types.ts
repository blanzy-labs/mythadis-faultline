export type ScanModeId =
  | "business_idea"
  | "technical_architecture"
  | "product_feature"
  | "security_risk_decision"
  | "strategic_decision";

export type ProviderId = "openai" | "gemini";

export type RiskLevel = "low" | "medium" | "high" | "critical";
export type AuditorConfidence = "low" | "medium" | "high";

export interface ScanRequest {
  input: string;
  scan_mode: ScanModeId;
  scanner_provider: ProviderId;
  auditor_provider: ProviderId;
}

export interface ScannerReport {
  faultline_summary: string;
  surface_claim: string;
  hidden_assumptions: string[];
  pressure_points: string[];
  collapse_risks: string[];
  weak_evidence: string[];
  what_would_break_this: string[];
  validation_tests: string[];
  questions_before_commitment: string[];
  risk_level: RiskLevel;
  recommended_next_move: string;
}

export interface AuditReport {
  audit_summary: string;
  missed_risks: string[];
  weak_or_vague_findings: string[];
  validation_plan_gaps: string[];
  risk_level_challenge: string;
  recommended_report_improvements: string[];
  auditor_confidence: AuditorConfidence;
  final_caution: string;
}

export interface ModelsUsed {
  scanner_provider: ProviderId;
  scanner_model: string;
  auditor_provider: ProviderId;
  auditor_model: string;
}

export interface ScanResponse {
  input: string;
  scan_mode: ScanModeId;
  scanner_report: ScannerReport;
  audit_report: AuditReport;
  models_used: ModelsUsed;
}

export interface ScanModeOption {
  id: ScanModeId;
  label: string;
  description: string;
}
