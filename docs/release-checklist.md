# Release Checklist

Use this checklist before creating a release for AI Faultline.

## Preflight

- [ ] Confirm working tree is clean.
- [ ] Confirm branch is `main`, or document why branch standardization was skipped.
- [ ] Confirm canonical repo name is `ai-faultline`.
- [ ] Confirm display name is AI Faultline.
- [ ] Confirm GitHub auth is the expected `blanzy-labs` account.
- [ ] Confirm no `.env` file is staged or committed.
- [ ] Confirm no secrets or real API keys are staged.
- [ ] Confirm `.env` is ignored.
- [ ] Confirm `docs/disclaimer.md` exists and is linked from README.
- [ ] Confirm `docs/security-and-privacy.md` exists and is linked from README.
- [ ] Confirm GitHub metadata is updated.

## Version

- [ ] Confirm target version: `v0.1.1`.
- [ ] Confirm release title: `v0.1.1 - Blanzy Labs Standardization Patch`.
- [ ] Confirm target version.
- [ ] Confirm release title follows `vX.Y.Z - <Release Name>`.
- [ ] Confirm no existing tag or release would be overwritten.
- [ ] Confirm no tags will be moved.

## Validation

- [ ] Run backend tests:

```bash
cd backend
python -m pytest
```

- [ ] Run frontend build:

```bash
cd frontend
npm run build
```

- [ ] Run frontend tests:

```bash
cd frontend
npm test -- --run
```

- [ ] Run security checks:

```bash
python scripts/security_checks.py
python scripts/release_check.py
```

- [ ] Run Docker validation:

```bash
docker compose build
```

- [ ] Run Docker smoke test if practical:

```bash
docker compose up -d
curl http://localhost:8000/health
docker compose down
```

## Safety

- [ ] No force push.
- [ ] No history rewrite.
- [ ] No tag movement.
- [ ] No release overwrite.
- [ ] No secrets printed in logs or copied into release notes.
