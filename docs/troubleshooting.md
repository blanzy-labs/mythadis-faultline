# Troubleshooting

## Docker Is Not Running

Start Docker Desktop or Docker Engine, then retry:

```bash
docker compose up --build
```

## Port 8000 Or 5173 Is Already In Use

The app expects:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

Stop the process or container using the conflicting port, or adjust the local port mapping and frontend API base URL together.

## `.env` Is Missing

Create the ignored local environment file:

```bash
cp .env.example .env
```

Startup and `/health` work without provider keys. Real scans require credentials for the selected providers.

## Provider Key Is Missing

Add credentials only to the backend-readable root `.env`:

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
```

Do not commit `.env`, paste keys into issues, or put provider keys in frontend env files.

## Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok","app":"mythadis-faultline"}
```

The `app` value is a legacy internal service identifier and is not the public display name.

## Frontend Says Backend Is Unavailable

Confirm:

- backend is running
- `curl http://localhost:8000/health` succeeds
- `VITE_API_BASE_URL` points to the backend if you changed the default
- Docker Compose or local dev commands are using matching ports

## Provider Call Failed

Check:

- selected provider is supported
- provider key exists in root `.env`
- account has quota/billing enabled
- model name is available to the provider account
- network access is available

AI Faultline returns sanitized provider errors rather than raw provider details.

## Build Or Test Failure

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
```

Frontend:

```bash
cd frontend
npm install
npm run build
npm test -- --run
```

## Reporting Issues

When reporting an issue, include:

- app version
- operating system
- setup method
- command that failed
- sanitized error output

Do not include API keys, `.env` contents, private prompts, client data, or sensitive logs.
