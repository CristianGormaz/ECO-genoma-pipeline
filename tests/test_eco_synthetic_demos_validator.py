import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/validate_eco_synthetic_demos.py")
MAKEFILE = Path("Makefile")


def test_synthetic_demos_validator_script_exists():
    assert SCRIPT.exists()


def test_makefile_exposes_synthetic_demos_validation_command():
    text = MAKEFILE.read_text(encoding="utf-8")
    assert "eco-validate-synthetic-demos:" in text
    assert "scripts/validate_eco_synthetic_demos.py" in text


def test_synthetic_demos_validator_runs_successfully():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "E.C.O. synthetic demos validation" in result.stdout
    assert "minimal simulation" in result.stdout
    assert "signal balance" in result.stdout
    assert "Estado: passed" in result.stdout
