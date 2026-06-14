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
- No frontend scan form yet
- No Markdown export yet

## Architecture

- **Backend:** Python and FastAPI, with async OpenAI and Gemini adapters
- **Frontend:** React, TypeScript, and Vite
- **Local orchestration:** Docker Compose
- **Secrets:** OpenAI and Gemini keys remain backend-only

The frontend receives only `VITE_BACKEND_URL`. Provider API keys must never be
added to frontend environment variables or source code.

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
grep -R "OPENAI_API_KEY\|GEMINI_API_KEY" frontend/src frontend/index.html frontend/package.json || true
grep -R "localStorage\|sessionStorage" frontend/src backend/app || true
```
