import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/run_eco_synthetic_operational_dashboard.py")
JSON_OUTPUT = Path("results/eco_synthetic_operational_dashboard.json")
MD_OUTPUT = Path("results/eco_synthetic_operational_dashboard.md")


def test_synthetic_operational_dashboard_runs():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["classification"] == "allowed"
    assert payload["component_count"] == 3
    assert "datos sintéticos" in payload["limit"]
    assert "sin entrenamiento" in payload["limit"]
    assert "sin datos sensibles" in payload["limit"]
    labels = {component["label"] for component in payload["components"]}
    assert "synthetic demos suite report" in labels
    assert "synthetic demo comparison report" in labels
    assert "synthetic signal matrix report" in labels
    statuses = {component["status"] for component in payload["components"]}
    assert statuses == {"passed"}
    md = MD_OUTPUT.read_text(encoding="utf-8")
    assert "E.C.O. synthetic operational dashboard" in md
    assert "synthetic signal matrix report" in md
