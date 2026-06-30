# Security and Privacy

## Security Posture Summary

AI Faultline is a local-first MVP with a deliberately small data surface.
It has no login, database, prompt history, telemetry, or analytics. It does not
intentionally store prompts or results on the server.

This page is retained as detailed security notes. The standard security and
privacy entry point is [docs/security-and-privacy.md](security-and-privacy.md).

Local-first does not mean provider calls stay on your computer. When you run a
scan, the backend sends your input to the external AI providers you select.

## Local-First Design

The frontend and backend run on your machine by default. The browser keeps only
the current result in React memory. Faultline does not use `localStorage`,
`sessionStorage`, IndexedDB, or cookies for prompt or result history.

Closing or reloading the page removes the current browser state. Starting a new
scan replaces the current result.

## Provider Key Handling

OpenAI and Gemini credentials are backend-only. The backend reads them from
your local `.env`; that file is ignored by Git. The frontend sends only
provider choices such as `openai` or `gemini` and never needs to receive the
keys.

Do not put provider credentials in frontend source, Vite variables,
screenshots, issue reports, logs, or documentation.

## Data Flow During a Scan

1. You enter text and select a scan mode and providers in the browser.
2. The frontend sends the request to the FastAPI backend running locally.
3. The backend sends the scanner prompt to the selected external provider.
4. The backend sends the scanner report and original input to the selected
   auditor provider.
5. The backend returns the structured result to the browser.
6. The browser renders the current result in memory.

## What the App Does Not Store

Faultline has no account records, database, saved report list, prompt history,
or analytics events. The backend does not intentionally write prompts,
provider responses, or reports to files.

Your operating system, browser extensions, terminal, network, downloaded
files, provider, or hosting environment may have their own logging or
retention. Those systems are outside Faultline's guarantees.

## Markdown Export Behavior

Markdown exports are created in the browser from the current in-memory result.
The app creates a temporary download URL and removes it after starting the
download. A report is saved only when you manually download it, and the
downloaded file is then your responsibility.

## External Provider Warning

Provider-side retention, training, monitoring, and other handling depend on
the provider, account, region, and settings you configure. Review the terms and
controls that apply to your account before running scans.

## What Users Should Avoid Submitting

Do not submit sensitive, confidential, regulated, security-critical, or
proprietary data unless you are comfortable sending it to both selected
providers. Remove personal data, credentials, customer records, unreleased
business information, and private source material where possible.

## Limitations

Faultline does not browse the web, verify facts, create authoritative
citations, or produce guaranteed truth. AI output may be incomplete, wrong, or
misleading. Legal, medical, financial, safety, security, compliance, and other
high-stakes decisions require qualified human review.

The automated security checks catch common repository regressions, not every
possible vulnerability or host-level risk.

## Reporting Security Issues

Do not post API keys, `.env` contents, private prompts, customer data, or other
secrets in a public issue.

Use a GitHub issue for non-sensitive security concerns. For sensitive reports,
use the repository owner's preferred private contact method if one is
published on the repository or owner profile. Do not disclose sensitive
details publicly while a private reporting path is being established.

Contributor implementation rules are documented separately in
[security-notes.md](security-notes.md). See [disclaimer.md](disclaimer.md) for
the full project disclaimer.
