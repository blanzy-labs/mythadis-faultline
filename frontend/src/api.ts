import type { ScanRequest, ScanResponse } from "./types";

const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL ??
  import.meta.env.VITE_BACKEND_URL ??
  "http://localhost:8000";

export class ScanApiError extends Error {
  constructor(
    message: string,
    public readonly kind:
      | "invalid-request"
      | "provider-config"
      | "provider-failure"
      | "backend-unavailable"
      | "unexpected-response",
  ) {
    super(message);
  }
}

export async function runFaultlineScan(
  request: ScanRequest,
): Promise<ScanResponse> {
  let response: Response;

  try {
    response = await fetch(`${apiBaseUrl}/faultline/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
  } catch {
    throw new ScanApiError(
      "The backend is unavailable. Make sure the FastAPI service is running.",
      "backend-unavailable",
    );
  }

  if (!response.ok) {
    if (response.status === 400) {
      throw new ScanApiError(
        "The selected provider is not configured. Check your backend .env file.",
        "provider-config",
      );
    }
    if (response.status === 422) {
      throw new ScanApiError(
        "The backend rejected the request. Check the selected scan mode and providers.",
        "invalid-request",
      );
    }
    if (response.status === 502) {
      throw new ScanApiError(
        "The provider call failed. Try again or switch providers.",
        "provider-failure",
      );
    }
    throw new ScanApiError(
      "Something went wrong while running the scan. Please try again.",
      "unexpected-response",
    );
  }

  try {
    const payload: unknown = await response.json();
    if (!isScanResponse(payload)) {
      throw new Error("Invalid response shape");
    }
    return payload;
  } catch {
    throw new ScanApiError(
      "Something went wrong while running the scan. Please try again.",
      "unexpected-response",
    );
  }
}

export async function checkBackendHealth(signal?: AbortSignal): Promise<boolean> {
  try {
    const response = await fetch(`${apiBaseUrl}/health`, { signal });
    if (!response.ok) {
      return false;
    }
    const payload = (await response.json()) as { status?: unknown };
    return payload.status === "ok";
  } catch {
    return false;
  }
}

function isScanResponse(value: unknown): value is ScanResponse {
  if (!isRecord(value)) {
    return false;
  }

  return (
    typeof value.input === "string" &&
    isScanMode(value.scan_mode) &&
    isScannerReport(value.scanner_report) &&
    isAuditReport(value.audit_report) &&
    isModelsUsed(value.models_used)
  );
}

function isScannerReport(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.faultline_summary === "string" &&
    typeof value.surface_claim === "string" &&
    isStringArray(value.hidden_assumptions) &&
    isStringArray(value.pressure_points) &&
    isStringArray(value.collapse_risks) &&
    isStringArray(value.weak_evidence) &&
    isStringArray(value.what_would_break_this) &&
    isStringArray(value.validation_tests) &&
    isStringArray(value.questions_before_commitment) &&
    ["low", "medium", "high", "critical"].includes(
      String(value.risk_level),
    ) &&
    typeof value.recommended_next_move === "string"
  );
}

function isAuditReport(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.audit_summary === "string" &&
    isStringArray(value.missed_risks) &&
    isStringArray(value.weak_or_vague_findings) &&
    isStringArray(value.validation_plan_gaps) &&
    typeof value.risk_level_challenge === "string" &&
    isStringArray(value.recommended_report_improvements) &&
    ["low", "medium", "high"].includes(String(value.auditor_confidence)) &&
    typeof value.final_caution === "string"
  );
}

function isModelsUsed(value: unknown): boolean {
  return (
    isRecord(value) &&
    isProvider(value.scanner_provider) &&
    typeof value.scanner_model === "string" &&
    isProvider(value.auditor_provider) &&
    typeof value.auditor_model === "string"
  );
}

function isScanMode(value: unknown): boolean {
  return [
    "business_idea",
    "technical_architecture",
    "product_feature",
    "security_risk_decision",
    "strategic_decision",
  ].includes(String(value));
}

function isProvider(value: unknown): boolean {
  return value === "openai" || value === "gemini";
}

function isStringArray(value: unknown): boolean {
  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
