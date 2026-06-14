# Mythadis Faultline Architecture

## Overview

Mythadis Faultline is a local-first, two-pass AI stress-testing application.
The React frontend collects an idea, plan, claim, product decision, or
technical design. The FastAPI backend sends it through a Primary Scanner and
then an Independent Auditor, returning one structured report to the browser.

The app is practical decision support. It does not browse the web, verify
facts, create citations, or guarantee that its findings are complete or
correct.

## System Goals

- Expose hidden assumptions, weak evidence, pressure points, and collapse risks.
- Separate the first analysis from an independent second-pass challenge.
- Return predictable JSON that the UI can render safely.
- Keep provider credentials in the backend.
- Keep the current result in memory and make export an explicit user action.
- Remain easy to run locally with Docker Compose or standard development tools.

## Non-Goals

The `v0.1.0` MVP does not provide accounts, authentication, a database, prompt
history, analytics, telemetry, browsing, citations, saved reports, share
links, or server-side export. It does not use browser storage or cookies.

## High-Level Architecture

```text
User input
  -> React frontend
  -> FastAPI backend
  -> selected Primary Scanner provider
  -> scanner JSON parsed and validated
  -> selected Auditor provider
  -> auditor JSON parsed and validated
  -> structured response returned to frontend
  -> current in-memory result rendered
  -> optional browser-side Markdown download
```

The browser sends provider names such as `openai` and `gemini`, never
credentials. The backend reads credentials from the local environment.

## Frontend Architecture

The frontend lives in `frontend/src` and uses React, TypeScript, and Vite.

- `App.tsx` owns backend status, loading, error, and current-result state.
- `components/ScanForm.tsx` collects the input, scan mode, and two providers.
- `api.ts` calls `/health` and `/faultline/run` and validates response shapes.
- Report components render scanner findings, the audit, and model metadata.
- `exportMarkdown.ts` builds a Markdown document from the current response.
- `downloadMarkdown.ts` creates and revokes the temporary browser download URL.

State is intentionally ephemeral. The frontend does not use `localStorage`,
`sessionStorage`, IndexedDB, or cookies for prompts or results.

## Backend Architecture

The backend lives in `backend/app` and uses FastAPI.

- `main.py` configures CORS, mounts the Faultline router, and exposes `/health`.
- `config.py` reads provider keys and model names from the root or backend
  `.env`.
- `faultline/routes.py` validates HTTP requests and maps safe provider errors to
  HTTP responses.
- `faultline/service.py` coordinates the scanner and auditor in sequence.
- `faultline/modes.py` defines the supported scan modes and their guidance.
- `faultline/prompts.py` builds the two provider prompts.
- `faultline/parser.py` extracts, validates, or safely replaces malformed JSON.
- `faultline/schemas.py` defines the request and response contracts.

The backend does not intentionally write prompts or results to disk.

## Provider Layer

`backend/app/providers` contains a small provider abstraction:

- `base.py` defines the async `generate` contract.
- `factory.py` resolves a provider name to an adapter.
- `openai_provider.py` and `gemini_provider.py` make provider calls.
- `errors.py` defines sanitized configuration and provider-call errors.

Adapters receive settings from the backend. Provider keys are not included in
the API response, frontend configuration, or normal error messages. Automated
tests replace providers with mocks and do not make real provider calls.

## Faultline Workflow

1. The frontend submits the input, scan mode, scanner provider, and auditor
   provider to `POST /faultline/run`.
2. FastAPI validates the request with `ScanRequest`.
3. The service builds the mode-specific scanner prompt.
4. The selected scanner provider returns text.
5. The parser extracts and validates the scanner JSON. Invalid output becomes a
   conservative fallback report.
6. The service builds an auditor prompt containing the original input, scan
   mode, and parsed scanner report.
7. The selected auditor provider returns text.
8. The parser validates the auditor JSON or supplies its conservative fallback.
9. FastAPI returns the input, both reports, and non-secret model metadata.
10. React renders that response as the current in-memory result.

The auditor still runs when scanner output requires a fallback, so the response
contract remains complete.

## Prompt Design Relationship

Prompt roles, mode guidance, safety constraints, and output contracts are
documented in [prompt-design.md](prompt-design.md). Prompt changes must remain
coordinated with schemas, parsers, tests, and frontend types. The scanner and
auditor should remain distinct rather than becoming one self-review prompt.

## JSON Contracts

The backend uses Pydantic models for `ScanRequest`, `ScannerReport`,
`AuditReport`, `ModelsUsed`, and `ScanResponse`. The frontend mirrors those
shapes in TypeScript and checks an unknown response before rendering it.

Field names and constrained values are part of the application contract.
Changing them requires coordinated backend, frontend, test, sample-report, and
prompt documentation updates.

## Markdown Export Flow

Export is entirely browser-side:

1. The user selects **Download Markdown** for the current result.
2. The frontend formats the structured response and adds limitations.
3. Export formatting redacts provider-key assignments and common key-shaped
   values.
4. The browser creates a temporary `Blob` URL and starts a download.
5. The temporary URL is revoked.

There is no backend export endpoint. A report is saved only when the user
chooses to download it.

## Security and Privacy Boundaries

- Provider keys remain backend-only and local environment files are ignored by
  Git.
- User input is sent to the selected external providers when a scan runs.
- Provider data handling depends on the user's provider account and settings.
- Neither application layer intentionally stores prompt or result history.
- The frontend stores only the current React state for the active page.
- The project contains no telemetry, analytics, database, or authentication.

See [security.md](security.md) for user-facing guidance and
[security-notes.md](security-notes.md) for contributor rules.

## Local Development Flow

Docker Compose starts the backend on port `8000` and the Vite frontend on port
`5173`. Manual development uses a Python virtual environment for the backend
and npm for the frontend. Both modes use the same API and environment
boundaries. See [local-install.md](local-install.md) for exact commands.

## Testing Strategy

- Backend tests cover health, configuration, providers, schemas, prompts,
  parsing, orchestration, routes, documentation, and security checks.
- Provider behavior is mocked; tests must never consume real provider quota.
- Frontend tests cover form behavior, API errors, rendering, and Markdown
  export.
- The frontend production build catches TypeScript and bundling regressions.
- `scripts/security_checks.py` checks environment safety, forbidden storage and
  dependency patterns, obvious key-shaped values, and required documentation.
- Docker and direct startup checks validate the two supported run paths.

## Known Limitations

- Output quality depends on the submitted input and selected models.
- Models can miss risks, overstate confidence, or return generic advice.
- The auditor can repeat the scanner instead of independently challenging it.
- The app has no external fact source and cannot establish whether a claim is
  current or true.
- Provider availability, cost, retention, and policy are outside the app's
  control.
- In-memory state is lost when the page reloads or another scan replaces it.

## Future Scope Boundaries

Persistence, accounts, collaboration, share links, telemetry, additional
exports, browsing, citations, and hosted deployment would change the privacy,
security, and operational model. They require explicit future design work and
must not be introduced as incidental changes to this MVP.
