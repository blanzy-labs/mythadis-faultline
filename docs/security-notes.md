# Security Notes

## Security Posture Summary

Mythadis Faultline is a local-first MVP with a deliberately small data surface.
It has no accounts, database, prompt history, telemetry, analytics, saved
reports, or server-side export endpoint. The current scan exists in application
memory only until it is replaced or the process/page ends.

This posture is an implementation boundary, not a claim that provider calls are
local. User input leaves the machine when the backend sends prompts to the
selected external AI providers.

## Secret Handling

- Keep real provider credentials only in the untracked root `.env` or another
  ignored backend environment file.
- Never commit `.env`.
- Never use `git add -f .env`.
- Keep `.env.example` limited to empty placeholders and public model defaults.
- Do not put secrets in documentation, fixtures, screenshots, logs, exceptions,
  or sample reports.
- Do not log prompts, model outputs, raw provider responses, or API keys.

## Provider Key Boundaries

The backend reads `OPENAI_API_KEY` and `GEMINI_API_KEY`. The frontend sends only
the provider IDs `openai` and `gemini`; it must not define provider-key Vite
variables or receive provider credentials in API responses.

Safe frontend configuration may include the local API base URL. It must never
include provider secrets.

## No-Storage Rule

Do not add:

- browser `localStorage`, `sessionStorage`, IndexedDB, or cookies
- backend prompt or result files
- databases, caches, queues, or report history
- automatic cloud uploads or share links

Adding prompt history, persistence, or accounts requires a separate privacy and
threat-model redesign. React component state is appropriate for the current
in-memory result.

## Browser-Side Markdown Export

Markdown export is generated from the current in-memory response in the
browser. The app creates a temporary `Blob` URL, triggers the user-requested
download, and revokes the URL. There is no backend export endpoint and no report
is saved unless the user downloads it.

Export code must continue to avoid raw objects, missing-value artifacts, key
values, invented citations, and browsing claims.

## Provider Data Flow

1. The user enters text in the browser.
2. The frontend sends the text, scan mode, and provider IDs to the local
   FastAPI backend.
3. The backend creates scanner and auditor prompts.
4. The backend sends those prompts to the configured external providers.
5. The structured response returns to the browser and remains in memory.

Provider-side data handling is governed by the selected provider and configured
account. Contributors must not imply that a provider-backed scan stays entirely
on the local machine.

## Dependency Hygiene

- Keep Python and npm dependencies minimal.
- Review dependency changes before release.
- Avoid heavy frameworks unless they solve a demonstrated need.
- Do not add analytics, telemetry, advertising, or session-recording packages.
- Do not add database, ORM, cache, or persistence packages without an explicit
  architecture and privacy decision.
- Run package audit commands where available and review findings in context.

## Recommended Local Checks

From the repository root:

```bash
python scripts/security_checks.py
```

Backend:

```bash
cd backend
python -m pytest
```

Frontend:

```bash
cd frontend
npm run build
npm test -- --run
npm audit
```

Before release, also inspect `git status --short` and confirm only
`.env.example`, never a secret-bearing environment file, is tracked.

## What Not To Add Without A Design Decision

Do not add any of the following as incidental implementation details:

- prompt or report history
- databases or durable caches
- telemetry or analytics
- authentication or user profiles
- public report URLs or share links
- server-side exports
- prompt, response, or provider-error logging

Each would change the privacy, retention, operational, or abuse model and needs
explicit scope, threat modeling, and documentation.

## Known Limitations

- Provider calls may transmit user input to external services.
- Provider behavior, retention, and training policies are outside this
  repository's control.
- Local malware, browser extensions, terminal history, downloaded files, and
  host-level logging are outside the app's guarantees.
- The security checker catches common accidental regressions; it is not a full
  static analyzer, dependency scanner, or secret-scanning service.
- AI output can be incomplete or wrong and requires qualified human review for
  high-stakes decisions.
