# Local Installation

## Prerequisites

- Git
- Docker Desktop or Docker Engine with Docker Compose
- Python 3.12 or newer for manual backend development
- Node.js 22 and npm for manual frontend development
- An OpenAI and/or Gemini provider key for real scans

Provider keys are optional for startup, `/health`, builds, and automated tests.

## Clone the Repo

```bash
git clone https://github.com/blanzy-labs/ai-faultline.git
cd ai-faultline
```

## Configure `.env`

Create the ignored local environment file from the tracked example:

```bash
cp .env.example .env
```

The file should keep this shape:

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_MODEL=gemini-2.5-flash
```

Add only the keys for providers you intend to use. Never commit `.env`, force
add it, paste it into an issue, or expose it on screen.

## Run with Docker Compose

From the repository root:

```bash
docker compose up --build
```

Open <http://localhost:5173>. The backend listens on
<http://localhost:8000>.

Stop the stack with `Ctrl+C`, or run this from another terminal:

```bash
docker compose down
```

## Run Backend Manually

From the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

If your system does not provide a `python` command, use `python3` in the same
commands.

On Windows Command Prompt, activate the environment with:

```bat
.venv\Scripts\activate
```

The backend reads the root `.env` automatically.

## Run Frontend Manually

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://localhost:8000`. To use another backend, set
only `VITE_API_BASE_URL` in an ignored `frontend/.env`. Provider keys must not
be placed in frontend environment files.

## Verify Backend Health

```bash
curl http://localhost:8000/health
```

The response should include:

```json
{"status":"ok","app":"mythadis-faultline"}
```

Health checks do not call an AI provider or require provider keys.

## Run a Faultline Scan

1. Open <http://localhost:5173>.
2. Enter a non-sensitive idea, plan, claim, or design.
3. Select a scan mode.
4. Select the Primary Scanner and Independent Auditor providers.
5. Run the scan.
6. Review both report sections and optionally download the Markdown report.

A real scan requires valid backend credentials for both selected providers.
The scanner and auditor may use the same provider.

## Run Tests

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

Automated tests use mocks and do not make real provider calls.

## Run Security Checks

From the repository root:

```bash
python scripts/security_checks.py
```

Also inspect staged files before every commit:

```bash
git status --short
git diff --cached
```

## Troubleshooting

**Docker is not running**

Start Docker Desktop or the Docker service, then retry `docker compose up
--build`.

**Port 8000 or 5173 is already in use**

Stop the process or container using the port, or adjust the local port mapping
and frontend API base URL together.

**`.env` is missing**

Run `cp .env.example .env`. Startup and health still work without keys, but
real scans do not.

**A provider key is missing**

Add the credential to the backend-readable root `.env`, restart the backend,
and select a configured provider.

**The frontend says the backend is unavailable**

Confirm the backend is running, `curl http://localhost:8000/health` succeeds,
and `VITE_API_BASE_URL` points to the correct origin.

**A provider call failed**

Check provider availability, account access, quota, billing, network access,
and the configured model. Faultline intentionally returns a sanitized error
rather than raw provider details.

**A model name is invalid**

Restore the defaults from `.env.example` or use a model available to the
configured provider account, then restart the backend.

**npm install or build fails**

Use Node.js 22, remove only generated local dependencies if needed, run `npm
install`, and read the first reported TypeScript or package error.

**The Python virtual environment fails**

Confirm `python --version`, recreate `backend/.venv`, reactivate it, and install
`backend/requirements.txt` again.

## Common Mistakes

- Running manual backend commands outside `backend`.
- Putting provider keys in `frontend/.env` or a `VITE_` variable.
- Expecting `/health` to validate provider credentials.
- Treating AI findings as verified facts.
- Submitting confidential data without reviewing provider handling.
- Assuming a result persists after reload without downloading it.
- Accidentally staging `.env`. If that happens, run `git restore --staged .env`
  and confirm it remains ignored.
