import type { ScannerReport } from "../types";
import { ReportSection } from "./ReportSection";

interface FaultlineReportProps {
  report: ScannerReport;
}

export function FaultlineReport({ report }: FaultlineReportProps) {
  return (
    <article className="report-panel report-panel--scanner">
      <header className="report-header">
        <div>
          <p className="section-kicker">Primary analysis</p>
          <h2>Faultline Report</h2>
        </div>
        <span className={`metric-badge metric-badge--${report.risk_level}`}>
          Risk: {report.risk_level}
        </span>
      </header>

      <div className="report-grid">
        <ReportSection title="Faultline Summary" text={report.faultline_summary} />
        <ReportSection title="Surface Claim" text={report.surface_claim} />
        <ReportSection
          title="Hidden Assumptions"
          items={report.hidden_assumptions}
        />
        <ReportSection title="Pressure Points" items={report.pressure_points} />
        <ReportSection
          title="Collapse Risks"
          items={report.collapse_risks}
          tone="warning"
        />
        <ReportSection title="Weak Evidence" items={report.weak_evidence} />
        <ReportSection
          title="What Would Break This"
          items={report.what_would_break_this}
          tone="warning"
        />
        <ReportSection
          title="Validation Tests"
          items={report.validation_tests}
          tone="action"
        />
        <ReportSection
          title="Questions Before Commitment"
          items={report.questions_before_commitment}
        />
        <ReportSection
          title="Recommended Next Move"
          text={report.recommended_next_move}
          tone="action"
        />
      </div>
    </article>
  );
}
