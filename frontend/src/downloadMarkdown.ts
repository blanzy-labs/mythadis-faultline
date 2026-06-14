import { buildMarkdownFilename, buildMarkdownReport } from "./exportMarkdown";
import type { ScanResponse } from "./types";

export function downloadMarkdownReport(
  result: ScanResponse,
  exportedAt: Date = new Date(),
): void {
  const content = buildMarkdownReport(result, exportedAt);
  const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
  const objectUrl = URL.createObjectURL(blob);
  const anchor = document.createElement("a");

  anchor.href = objectUrl;
  anchor.download = buildMarkdownFilename(exportedAt);
  anchor.style.display = "none";
  document.body.appendChild(anchor);

  try {
    anchor.click();
  } finally {
    anchor.remove();
    URL.revokeObjectURL(objectUrl);
  }
}
