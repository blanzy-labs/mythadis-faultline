import { useMemo, useState, type FormEvent } from "react";

import { SCAN_MODES } from "../scanModes";
import type { ProviderId, ScanModeId, ScanRequest } from "../types";

const MAX_INPUT_LENGTH = 12000;

interface ScanFormProps {
  isLoading: boolean;
  onSubmit: (request: ScanRequest) => void;
}

export function ScanForm({ isLoading, onSubmit }: ScanFormProps) {
  const [input, setInput] = useState("");
  const [scanMode, setScanMode] = useState<ScanModeId>("business_idea");
  const [scannerProvider, setScannerProvider] =
    useState<ProviderId>("openai");
  const [auditorProvider, setAuditorProvider] =
    useState<ProviderId>("gemini");
  const [validationMessage, setValidationMessage] = useState("");

  const selectedMode = useMemo(
    () => SCAN_MODES.find((mode) => mode.id === scanMode) ?? SCAN_MODES[0],
    [scanMode],
  );
  const isInputValid =
    input.trim().length > 0 && input.length <= MAX_INPUT_LENGTH;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!input.trim()) {
      setValidationMessage("Please enter something to stress-test.");
      return;
    }
    if (input.length > MAX_INPUT_LENGTH) {
      setValidationMessage(
        "The input is too long. Please shorten it and try again.",
      );
      return;
    }

    setValidationMessage("");
    onSubmit({
      input: input.trim(),
      scan_mode: scanMode,
      scanner_provider: scannerProvider,
      auditor_provider: auditorProvider,
    });
  }

  return (
    <form className="scan-form" onSubmit={handleSubmit}>
      <div className="field-group">
        <div className="field-heading">
          <label htmlFor="scan-input">
            Idea, plan, claim, decision, or design to stress-test
          </label>
          <span className="character-count">
            {input.length.toLocaleString()} / {MAX_INPUT_LENGTH.toLocaleString()}
          </span>
        </div>
        <textarea
          id="scan-input"
          name="input"
          rows={9}
          maxLength={MAX_INPUT_LENGTH}
          value={input}
          disabled={isLoading}
          aria-describedby="input-help input-error"
          onChange={(event) => {
            setInput(event.target.value);
            if (validationMessage) {
              setValidationMessage("");
            }
          }}
          placeholder="Example: We are considering launching a local-first AI risk review tool for small businesses. It will run without accounts, avoid storing prompts, and rely on backend-configured providers."
        />
        <p id="input-help" className="field-help">
          Be specific about the intended outcome, assumptions, constraints, and
          evidence you already have.
        </p>
        {validationMessage && (
          <p id="input-error" className="field-error" role="alert">
            {validationMessage}
          </p>
        )}
      </div>

      <div className="control-grid">
        <div className="field-group">
          <label htmlFor="scan-mode">Scan mode</label>
          <select
            id="scan-mode"
            value={scanMode}
            disabled={isLoading}
            onChange={(event) =>
              setScanMode(event.target.value as ScanModeId)
            }
          >
            {SCAN_MODES.map((mode) => (
              <option key={mode.id} value={mode.id}>
                {mode.label}
              </option>
            ))}
          </select>
          <p className="field-help">{selectedMode.description}</p>
        </div>

        <div className="provider-grid">
          <ProviderSelect
            id="scanner-provider"
            label="Primary Scanner"
            value={scannerProvider}
            disabled={isLoading}
            onChange={setScannerProvider}
          />
          <ProviderSelect
            id="auditor-provider"
            label="Auditor"
            value={auditorProvider}
            disabled={isLoading}
            onChange={setAuditorProvider}
          />
        </div>
      </div>

      <p className="provider-note">
        Provider keys stay backend-side in your local .env file. The frontend
        only sends provider choices.
      </p>

      <button
        className="run-button"
        type="submit"
        disabled={!isInputValid || isLoading}
      >
        {isLoading ? "Scan in progress..." : "Run Faultline Scan"}
      </button>
    </form>
  );
}

interface ProviderSelectProps {
  id: string;
  label: string;
  value: ProviderId;
  disabled: boolean;
  onChange: (value: ProviderId) => void;
}

function ProviderSelect({
  id,
  label,
  value,
  disabled,
  onChange,
}: ProviderSelectProps) {
  return (
    <div className="field-group">
      <label htmlFor={id}>{label} provider</label>
      <select
        id={id}
        value={value}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value as ProviderId)}
      >
        <option value="openai">OpenAI</option>
        <option value="gemini">Gemini</option>
      </select>
    </div>
  );
}
