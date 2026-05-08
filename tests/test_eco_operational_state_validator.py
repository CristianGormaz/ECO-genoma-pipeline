import subprocess
import sys
from pathlib import Path


def test_eco_operational_state_validator_passes_examples():
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "validate_eco_operational_state_examples.py"
    result = subprocess.run([sys.executable, str(script)], cwd=root, text=True, capture_output=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Estado: passed" in result.stdout
    assert "Ejemplos validados:" in result.stdout
    assert "sin datos sensibles" in result.stdout
