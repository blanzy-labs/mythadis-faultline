import subprocess
import sys
from pathlib import Path


def test_repository_security_checks_pass() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "scripts/security_checks.py"],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Security checks passed" in result.stdout
