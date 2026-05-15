import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPT = Path("scripts/run_eco_synthetic_operational_dashboard.py")
JSON_OUTPUT = Path("results/eco_synthetic_operational_dashboard.json")
MD_OUTPUT = Path("results/eco_synthetic_operational_dashboard.md")


def test_synthetic_operational_dashboard_runs():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["classification"] == "allowed"
    assert payload["component_count"] == 7
    assert "datos sintéticos" in payload["limit"]
    assert "sin entrenamiento" in payload["limit"]
    assert "sin datos sensibles" in payload["limit"]
    labels = {component["label"] for component in payload["components"]}
    assert "adaptive dataset readiness gate" in labels
    assert "source admission decision summary" in labels
    assert "synthetic demos suite report" in labels
    assert "synthetic demo comparison report" in labels
    assert "synthetic signal matrix report" in labels
    assert "adaptive dataset operational report" in labels
    assert "governance panel" in labels
    statuses = {component["status"] for component in payload["components"]}
    assert statuses == {"passed"}
    md = MD_OUTPUT.read_text(encoding="utf-8")
    assert "E.C.O. synthetic operational dashboard" in md
    assert "source admission decision summary" in md
    assert "synthetic signal matrix report" in md
    assert "adaptive dataset operational report" in md
    assert "adaptive dataset readiness gate" in md
    assert "governance panel" in md


def test_synthetic_operational_dashboard_includes_adaptive_dataset_readiness_gate():
    script = SCRIPT
    text = script.read_text(encoding="utf-8")

    assert "adaptive_dataset_readiness_gate" in text
    assert "scripts/run_eco_adaptive_dataset_readiness_gate.py" in text
    assert "eco_adaptive_dataset_readiness_gate.json" in text
    assert 'Path("results/eco_adaptive_dataset_readiness_gate.json")' in text


def test_synthetic_operational_dashboard_includes_source_admission_summary():
    text = SCRIPT.read_text(encoding="utf-8")

    assert "source_admission_decision_summary" in text
    assert "scripts/run_eco_source_admission_decision_summary.py" in text
    assert "eco_source_admission_decision_summary.json" in text
    assert 'Path("results/eco_source_admission_decision_summary.json")' in text


def test_synthetic_operational_dashboard_includes_governance_panel():
    text = SCRIPT.read_text(encoding="utf-8")

    assert "governance_panel" in text
    assert "scripts/run_eco_governance_panel.py" in text
    assert "eco_governance_panel.json" in text
    assert 'Path("results/eco_governance_panel.json")' in text
