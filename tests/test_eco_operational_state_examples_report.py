import json
import subprocess
import sys
from pathlib import Path


def test_eco_operational_state_examples_report_outputs_contract():
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "run_eco_operational_state_examples_report.py"
    json_out = root / "results" / "eco_operational_state_examples_report.json"
    md_out = root / "results" / "eco_operational_state_examples_report.md"

    result = subprocess.run([sys.executable, str(script)], cwd=root, text=True, capture_output=True, check=True)

    assert "Estado: passed" in result.stdout
    assert json_out.exists()
    assert md_out.exists()

    data = json.loads(json_out.read_text(encoding="utf-8"))
    md_text = md_out.read_text(encoding="utf-8")

    assert data["status"] == "passed"
    assert data["classification"] == "permitido"
    assert data["examples_count"] >= 1
    assert data["examples"]
    assert data["responsible_limit"]
    assert "sin datos sensibles" in data["responsible_limit"]
    assert "sin entrenamiento" in data["responsible_limit"]
    assert "# E.C.O. operational state examples report" in md_text
