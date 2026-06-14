import { beforeEach, describe, expect, it, vi } from "vitest";

import { runFaultlineScan, ScanApiError } from "./api";
import { fakeScanResponse } from "./test/fixtures";
import type { ScanRequest } from "./types";

const request: ScanRequest = {
  input: "A technical design",
  scan_mode: "technical_architecture",
  scanner_provider: "gemini",
  auditor_provider: "openai",
};

describe("runFaultlineScan", () => {
  beforeEach(() => {
    vi.unstubAllGlobals();
  });

  it("posts the selected input, mode, and providers", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(fakeScanResponse), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const response = await runFaultlineScan(request);

    expect(response).toEqual(fakeScanResponse);
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/faultline/run",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(request),
      }),
    );
  });

  it("maps a provider failure to a safe message", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(
          new Response("private provider detail", { status: 502 }),
        ),
    );

    await expect(runFaultlineScan(request)).rejects.toMatchObject({
      kind: "provider-failure",
      message: "The provider call failed. Try again or switch providers.",
    });
  });

  it("maps missing provider configuration to a backend-side setup message", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("private detail", { status: 400 })),
    );

    await expect(runFaultlineScan(request)).rejects.toMatchObject({
      kind: "provider-config",
      message:
        "The selected provider is not configured. Check your backend .env file.",
    });
  });

  it("maps request validation failures without exposing backend detail", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("private detail", { status: 422 })),
    );

    await expect(runFaultlineScan(request)).rejects.toMatchObject({
      kind: "invalid-request",
      message:
        "The backend rejected the request. Check the selected scan mode and providers.",
    });
  });

  it("maps a network failure to a backend unavailable message", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("ECONNREFUSED")));

    await expect(runFaultlineScan(request)).rejects.toEqual(
      new ScanApiError(
        "The backend is unavailable. Make sure the FastAPI service is running.",
        "backend-unavailable",
      ),
    );
  });

  it("rejects an unexpected response shape safely", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ scanner_report: {} }), { status: 200 }),
      ),
    );

    await expect(runFaultlineScan(request)).rejects.toMatchObject({
      kind: "unexpected-response",
    });
  });
});
