import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App";
import { SCAN_MODES } from "./scanModes";
import { fakeScanResponse } from "./test/fixtures";

function response(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

describe("App", () => {
  beforeEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders the title, form, all scan modes, and provider selectors", () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(response({ status: "ok" })),
    );

    render(<App />);

    expect(
      screen.getByRole("heading", { name: "Mythadis Faultline" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Find the crack before the collapse."),
    ).toBeInTheDocument();
    expect(
      screen.getByLabelText(
        "Idea, plan, claim, decision, or design to stress-test",
      ),
    ).toHaveAttribute("maxlength", "12000");

    const modeSelect = screen.getByLabelText("Scan mode");
    expect(within(modeSelect).getAllByRole("option")).toHaveLength(5);
    for (const mode of SCAN_MODES) {
      expect(
        within(modeSelect).getByRole("option", { name: mode.label }),
      ).toBeInTheDocument();
    }

    expect(screen.getByLabelText("Primary Scanner provider")).toHaveValue(
      "openai",
    );
    expect(screen.getByLabelText("Auditor provider")).toHaveValue("gemini");
    expect(
      screen.getByRole("button", { name: "Run Faultline Scan" }),
    ).toBeDisabled();
    expect(
      screen.queryByRole("button", { name: "Download Markdown Report" }),
    ).not.toBeInTheDocument();
  });

  it("sends selected values and disables controls while loading", async () => {
    const user = userEvent.setup();
    let resolveScan: ((value: Response) => void) | undefined;
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(response({ status: "ok" }))
      .mockImplementationOnce(
        () =>
          new Promise<Response>((resolve) => {
            resolveScan = resolve;
          }),
      );
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await user.type(
      screen.getByLabelText(
        "Idea, plan, claim, decision, or design to stress-test",
      ),
      "A technical architecture proposal",
    );
    await user.selectOptions(
      screen.getByLabelText("Scan mode"),
      "technical_architecture",
    );
    await user.selectOptions(
      screen.getByLabelText("Primary Scanner provider"),
      "gemini",
    );
    await user.selectOptions(
      screen.getByLabelText("Auditor provider"),
      "openai",
    );
    await user.click(
      screen.getByRole("button", { name: "Run Faultline Scan" }),
    );

    expect(
      screen.getByRole("heading", { name: "Running the faultline scan" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Scan mode")).toBeDisabled();
    expect(
      screen.getByRole("button", { name: "Scan in progress..." }),
    ).toBeDisabled();

    const request = JSON.parse(
      String(fetchMock.mock.calls[1][1]?.body),
    ) as Record<string, string>;
    expect(request).toMatchObject({
      input: "A technical architecture proposal",
      scan_mode: "technical_architecture",
      scanner_provider: "gemini",
      auditor_provider: "openai",
    });

    resolveScan?.(response(fakeScanResponse));
    expect(
      await screen.findByRole("heading", { name: "Faultline Report" }),
    ).toBeInTheDocument();
  });

  it("renders scanner, audit, models, and empty-list placeholders", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(response({ status: "ok" }))
        .mockResolvedValueOnce(response(fakeScanResponse)),
    );
    render(<App />);

    await user.type(
      screen.getByLabelText(
        "Idea, plan, claim, decision, or design to stress-test",
      ),
      "Launch a focused local-first product",
    );
    await user.click(
      screen.getByRole("button", { name: "Run Faultline Scan" }),
    );

    expect(
      await screen.findByRole("heading", { name: "Faultline Report" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Second-AI Audit Review" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Risk: high")).toBeInTheDocument();
    expect(screen.getByText("Confidence: high")).toBeInTheDocument();
    expect(screen.getByText("OpenAI / gpt-4.1-mini")).toBeInTheDocument();
    expect(screen.getByText("Gemini / gemini-2.5-flash")).toBeInTheDocument();
    expect(screen.getByText("No items returned.")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Validation Tests" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Download Markdown Report" }),
    ).toBeInTheDocument();
  });

  it("downloads the current result as Markdown in the browser", async () => {
    const user = userEvent.setup();
    const createObjectURL = vi.fn().mockReturnValue("blob:current-report");
    const revokeObjectURL = vi.fn();
    const anchorClick = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => undefined);
    vi.stubGlobal("URL", { createObjectURL, revokeObjectURL });
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(response({ status: "ok" }))
        .mockResolvedValueOnce(response(fakeScanResponse)),
    );
    render(<App />);

    await user.type(
      screen.getByLabelText(
        "Idea, plan, claim, decision, or design to stress-test",
      ),
      "Launch a focused local-first product",
    );
    await user.click(
      screen.getByRole("button", { name: "Run Faultline Scan" }),
    );
    await user.click(
      await screen.findByRole("button", {
        name: "Download Markdown Report",
      }),
    );

    expect(createObjectURL).toHaveBeenCalledWith(expect.any(Blob));
    expect(anchorClick).toHaveBeenCalledOnce();
    expect(revokeObjectURL).toHaveBeenCalledWith("blob:current-report");
  });

  it("shows a safe backend unavailable error", async () => {
    const user = userEvent.setup();
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(response({ status: "ok" }))
        .mockRejectedValueOnce(new Error("private network detail")),
    );
    render(<App />);

    await user.type(
      screen.getByLabelText(
        "Idea, plan, claim, decision, or design to stress-test",
      ),
      "A product idea",
    );
    await user.click(
      screen.getByRole("button", { name: "Run Faultline Scan" }),
    );

    expect(
      await screen.findByText(
        "The backend is unavailable. Make sure the FastAPI service is running.",
      ),
    ).toBeInTheDocument();
    expect(screen.queryByText("private network detail")).not.toBeInTheDocument();
  });
});
