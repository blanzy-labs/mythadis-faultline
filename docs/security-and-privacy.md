# Security And Privacy

AI Faultline is designed as a local-first Blanzy Labs AI app.

This is the standard security and privacy entry point. Additional detailed notes are retained in [docs/security.md](security.md), and contributor rules are retained in [docs/security-notes.md](security-notes.md).

## Local-First Design

- The app is intended to run on the user's machine or controlled local environment.
- No hosted service is provided by default.
- Local configuration uses `.env`, copied from `.env.example`.

## Telemetry

No telemetry, analytics, or tracking is implemented in V1.

## Persistence

No database, user accounts, prompt history, result history, browser storage, or server-side report storage is implemented in V1.

Markdown export is generated locally in the browser from the result currently displayed on screen.

## Environment Files

- `.env` is ignored by git.
- `.env.example` contains safe placeholders only.
- Do not commit real API keys, tokens, secrets, credentials, private prompts, or sensitive user data.

## API Keys

- Provider API keys stay server-side in the backend/root `.env`.
- The frontend must never receive OpenAI, Gemini, or other provider secrets.
- Do not paste secrets into prompts, uploaded content, issues, logs, screenshots, or exported reports.

## Provider Calls

Provider calls occur only when the app is configured for a provider and the user runs a faultline scan.

When a provider is used, the provider may receive user inputs, generated intermediate outputs, prompt instructions, selected model/provider metadata, and other configured request content. Provider terms and privacy policies apply.

Supported providers in V1:

- OpenAI
- Gemini

## Public Internet Exposure

AI Faultline is not hardened for public internet exposure. Do not deploy it publicly without reviewing authentication, authorization, rate limiting, logging, secret handling, network exposure, provider usage, and compliance requirements.

## Disclaimer

See [docs/disclaimer.md](disclaimer.md). Users are responsible for their own usage, costs, data, decisions, and outcomes.
