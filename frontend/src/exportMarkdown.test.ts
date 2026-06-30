import { describe, expect, it } from "vitest";

import {
  buildMarkdownFilename,
  buildMarkdownReport,
} from "./exportMarkdown";
import { fakeScanResponse } from "./test/fixtures";
import type { ScanResponse } from "./types";

const exportedAt = new Date("2026-06-14T12:30:00.000Z");

describe("buildMarkdownReport", () => {
  it("includes metadata, context, models, both reports, and limitations", () => {
    const markdown = buildMarkdownReport(fakeScanResponse, exportedAt);
    const expectedHeadings = [
      "# AI Faultline Report",
      "## Metadata",
      "## Original Input",
      "## Scan Mode",
      "## Models Used",
      "## Faultline Report",
      "### Faultline Summary",
      "### Surface Claim",
      "### Hidden Assumptions",
      "### Pressure Points",
      "### Collapse Risks",
      "### Weak Evidence",
      "### What Would Break This",
      "### Validation Tests",
      "### Questions Before Commitment",
      "### Risk Level",
      "### Recommended Next Move",
      "## Second-AI Audit Review",
      "### Audit Summary",
      "### Missed Risks",
      "### Weak or Vague Findings",
      "### Validation Plan Gaps",
      "### Risk Level Challenge",
      "### Recommended Report Improvements",
      "### Auditor Confidence",
      "### Final Caution",
      "## Limitations",
    ];

    for (const heading of expectedHeadings) {
      expect(markdown).toContain(heading);
    }

    expect(markdown).toContain("Exported At: 2026-06-14T12:30:00.000Z");
    expect(markdown).toContain(fakeScanResponse.input);
    expect(markdown).toContain("Scan Mode: business_idea");
    expect(markdown).toContain("Scan Mode Label: Business Idea");
    expect(markdown).toContain("openai / gpt-4.1-mini");
    expect(markdown).toContain("gemini / gemini-2.5-flash");
    expect(markdown).toContain("Scanner Risk Level: high");
    expect(markdown).toContain("Auditor Confidence: high");
    expect(markdown).toContain("structured risk analysis support");
  });

  it("renders empty lists and unsafe values with controlled placeholders", () => {
    const result = structuredClone(fakeScanResponse) as ScanResponse;
    result.scanner_report.hidden_assumptions = [];
    result.scanner_report.faultline_summary = undefined as unknown as string;
    result.audit_report.final_caution = null as unknown as string;

    const markdown = buildMarkdownReport(result, exportedAt);

    expect(markdown).toContain("### Hidden Assumptions\n\n- No items returned.");
    expect(markdown).toContain("### Faultline Summary\n\nNot provided.");
    expect(markdown).toContain("### Final Caution\n\nNot provided.");
    expect(markdown).not.toContain("undefined");
    expect(markdown).not.toContain("null");
    expect(markdown).not.toContain("[object Object]");
  });

  it("redacts provider key assignments and key-like values", () => {
    const result = structuredClone(fakeScanResponse) as ScanResponse;
    const openAiEnvName = `${"OPENAI"}_${"API"}_${"KEY"}`;
    const geminiEnvName = `${"GEMINI"}_${"API"}_${"KEY"}`;
    const openAiKey = `${"sk"}-${"a".repeat(24)}`;
    const geminiKey = `${"AI"}${"za"}${"b".repeat(32)}`;
    result.input = `${openAiEnvName}=${openAiKey} ${geminiEnvName}=${geminiKey}`;

    const markdown = buildMarkdownReport(result, exportedAt);

    expect(markdown).toContain("[redacted provider key]");
    expect(markdown).not.toContain(openAiKey);
    expect(markdown).not.toContain(geminiKey);
    expect(markdown).not.toContain(`${openAiEnvName}=`);
    expect(markdown).not.toContain(`${geminiEnvName}=`);
  });

  it("does not generate browsing claims, citations, or source sections", () => {
    const markdown = buildMarkdownReport(fakeScanResponse, exportedAt);

    expect(markdown).toContain("does not browse the web");
    expect(markdown).not.toContain("browsed the web");
    expect(markdown).not.toContain("## Sources");
    expect(markdown).not.toContain("## Citations");
    expect(markdown).not.toMatch(/\[[0-9]+\]/);
  });
});

describe("buildMarkdownFilename", () => {
  it("creates a timestamped markdown filename with safe characters", () => {
    const filename = buildMarkdownFilename(exportedAt);

    expect(filename).toBe("ai-faultline-report-20260614-123000.md");
    expect(filename).toMatch(/^[a-z0-9-]+\.md$/);
  });
});
