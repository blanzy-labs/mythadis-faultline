# Mythadis Faultline

> **Find the crack before the collapse.**

Mythadis Faultline is a local-first analysis tool for exposing hidden
assumptions, pressure points, weak evidence, and collapse risks before
committing to an idea, plan, claim, product decision, or technical design.

This repository currently contains the `v0.1.0` Local Faultline MVP foundation:
a FastAPI health endpoint, a React/Vite application shell, environment
configuration, Docker Compose orchestration, and backend-only OpenAI and Gemini
provider adapters. It also includes the two-step Faultline scanner and auditor
workflow behind a structured backend API.

## MVP boundaries

The project has these non-negotiable exclusions:

- No login
- No database
- No prompt history
- No telemetry or analytics
- No server-side prompt or result storage
- No `localStorage` or `sessionStorage`
- No provider calls during startup or health checks
- No saved report history
- No server-side export

## Architecture

- **Backend:** Python and FastAPI, with async OpenAI and Gemini adapters
- **Frontend:** React, TypeScript, and Vite
- **Local orchestration:** Docker Compose
- **Secrets:** OpenAI and Gemini keys remain backend-only

The frontend receives only `VITE_API_BASE_URL`. Provider API keys must never be
added to frontend environment variables or source code.

## Privacy and Security

Mythadis Faultline is designed as a local-first MVP. It has no login or
accounts, no database, no prompt history, no telemetry or analytics, and no
intentional server-side prompt or report storage. The browser application does
not use `localStorage`, `sessionStorage`, IndexedDB, or cookies.

Provider API keys are read only by the backend from your local `.env` file. The
frontend sends provider choices such as `openai` or `gemini`; it never receives
OpenAI or Gemini API keys.

When you run a scan, the submitted input travels from the browser to your local
FastAPI backend. The backend builds the scanner and auditor prompts and sends
them to the external providers you selected. Provider-side retention, training,
and other data handling depend on the provider, account, and settings you
configure. Do not submit sensitive data unless you are comfortable sending it
to those providers.

Markdown export is generated entirely in the browser from the current in-memory
result. Faultline saves a report only when you manually download the Markdown
file.

## Faultline API

`POST /faultline/run` accepts:

```json
{
  "input": "A plan, claim, decision, or design to stress-test",
  "scan_mode": "business_idea",
  "scanner_provider": "openai",
  "auditor_provider": "gemini"
}
```

Supported scan modes are `business_idea`, `technical_architecture`,
`product_feature`, `security_risk_decision`, and `strategic_decision`.
Provider calls happen only when this endpoint is invoked. Inputs, prompts, and
results are neither logged nor stored by the application.

## Docker setup

1. Create a local environment file:

   ```bash
   cp .env.example .env
   ```

2. Provider keys are optional for startup and `/health`. Add one only when
   exercising its provider adapter:

   ```env
   OPENAI_API_KEY=your-key
   GEMINI_API_KEY=your-key
   ```

   Keep unused keys empty.

3. Start both applications:

   ```bash
   docker compose up --build
   ```

The frontend is available at <http://localhost:5173> and the backend health
endpoint at <http://localhost:8000/health>.

## Manual development

Run the backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

In another terminal, run the frontend:

```bash
cd frontend
npm install
npm run dev
```

By default, the frontend calls `http://localhost:8000`. To use another backend,
set `VITE_API_BASE_URL` in `frontend/.env`; do not put provider keys there.

## Validation

Backend tests:

```bash
cd backend
python -m pytest
```

Frontend build:

```bash
cd frontend
npm install
npm run build
```

Service checks:

```bash
docker compose up --build
curl http://localhost:8000/health
```

Security checks:

```bash
python scripts/security_checks.py
grep -R "OPENAI_API_KEY\|GEMINI_API_KEY" frontend/src frontend/index.html frontend/package.json || true
grep -R "localStorage\|sessionStorage" frontend/src backend/app || true
```
