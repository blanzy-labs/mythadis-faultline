import { useEffect, useState } from "react";

type BackendState =
  | { kind: "checking"; message: string }
  | { kind: "online"; message: string }
  | { kind: "offline"; message: string };

const backendUrl = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000";

function App() {
  const [backendState, setBackendState] = useState<BackendState>({
    kind: "checking",
    message: "Checking backend connection...",
  });

  useEffect(() => {
    const controller = new AbortController();

    async function checkBackend() {
      try {
        const response = await fetch(`${backendUrl}/health`, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`Health check returned ${response.status}`);
        }

        const health = (await response.json()) as { status?: string };
        if (health.status !== "ok") {
          throw new Error("Unexpected health response");
        }

        setBackendState({
          kind: "online",
          message: "Backend online",
        });
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }

        setBackendState({
          kind: "offline",
          message: "Backend unavailable. Start the API and try again.",
        });
      }
    }

    void checkBackend();
    return () => controller.abort();
  }, []);

  return (
    <main className="app-shell">
      <section className="hero" aria-labelledby="page-title">
        <p className="eyebrow">Mythadis Labs / App 03</p>
        <h1 id="page-title">Mythadis Faultline</h1>
        <p className="tagline">Find the crack before the collapse.</p>
        <p className="positioning">
          Expose hidden assumptions, pressure points, weak evidence, and collapse
          risks before committing to an idea, plan, claim, product decision, or
          technical design.
        </p>

        <div className="status-panel" aria-live="polite">
          <div>
            <p className="status-label">System link</p>
            <p className="status-message">{backendState.message}</p>
          </div>
          <span
            className={`status-light status-light--${backendState.kind}`}
            aria-hidden="true"
          />
        </div>
      </section>
    </main>
  );
}

export default App;
