#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_ENV_EXAMPLE = [
    "OPENAI_API_KEY=",
    "GEMINI_API_KEY=",
    "OPENAI_MODEL=gpt-4.1-mini",
    "GEMINI_MODEL=gemini-2.5-flash",
]

FRONTEND_FILES = [
    ROOT / "frontend" / "src",
    ROOT / "frontend" / "index.html",
    ROOT / "frontend" / "package.json",
]
APP_FILES = [
    ROOT / "backend" / "app",
    ROOT / "frontend" / "src",
]
DEPENDENCY_FILES = [
    ROOT / "backend" / "requirements.txt",
    ROOT / "frontend" / "package.json",
]

KEY_ENV_NAMES = [
    f"{provider}_{suffix}"
    for provider in ("OPENAI", "GEMINI")
    for suffix in ("API_KEY",)
]
VITE_KEY_PREFIXES = [f"VITE_{provider}" for provider in ("OPENAI", "GEMINI")]
STORAGE_PATTERNS = [
    r"\blocalStorage\b",
    r"\bsessionStorage\b",
    r"\bindexedDB\b",
    r"\bdocument\.cookie\b",
]
DATABASE_PATTERNS = [
    r"\bsqlite3?\b",
    r"\bsqlalchemy\b",
    r"\bpostgres(?:ql)?\b",
    r"\bmysql\b",
    r"\bmongodb\b",
    r"\bredis\b",
    r"\bprisma\b",
    r"\btypeorm\b",
    r"\bsequelize\b",
]
ANALYTICS_PATTERNS = [
    r"\banalytics\b",
    r"\btelemetry\b",
    r"\bposthog\b",
    r"\bsegment\b",
    r"\bmixpanel\b",
    r"\bamplitude\b",
    r"\bga4\b",
    r"\bgoogle-analytics\b",
]
BACKEND_WRITE_PATTERNS = [
    r"\.write_text\s*\(",
    r"\.write_bytes\s*\(",
    r"\bopen\s*\([^,\n]+,\s*[\"'][wax+]",
]
SECRET_VALUE_PATTERNS = [
    re.compile(r"\b" + "sk" + r"-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\b" + "AI" + r"za[A-Za-z0-9_-]{20,}\b"),
]


def main() -> int:
    failures: list[str] = []

    check_env_example(failures)
    check_git_env_safety(failures)
    check_frontend_key_boundary(failures)
    check_forbidden_app_patterns(failures)
    check_dependency_boundaries(failures)
    check_backend_file_writes(failures)
    check_tracked_secret_values(failures)

    if failures:
        print("Security checks failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Security checks passed:")
    print("- .env.example contains only the expected safe placeholders.")
    print("- Secret-bearing env files are ignored and untracked.")
    print("- Provider key names and values are absent from frontend source.")
    print("- No browser storage, database, analytics, or backend file writes found.")
    print("- No obvious provider key values found in repository files.")
    return 0


def check_env_example(failures: list[str]) -> None:
    path = ROOT / ".env.example"
    if not path.is_file():
        failures.append(".env.example is missing.")
        return

    lines = path.read_text(encoding="utf-8").splitlines()
    if lines != EXPECTED_ENV_EXAMPLE:
        failures.append(
            ".env.example must contain exactly the approved placeholders and models."
        )
    if any(pattern.search("\n".join(lines)) for pattern in SECRET_VALUE_PATTERNS):
        failures.append(".env.example contains a provider-key-shaped value.")


def check_git_env_safety(failures: list[str]) -> None:
    tracked = set(run_git("ls-files").splitlines())
    if ".env.example" not in tracked:
        failures.append(".env.example is not tracked by Git.")

    forbidden_tracked = [
        path
        for path in tracked
        if is_secret_env_path(path)
    ]
    if forbidden_tracked:
        failures.append(
            "Secret-bearing env files are tracked: " + ", ".join(forbidden_tracked)
        )

    for path in (
        ".env",
        ".env.local",
        "backend/.env",
        "backend/.env.local",
        "frontend/.env",
        "frontend/.env.local",
    ):
        result = subprocess.run(
            ["git", "check-ignore", "--quiet", path],
            cwd=ROOT,
            check=False,
        )
        if result.returncode != 0:
            failures.append(f"{path} is not protected by .gitignore.")


def check_frontend_key_boundary(failures: list[str]) -> None:
    patterns = [re.escape(name) for name in KEY_ENV_NAMES + VITE_KEY_PREFIXES]
    scan_patterns(
        FRONTEND_FILES,
        patterns,
        "Frontend provider-key reference",
        failures,
    )
    scan_compiled_patterns(
        FRONTEND_FILES,
        SECRET_VALUE_PATTERNS,
        "Frontend provider-key-shaped value",
        failures,
    )


def check_forbidden_app_patterns(failures: list[str]) -> None:
    scan_patterns(
        APP_FILES,
        STORAGE_PATTERNS,
        "Browser storage or cookie API",
        failures,
    )


def check_dependency_boundaries(failures: list[str]) -> None:
    paths = DEPENDENCY_FILES + APP_FILES
    scan_patterns(paths, DATABASE_PATTERNS, "Database dependency or usage", failures)
    scan_patterns(
        paths,
        ANALYTICS_PATTERNS,
        "Analytics or telemetry dependency or usage",
        failures,
    )


def check_backend_file_writes(failures: list[str]) -> None:
    scan_patterns(
        [ROOT / "backend" / "app"],
        BACKEND_WRITE_PATTERNS,
        "Backend file-write operation",
        failures,
    )


def check_tracked_secret_values(failures: list[str]) -> None:
    scan_compiled_patterns(
        [ROOT],
        SECRET_VALUE_PATTERNS,
        "Repository provider-key-shaped value",
        failures,
    )


def scan_patterns(
    paths: list[Path],
    patterns: list[str],
    label: str,
    failures: list[str],
) -> None:
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    scan_compiled_patterns(paths, compiled, label, failures)


def scan_compiled_patterns(
    paths: list[Path],
    patterns: list[re.Pattern[str]],
    label: str,
    failures: list[str],
) -> None:
    for path in iter_files(paths):
        content = read_text(path)
        if content is None:
            continue
        for line_number, line in enumerate(content.splitlines(), start=1):
            if any(pattern.search(line) for pattern in patterns):
                failures.append(
                    f"{label}: {path.relative_to(ROOT)}:{line_number}"
                )


def iter_files(paths: list[Path]):
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and not is_excluded(child):
                    yield child


def is_excluded(path: Path) -> bool:
    excluded_parts = {
        ".git",
        "node_modules",
        "dist",
        "build",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
    }
    is_secret_env = path.name == ".env" or (
        path.name.startswith(".env.") and path.name != ".env.example"
    )
    return any(part in excluded_parts for part in path.parts) or is_secret_env


def is_secret_env_path(path: str) -> bool:
    name = Path(path).name
    return name == ".env" or (name.startswith(".env.") and name != ".env.example")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


if __name__ == "__main__":
    sys.exit(main())
