import type { ScanModeOption } from "./types";

export const SCAN_MODES: ScanModeOption[] = [
  {
    id: "business_idea",
    label: "Business Idea",
    description:
      "Market assumptions, buyer clarity, pricing, differentiation, distribution, operating burden, and reasons the business may fail.",
  },
  {
    id: "technical_architecture",
    label: "Technical Architecture",
    description:
      "Dependencies, scaling limits, resilience assumptions, single points of failure, integration risk, security weaknesses, and failure modes.",
  },
  {
    id: "product_feature",
    label: "Product Feature",
    description:
      "User value, adoption friction, usability risk, edge cases, maintenance cost, workflow fit, and whether the feature solves a real problem.",
  },
  {
    id: "security_risk_decision",
    label: "Security / Risk Decision",
    description:
      "Threat exposure, control gaps, compliance risk, operational risk, misuse cases, blast radius, recovery assumptions, and residual risk.",
  },
  {
    id: "strategic_decision",
    label: "Strategic Decision",
    description:
      "Incentives, timing, opportunity cost, reversibility, stakeholder resistance, second-order consequences, evidence quality, and execution risk.",
  },
];
