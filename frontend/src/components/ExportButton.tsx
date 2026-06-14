import { downloadMarkdownReport } from "../downloadMarkdown";
import type { ScanResponse } from "../types";

interface ExportButtonProps {
  result: ScanResponse;
}

export function ExportButton({ result }: ExportButtonProps) {
  return (
    <button
      className="export-button"
      type="button"
      onClick={() => downloadMarkdownReport(result)}
    >
      Download Markdown Report
    </button>
  );
}
