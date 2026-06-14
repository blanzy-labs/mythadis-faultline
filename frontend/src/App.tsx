import { useEffect, useState } from "react";

import { checkBackendHealth, runFaultlineScan, ScanApiError } from "./api";
import { AuditReview } from "./components/AuditReview";
import { ErrorMessage } from "./components/ErrorMessage";
import { FaultlineReport } from "./components/FaultlineReport";
import { LoadingState } from "./components/LoadingState";
import { ModelsUsed } from "./components/ModelsUsed";
import { ScanForm } from "./components/ScanForm";
import type { ScanRequest, ScanResponse } from "./types";

type BackendState = "checking" | "online" | "offline";

function App() {
  const [backendState, setBackendState] =
    useState<BackendState>("checking");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [result, setResult] = useState<ScanResponse | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function updateBackendState() {
      const isOnline = await checkBackendHealth(controller.signal);
      if (!controller.signal.aborted) {
        setBackendState(isOnline ? "online" : "offline");
      }
    }

    void updateBackendState();
    return () => controller.abort();
  }, []);

  async function handleScan(request: ScanRequest) {
    setIsLoading(true);
    setErrorMessage("");
    setResult(null);

    try {
      setResult(await runFaultlineScan(request));
    } catch (error) {
      setErrorMessage(
        error instanceof ScanApiError
          ? error.message
          : "Something went wrong while running the scan. Please try again.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="site-header">
        <div className="brand-lockup">
          <span className="brand-mark" aria-hidden="true">
            MF
          </span>
          <div>
            <p className="eyebrow">Mythadis Labs / App 03</p>
            <p className="brand-name">Faultline</p>
          </div>
        </div>
        <div className="backend-status" aria-live="polite">
          <span
            className={`status-light status-light--${backendState}`}
            aria-hidden="true"
          />
          {backendState === "checking" && "Checking backend"}
          {backendState === "online" && "Backend online"}
          {backendState === "offline" && "Backend unavailable"}
        </div>
      </header>

      <section className="hero" aria-labelledby="page-title">
        <div className="hero-copy">
          <p className="hero-index">Faultline analysis / two-pass review</p>
          <h1 id="page-title">Mythadis Faultline</h1>
          <p className="tagline">Find the crack before the collapse.</p>
          <p className="positioning">
            Expose hidden assumptions, pressure points, weak evidence, and
            collapse risks before committing to an idea, plan, claim, product
            decision, or technical design.
          </p>
        </div>
        <div className="hero-signal" aria-hidden="true">
          <span>01</span>
          <div />
          <span>SCAN</span>
          <div />
          <span>02</span>
          <div />
          <span>AUDIT</span>
        </div>
      </section>

      <section className="workspace" aria-label="Faultline scan workspace">
        <div className="panel-heading">
          <div>
            <p className="section-kicker">New analysis</p>
            <h2>Stress-test before you commit</h2>
          </div>
          <p>
            Your input is sent to the selected backend providers for this scan
            only. Faultline does not add browser-side history or storage.
          </p>
        </div>
        <ScanForm isLoading={isLoading} onSubmit={handleScan} />
      </section>

      <div className="feedback-area">
        {isLoading && <LoadingState />}
        {errorMessage && <ErrorMessage message={errorMessage} />}
      </div>

      {result && (
        <section className="results-area" aria-label="Faultline scan results">
          <FaultlineReport report={result.scanner_report} />
          <AuditReview report={result.audit_report} />
          <ModelsUsed models={result.models_used} />
        </section>
      )}

      <footer className="site-footer">
        <span>Structured risk analysis, not guaranteed truth.</span>
        <span>Local-first / no accounts / no stored history</span>
      </footer>
    </main>
  );
}

export default App;
