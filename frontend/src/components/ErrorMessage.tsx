interface ErrorMessageProps {
  message: string;
}

export function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <section className="error-panel" role="alert">
      <p className="section-kicker">Scan interrupted</p>
      <h2>Unable to complete the scan</h2>
      <p>{message}</p>
    </section>
  );
}
