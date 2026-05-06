import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_status.py")
MAKEFILE = Path("Makefile")


def test_eco_status_script_exists():
    assert SCRIPT.exists()


def test_eco_status_outputs_operational_state():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert "E.C.O. status operativo" in result.stdout
    assert "Rama actual:" in result.stdout
    assert "Árbol limpio:" in result.stdout
    assert "Límite operativo" in result.stdout


def test_eco_status_make_target_exists():
    text = MAKEFILE.read_text(encoding="utf-8")
    assert ".PHONY: eco-status" in text
    assert "eco-status:" in text
    assert "scripts/run_eco_status.py" in text
