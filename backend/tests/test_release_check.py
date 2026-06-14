import subprocess
import sys
from pathlib import Path


def test_repository_release_checks_pass() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "scripts/release_check.py"],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Release checks passed" in result.stdout
