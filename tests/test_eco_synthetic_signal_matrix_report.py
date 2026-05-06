import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/run_eco_synthetic_signal_matrix_report.py")
JSON_OUTPUT = Path("results/eco_synthetic_signal_matrix_report.json")
MD_OUTPUT = Path("results/eco_synthetic_signal_matrix_report.md")


def test_signal_matrix_report_runs():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["classification"] == "allowed"
    assert payload["signal_count"] == 4
    assert "datos sintéticos" in payload["limit"]
    assert "sin entrenamiento" in payload["limit"]
    md = MD_OUTPUT.read_text(encoding="utf-8")
    assert "minimal simulation" in md
    assert "signal balance" in md
    assert "waste pressure" in md
    assert "absorption threshold" in md
