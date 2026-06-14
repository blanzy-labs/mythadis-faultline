interface ReportSectionProps {
  title: string;
  text?: string;
  items?: string[];
  tone?: "default" | "warning" | "action";
}

export function ReportSection({
  title,
  text,
  items,
  tone = "default",
}: ReportSectionProps) {
  return (
    <section className={`report-section report-section--${tone}`}>
      <h3>{title}</h3>
      {text !== undefined && <p>{text}</p>}
      {items !== undefined &&
        (items.length > 0 ? (
          <ul>
            {items.map((item, index) => (
              <li key={`${title}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="empty-state">No items returned.</p>
        ))}
    </section>
  );
}
