# Mythadis Faultline v0.1.0 - Local Faultline MVP

## Summary

Mythadis Faultline is a local-first AI stress-testing tool for exposing hidden
assumptions, pressure points, weak evidence, and collapse risks before
committing to an idea, plan, claim, product decision, or technical design.

This first release provides a complete two-pass workflow: a Primary Scanner
produces a structured report, then a second-AI Auditor challenges that report
for missed risks, vague findings, and validation gaps.

> Find the crack before the collapse.

## What Is Included

- Local FastAPI backend
- React, TypeScript, and Vite frontend
- OpenAI provider support
- Gemini provider support
- Primary Scanner workflow
- Independent second-AI Auditor workflow
- Structured scanner report and audit review
- Safe parsing with conservative fallback reports
- Current-result rendering in browser memory
- Browser-side Markdown export
- Docker Compose and manual local setup
- Sample report and short/long demo documentation
- Architecture, prompt design, security, privacy, and contributor guidance

## What Is Intentionally Not Included

- No user accounts or authentication
- No database
- No saved report or prompt history
- No server-side prompt or result storage
- No telemetry or analytics
- No cloud sync
- No share links
- No PDF or DOCX export
- No web browsing or citation engine
- No automatic fact verification

These exclusions are part of the v0.1.0 privacy and scope boundaries, not
missing setup steps.

## Local-First Privacy Posture

The frontend and backend run locally by default. Provider keys are read only by
the backend from an ignored local `.env` file. The frontend sends provider
choices and never receives provider credentials.

Faultline does not intentionally store prompts or results on the server and
does not use `localStorage`, `sessionStorage`, IndexedDB, or cookies for report
history. There is no database, account system, telemetry, or analytics.

Local-first does not mean that scan content stays on the machine. When a scan
runs, the local backend sends the submitted content to the selected external
providers. Provider-side handling depends on the user's provider account,
settings, region, and applicable terms.

## Supported Providers

- OpenAI, default model `gpt-4.1-mini`
- Gemini, default model `gemini-2.5-flash`

The scanner and auditor providers are selected independently. Both selected
providers must be configured in the backend for a live scan.

## Scan Modes

- Business Idea
- Technical Architecture
- Product Feature
- Security / Risk Decision
- Strategic Decision

Each mode supplies focused guidance to both the scanner and auditor while
preserving the shared structured JSON contracts.

## Export Support

v0.1.0 supports Markdown export only. The report is generated in the browser
from the current in-memory result and saved only when the user manually
downloads it. There is no server-side export endpoint or saved report list.

## How to Run Locally

```bash
git clone https://github.com/blanzy-labs/ai-faultline.git
cd ai-faultline
cp .env.example .env
docker compose up --build
```

Open <http://localhost:5173> and verify the backend at
<http://localhost:8000/health>. Add provider keys to the ignored root `.env`
only when running live scans.

See [local-install.md](local-install.md) for manual backend and frontend setup.

## Validation Status

The release candidate was validated locally on June 14, 2026:

- 57 backend unit and integration tests passed with mocked providers.
- 17 frontend tests and the production build passed.
- npm reported no known dependency vulnerabilities.
- Repository security/privacy and offline release-readiness checks passed.
- Direct FastAPI startup and the health endpoint passed.
- Docker Compose rebuilt both services; frontend and backend smoke checks passed.
- Git environment-file safety checks passed.
- Tracked-source scans found no provider-key exposure, browser storage,
  database, or telemetry additions.

No automated test makes a real provider call.

## Known Limitations

- AI output may be incomplete, generic, misleading, or wrong.
- Faultline does not browse the web or verify facts.
- External providers receive submitted content when a scan runs.
- Users are responsible for provider credentials, model access, quota, cost,
  and provider account settings.
- Provider availability and data handling are outside this repository's
  control.
- The current result is lost on reload unless it is downloaded.
- Faultline provides structured risk analysis support, not legal, medical,
  financial, security, or compliance advice.
- High-stakes decisions require qualified human review.

## Release Checklist

Complete [release-checklist.md](release-checklist.md) before creating the tag or
GitHub release. In particular:

- Confirm the worktree and staged files contain no secrets.
- Run backend, frontend, security, and release checks.
- Rebuild and smoke-test Docker Compose.
- Perform the manual UI and Markdown export review.
- Perform a live provider smoke test only with approved non-sensitive input.
- Review the final diff and release notes.

## Suggested GitHub Release Text

Mythadis Faultline v0.1.0 is the Local Faultline MVP: a local-first,
two-pass AI stress-testing workflow with OpenAI and Gemini support, five scan
modes, structured scanner and auditor reports, and browser-side Markdown
export.

The release intentionally includes no login, database, prompt history,
telemetry, server-side report storage, share links, browsing, or automatic fact
verification. Submitted content is sent to the external providers selected for
each live scan.

Start with the [local installation guide](local-install.md), review the
[security and privacy guide](security.md), and use the
[sample report](sample-report.md) for a provider-free walkthrough.
