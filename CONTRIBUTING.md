# Contributing to AI Faultline

Thank you for helping improve AI Faultline. Keep changes focused,
testable, and consistent with the local-first MVP.

## Project Scope

Faultline is a two-pass AI stress-testing tool. The current release focuses on
structured scanner and auditor reports, backend-only provider access, and
browser-side Markdown export.

The MVP intentionally has no login, accounts, database, prompt history,
telemetry, analytics, server-side storage, share links, browsing, or citation
engine.

## Local Setup

Follow [docs/local-install.md](docs/local-install.md). In short:

```bash
cp .env.example .env
docker compose up --build
```

Provider keys are needed only for real scans. Do not commit .env. Do not use
`git add -f .env`.

## Development Workflow

1. Create a focused branch.
2. Read the relevant code, tests, and documentation before changing behavior.
3. Keep implementation within the issue's scope.
4. Add or update focused tests.
5. Run backend, frontend, and security checks.
6. Review `git diff` and staged files for secrets or unrelated changes.
7. Explain behavior and contract changes clearly in the pull request.

## Test Commands

Backend:

```bash
cd backend
python -m pytest
```

Frontend:

```bash
cd frontend
npm install
npm run build
npm test -- --run
```

Automated tests must not call real providers or consume provider quota. Keep
provider tests mocked.

## Security Checks

From the repository root:

```bash
python scripts/security_checks.py
```

Also inspect:

```bash
git status --short
git diff --cached
```

Never put provider keys in frontend code, frontend environment variables,
fixtures, screenshots, logs, errors, documentation, or issue reports. Do not
add frontend provider-key `VITE_` variables.

Do not log prompts, provider responses, model outputs, or API keys.

## Prompt Design Rules

- Keep the Primary Scanner and Independent Auditor roles distinct.
- Preserve mode-specific guidance and explicit safety limitations.
- Do not add browsing, factual-verification, or citation claims.
- Require structured JSON and conservative handling of malformed output.
- Use fictional or sanitized examples in tests and documentation.
- Update [docs/prompt-design.md](docs/prompt-design.md) when prompt behavior
  changes.

## JSON Contract Rules

Do not change scanner, auditor, request, or response contracts casually. A
contract change must update backend schemas, prompts, parsers, route tests,
frontend types and validation, rendering, export, fixtures, and documentation
together.

Treat field renames, required values, enum changes, and fallback behavior as
user-facing API changes.

## Privacy Rules

- Keep provider keys backend-only.
- Keep docs honest that scan content is sent to selected external providers.
- Do not add prompt or result storage without an explicit future design
  decision.
- Do not add login or accounts without an explicit future design decision.
- Do not add telemetry or analytics without an explicit future design decision.
- Do not add database, cache, or persistence dependencies without an explicit
  future design decision.
- Do not add `localStorage`, `sessionStorage`, IndexedDB, or cookies for prompt
  or result history.
- Keep Markdown export browser-side unless a separate design explicitly changes
  the retention and privacy model.

## No-Overbuilding Rules

Keep the MVP local-first. Do not introduce adjacent features such as PDF or
DOCX export, public share links, collaboration, hosted accounts, report
history, browsing, citations, or background processing as incidental changes.

When a proposal changes data retention, identity, external data flow, or
deployment assumptions, open a design discussion before implementation.

## Pull Request Checklist

- [ ] Backend tests pass
- [ ] Frontend build passes
- [ ] Frontend tests pass, if configured
- [ ] Security checks pass
- [ ] No `.env` or secrets committed
- [ ] No frontend API key references added
- [ ] No localStorage/sessionStorage/database/telemetry added
- [ ] JSON contracts unchanged or intentionally documented
- [ ] Docs updated if behavior changed
- [ ] Provider calls remain mocked in automated tests
- [ ] The change stays within the agreed issue scope
