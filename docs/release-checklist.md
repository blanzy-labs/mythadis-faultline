# Release Checklist - Mythadis Faultline v0.1.0

This checklist prepares `v0.1.0 - Local Faultline MVP` for a human-created
release. Run validation first. Do not tag, push, or create a GitHub release
until every applicable item is complete.

## 1. Repo Status

- [ ] Confirm the active branch is the intended release branch:

  ```bash
  git branch --show-current
  ```

- [ ] Confirm the worktree contains only intentional release changes:

  ```bash
  git status --short
  git diff --check
  git diff
  ```

- [ ] Confirm release identity is consistently `Mythadis Faultline`,
  `v0.1.0 - Local Faultline MVP`, and `Find the crack before the collapse.`

## 2. Environment Safety

- [ ] Confirm secret-bearing environment files are ignored and untracked:

  ```bash
  git ls-files .env .env.* backend/.env backend/.env.* frontend/.env frontend/.env.* || true
  git check-ignore .env backend/.env frontend/.env
  ```

- [ ] Confirm the safe example remains tracked:

  ```bash
  git ls-files .env.example
  ```

- [ ] Review staged files without opening or printing `.env`:

  ```bash
  git diff --cached --name-only
  ```

## 3. Backend Validation

- [ ] Run all backend tests:

  ```bash
  cd backend
  python -m pytest
  ```

- [ ] Start the backend directly:

  ```bash
  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

- [ ] In another terminal, verify health:

  ```bash
  curl http://localhost:8000/health
  ```

- [ ] Confirm the response includes `"status":"ok"`, then stop Uvicorn.

Use `python3` when the host does not provide a `python` command.

## 4. Frontend Validation

- [ ] Install dependencies, build, and run tests:

  ```bash
  cd frontend
  npm install
  npm run build
  npm test -- --run
  npm audit
  ```

- [ ] Confirm the production build completes and dependency findings are
  reviewed.

## 5. Docker Validation

- [ ] Rebuild from the repository root:

  ```bash
  docker compose down
  docker compose up --build
  ```

- [ ] Verify the backend:

  ```bash
  curl http://localhost:8000/health
  ```

- [ ] Open <http://localhost:5173> and confirm the frontend loads.
- [ ] Review `docker compose logs` for startup errors without publishing logs
  that could contain private host information.

### Clean Checkout Rehearsal

Perform this manually in a separate temporary directory when practical:

```bash
git clone https://github.com/blanzy-labs/mythadis-faultline.git
cd mythadis-faultline
cp .env.example .env
# Optionally add provider keys to the ignored .env.
docker compose up --build
curl http://localhost:8000/health
```

Then open <http://localhost:5173>. Do not copy the working repository's `.env`
into the clean checkout.

## 6. Security/Privacy Validation

- [ ] Run the consolidated checks:

  ```bash
  python scripts/security_checks.py
  python scripts/release_check.py
  ```

- [ ] Confirm provider keys remain backend-only.
- [ ] Confirm there is no prompt/result persistence, browser history storage,
  database, telemetry, analytics, or server-side export.
- [ ] Confirm automated tests use mocks and make no real provider calls.

## 7. Manual UI Validation

- [ ] Open <http://localhost:5173>.
- [ ] Confirm the app title and tagline.
- [ ] Confirm the input form and backend status render.
- [ ] Confirm all five scan modes are available.
- [ ] Confirm OpenAI and Gemini are available for scanner and auditor choices.
- [ ] Confirm provider helper text exposes no credentials.
- [ ] Submit empty input and confirm safe validation.
- [ ] Confirm loading and error states do not reveal provider details.

## 8. Live Provider Smoke Test

This is a manual, billable external call. Use approved fictional input and do
not automate it as part of tests or release scripts.

- [ ] Confirm the root `.env` contains only the intended provider credentials.
- [ ] Run one live scan with non-sensitive text.
- [ ] Confirm the Faultline Report renders.
- [ ] Confirm the Second-AI Audit Review renders.
- [ ] Confirm Models Used renders without credentials.
- [ ] Confirm no prompt, result, or provider response is written by the app.

## 9. Markdown Export Validation

- [ ] Download the current report as Markdown.
- [ ] Confirm it includes Metadata, Original Input, Scan Mode, Models Used,
  Faultline Report, Second-AI Audit Review, and Limitations.
- [ ] Confirm it contains no accidental missing-value text, raw object text,
  API keys, fake citations, or browsing claims.
- [ ] Confirm the file exists only because the user initiated the download.

## 10. Documentation Validation

- [ ] Review `README.md`.
- [ ] Review `docs/release-notes-v0.1.0.md`.
- [ ] Review `docs/release-checklist.md`.
- [ ] Confirm architecture, security, install, demo, prompt-design, sample
  report, and contributor docs remain linked and accurate.
- [ ] Confirm the docs explain external provider data flow honestly.
- [ ] Confirm known limitations and intentional exclusions are complete.

## 11. Final Git Checks

- [ ] Run the required source scans:

  ```bash
  grep -R "OPENAI_API_KEY\|GEMINI_API_KEY" frontend/src frontend/index.html frontend/package.json frontend/vite.config.ts || true
  grep -R "VITE_OPENAI_API_KEY\|VITE_GEMINI_API_KEY" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=dist --exclude=.env || true
  grep -R "localStorage\|sessionStorage\|indexedDB\|document.cookie" frontend/src backend/app || true
  grep -R "sqlite\|sqlite3\|sqlalchemy\|prisma\|typeorm\|mongoose\|postgres\|mysql" backend/app backend/requirements.txt frontend/package.json frontend/package-lock.json || true
  grep -R "analytics\|telemetry\|posthog\|segment\|mixpanel\|sentry\|amplitude" frontend/src backend/app frontend/package.json backend/requirements.txt || true
  grep -R "sk-\|AIza" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=dist --exclude=.env || true
  grep -R "undefined\|\[object Object\]" docs README.md frontend/src || true
  ```

- [ ] Investigate every match. Negative security statements and TypeScript
  language usage can be legitimate; rendered secret values and accidental
  report text are not.
- [ ] Run `git status --short` one final time.
- [ ] Commit the reviewed release-prep changes before tagging.

## 12. Release Commands

The current repository branch is `master`. The following commands are for the
human release owner to run only after all checks pass and the release-prep
commit is present:

```bash
git status --short
git push origin master
git tag -a v0.1.0 -m "v0.1.0 - Local Faultline MVP"
git push origin v0.1.0
```

Optionally create the GitHub release after the tag is pushed:

```bash
gh release create v0.1.0 \
  --title "v0.1.0 - Local Faultline MVP" \
  --notes-file docs/release-notes-v0.1.0.md
```

Before running these commands, verify the remote, branch, tag list, final
commit, and release notes. These commands are documentation only; release
validation must not execute them automatically.
