import type { AuditReport } from "../types";
import { ReportSection } from "./ReportSection";

interface AuditReviewProps {
  report: AuditReport;
}

export function AuditReview({ report }: AuditReviewProps) {
  return (
    <article className="report-panel report-panel--audit">
      <header className="report-header">
        <div>
          <p className="section-kicker">Independent challenge layer</p>
          <h2>Second-AI Audit Review</h2>
          <p className="report-intro">
            The auditor challenges the scanner report for missed risks, vague
            findings, and weak validation logic.
          </p>
        </div>
        <span
          className={`metric-badge metric-badge--confidence-${report.auditor_confidence}`}
        >
          Confidence: {report.auditor_confidence}
        </span>
      </header>

      <div className="report-grid">
        <ReportSection title="Audit Summary" text={report.audit_summary} />
        <ReportSection title="Missed Risks" items={report.missed_risks} />
        <ReportSection
          title="Weak or Vague Findings"
          items={report.weak_or_vague_findings}
        />
        <ReportSection
          title="Validation Plan Gaps"
          items={report.validation_plan_gaps}
        />
        <ReportSection
          title="Risk Level Challenge"
          text={report.risk_level_challenge}
          tone="warning"
        />
        <ReportSection
          title="Recommended Report Improvements"
          items={report.recommended_report_improvements}
          tone="action"
        />
        <ReportSection
          title="Final Caution"
          text={report.final_caution}
          tone="warning"
        />
      </div>
    </article>
  );
}
