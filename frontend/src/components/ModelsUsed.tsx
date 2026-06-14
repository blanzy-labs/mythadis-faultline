import type { ModelsUsed as ModelsUsedType, ProviderId } from "../types";

interface ModelsUsedProps {
  models: ModelsUsedType;
}

export function ModelsUsed({ models }: ModelsUsedProps) {
  return (
    <section className="models-panel">
      <p className="section-kicker">Models used</p>
      <div className="models-grid">
        <ModelLine
          role="Primary Scanner"
          provider={models.scanner_provider}
          model={models.scanner_model}
        />
        <ModelLine
          role="Auditor"
          provider={models.auditor_provider}
          model={models.auditor_model}
        />
      </div>
    </section>
  );
}

function ModelLine({
  role,
  provider,
  model,
}: {
  role: string;
  provider: ProviderId;
  model: string;
}) {
  const providerLabel = provider === "openai" ? "OpenAI" : "Gemini";

  return (
    <p>
      <strong>{role}</strong>
      <span>
        {providerLabel} / {model}
      </span>
    </p>
  );
}
