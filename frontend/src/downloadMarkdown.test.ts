import { afterEach, describe, expect, it, vi } from "vitest";

import { downloadMarkdownReport } from "./downloadMarkdown";
import { fakeScanResponse } from "./test/fixtures";

describe("downloadMarkdownReport", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("creates, clicks, and revokes a temporary object URL", () => {
    const createObjectURL = vi.fn().mockReturnValue("blob:test-report");
    const revokeObjectURL = vi.fn();
    const click = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => undefined);
    vi.stubGlobal("URL", { createObjectURL, revokeObjectURL });

    downloadMarkdownReport(
      fakeScanResponse,
      new Date("2026-06-14T12:30:00.000Z"),
    );

    expect(createObjectURL).toHaveBeenCalledWith(expect.any(Blob));
    expect(click).toHaveBeenCalledOnce();
    expect(revokeObjectURL).toHaveBeenCalledWith("blob:test-report");
    expect(document.querySelector('a[download$=".md"]')).not.toBeInTheDocument();
  });
});
