# AI Faultline

AI Faultline is a local-first Blanzy Labs AI app for surfacing disagreement, assumptions, risks, and fault lines in AI-generated analysis.

Tagline: Find the crack before the collapse.

Current release: `v0.1.1 - Blanzy Labs Standardization Patch`

Original MVP release: `v0.1.0 - Local Faultline MVP`

AI Faultline is part of the Blanzy Labs AI app family.

## What It Does

- Stress-tests an idea, plan, claim, product decision, or technical design.
- Runs a Primary Scanner pass and an Independent Auditor pass.
- Surfaces hidden assumptions, pressure points, weak evidence, collapse risks, validation tests, and follow-up questions.
- Exports the visible result as a local Markdown report in the browser.

## Current Scope

- Local-first FastAPI backend and React/Vite frontend.
- OpenAI and Gemini provider support.
- Five scan modes: business idea, technical architecture, product feature, security risk decision, and strategic decision.
- Backend-only provider keys loaded from the ignored local `.env`.
- Docker Compose support.
- No login, database, prompt history, telemetry, analytics, browser storage, saved report history, or server-side export.

## Out Of Scope

- Hosted or production deployment.
- User accounts, authentication, collaboration, or share links.
- Database persistence, report history, or background jobs.
- Voice features.
- Hidden web browsing, factual verification, or citation generation.
- Professional legal, financial, medical, security, compliance, or safety advice.

## Roadmap

- v0.1.1: Blanzy Labs naming, docs, metadata, branch, and release-readiness cleanup.
- v0.2.x: validation polish, docs normalization, and focused app improvements.
- Future provider, export, or deployment changes only where explicitly planned.

## Architecture

- Backend: FastAPI
- Frontend: React, Vite, TypeScript
- Providers: OpenAI and Gemini
- Runtime: local development or Docker Compose

See [docs/architecture.md](docs/architecture.md).

## Local Setup

```bash
git clone https://github.com/blanzy-labs/ai-faultline.git
cd ai-faultline
cp .env.example .env
```

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run build
npm test -- --run
npm run dev
```

Open:

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/health`

See [docs/local-install.md](docs/local-install.md).

## Docker Setup

```bash
cp .env.example .env
# edit .env with backend provider keys if needed
docker compose up --build
docker compose down
```

Docker Compose loads `.env` for the backend service. The frontend receives only non-secret configuration.

## Environment Variables

Root `.env` values:

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_MODEL=gemini-2.5-flash
```

Provider keys go only in the backend/root `.env`. Do not put OpenAI, Gemini, or other provider keys in frontend env files. `.env` is ignored by git; `.env.example` contains placeholders only and is safe to commit.

## Testing

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
```

Security checks:

```bash
python scripts/security_checks.py
python scripts/release_check.py
```

Docker:

```bash
docker compose build
```

## Usage Workflow

1. Start the backend and frontend with Docker Compose or local development commands.
2. Add provider keys to the ignored `.env` file if you want to run real scans.
3. Open `http://localhost:5173`.
4. Enter non-sensitive text to stress-test.
5. Choose a scan mode.
6. Choose providers for the Primary Scanner and Independent Auditor.
7. Run the scan.
8. Review the report, audit review, model metadata, and limitations.
9. Export Markdown locally if needed.

## API Summary

- `GET /health`: returns backend status.
- `POST /faultline/run`: runs the two-pass faultline scan.

The frontend calls only the local backend. Provider API keys remain backend-only.

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md).

## Security And Privacy

See [docs/security-and-privacy.md](docs/security-and-privacy.md).

Short version:

- API keys are backend-only.
- User inputs and generated report content are sent to configured providers when a scan runs.
- No prompt/result storage is implemented in V1.
- Markdown export is generated locally in the browser.
- Avoid submitting sensitive or private data unless you are comfortable sending it to the configured providers.

## Documentation

- [Architecture](docs/architecture.md)
- [Security and privacy](docs/security-and-privacy.md)
- [Security notes](docs/security.md)
- [Contributor security notes](docs/security-notes.md)
- [Local installation](docs/local-install.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Demo script](docs/demo-script.md)
- [Prompt design](docs/prompt-design.md)
- [Sample report](docs/sample-report.md)
- [Release checklist](docs/release-checklist.md)
- [Release notes](docs/release-notes/v0.1.1.md)
- [Validation notes](docs/validation/v0.1.1-validation.md)
- [Disclaimer](docs/disclaimer.md)
- [Contributing](CONTRIBUTING.md)

## License

See [LICENSE](LICENSE).

## Disclaimer

See [docs/disclaimer.md](docs/disclaimer.md).
