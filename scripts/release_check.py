#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = "0.1.1"
RELEASE_NAME = "v0.1.1 - Blanzy Labs Standardization Patch"
APP_NAME = "AI Faultline"
TAGLINE = "Find the crack before the collapse."

REQUIRED_FILES = [
    ".env.example",
    "README.md",
    "CONTRIBUTING.md",
    "docker-compose.yml",
    "backend/app/main.py",
    "backend/requirements.txt",
    "frontend/package.json",
    "frontend/package-lock.json",
    "docs/architecture.md",
    "docs/security.md",
    "docs/security-and-privacy.md",
    "docs/local-install.md",
    "docs/troubleshooting.md",
    "docs/demo-script.md",
    "docs/prompt-design.md",
    "docs/sample-report.md",
    "docs/security-notes.md",
    "docs/release-notes-v0.1.0.md",
    "docs/release-notes/v0.1.1.md",
    "docs/release-checklist.md",
    "docs/validation/v0.1.1-validation.md",
    "LICENSE",
    "scripts/security_checks.py",
]

README_REQUIREMENTS = [
    APP_NAME,
    TAGLINE,
    "v0.1.1",
    "OpenAI",
    "Gemini",
    "gpt-4.1-mini",
    "gemini-2.5-flash",
    "cp .env.example .env",
    "docker compose up --build",
    "docs/release-notes/v0.1.1.md",
    "docs/release-checklist.md",
]

RELEASE_DOC_REQUIREMENTS = [
    "no database",
    "no telemetry",
    "no saved report or prompt history",
    "external providers",
    "does not browse",
    "verify facts",
    "browser-side Markdown export",
]


def main() -> int:
    failures: list[str] = []

    check_required_files(failures)
    check_readme(failures)
    check_release_docs(failures)
    check_versions(failures)
    check_security_script(failures)

    if failures:
        print("Release checks failed:")
        for failure in failures:
            print(f"- FAIL: {failure}")
        return 1

    print("Release checks passed:")
    print(f"- PASS: Release identity is {APP_NAME} {RELEASE_NAME}.")
    print("- PASS: Required release, setup, security, and contributor files exist.")
    print("- PASS: README links release docs and lists supported default models.")
    print("- PASS: Backend and frontend versions are consistent at 0.1.1.")
    print("- PASS: Release docs preserve privacy boundaries and limitations.")
    print("- PASS: Consolidated security checks passed.")
    print("- PASS: No provider keys or network access were required.")
    return 0


def check_required_files(failures: list[str]) -> None:
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            failures.append(f"Required file is missing: {relative_path}")


def check_readme(failures: list[str]) -> None:
    content = read_required_text(ROOT / "README.md", failures)
    for phrase in README_REQUIREMENTS:
        if phrase not in content:
            failures.append(f"README is missing required release content: {phrase}")


def check_release_docs(failures: list[str]) -> None:
    notes = read_required_text(
        ROOT / "docs" / "release-notes" / "v0.1.1.md",
        failures,
    )
    checklist = read_required_text(
        ROOT / "docs" / "release-checklist.md",
        failures,
    )
    combined = f"{notes}\n{checklist}".casefold()

    for phrase in RELEASE_DOC_REQUIREMENTS:
        if phrase.casefold() not in combined:
            failures.append(f"Release docs are missing required content: {phrase}")

    if RELEASE_NAME not in notes or RELEASE_NAME not in checklist:
        failures.append(f"Release docs must identify {RELEASE_NAME}.")
    if "No tag movement" not in checklist:
        failures.append("Release checklist is missing tag safety guidance.")
    if "No release overwrite" not in checklist:
        failures.append("Release checklist is missing release safety guidance.")


def check_versions(failures: list[str]) -> None:
    backend_main = read_required_text(ROOT / "backend" / "app" / "main.py", failures)
    expected_backend_version = f'version="{RELEASE_VERSION}"'
    if expected_backend_version not in backend_main:
        failures.append(
            f"Backend version is not declared as {RELEASE_VERSION}."
        )

    package_path = ROOT / "frontend" / "package.json"
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"Could not read frontend/package.json: {exc}")
        return

    if package.get("version") != RELEASE_VERSION:
        failures.append(f"Frontend version is not {RELEASE_VERSION}.")


def check_security_script(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, "scripts/security_checks.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = (result.stdout + result.stderr).strip()
        failures.append(f"Security checks failed. {detail}")


def read_required_text(path: Path, failures: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        failures.append(f"Could not read {path.relative_to(ROOT)}: {exc}")
        return ""


if __name__ == "__main__":
    sys.exit(main())
