const PROGRESS_HINTS = [
  "Reading the claim...",
  "Finding hidden assumptions...",
  "Mapping pressure points...",
  "Checking collapse risks...",
  "Auditing the scanner report...",
];

export function LoadingState() {
  return (
    <section className="loading-panel" aria-live="polite" aria-busy="true">
      <div className="loading-orbit" aria-hidden="true">
        <span />
      </div>
      <div>
        <p className="section-kicker">Two-pass analysis underway</p>
        <h2>Running the faultline scan</h2>
        <ul className="progress-list">
          {PROGRESS_HINTS.map((hint) => (
            <li key={hint}>{hint}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
