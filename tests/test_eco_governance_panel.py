from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_eco_governance_panel.py"
JSON_OUTPUT = ROOT / "results" / "eco_governance_panel.json"
MD_OUTPUT = ROOT / "results" / "eco_governance_panel.md"


def test_governance_panel_script_runs_and_generates_outputs() -> None:
    completed = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)

    assert "Generated:" in completed.stdout
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()


def test_governance_panel_declares_responsible_limits_and_guards() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))

    assert payload["uses_real_data"] is False
    assert payload["training_enabled"] is False
    assert payload["baseline_modified"] is False
    assert payload["threshold_recalibration_enabled"] is False
    assert payload["human_review_required_for_critical_changes"] is True

    limits = set(payload["responsible_limits"])
    assert "no_real_data" in limits
    assert "no_training" in limits
    assert "no_baseline_changes" in limits
    assert "no_threshold_recalibration" in limits

    gates = payload["gates"]
    assert gates["real_data_gate"] == "human_review_required"
    assert gates["training_gate"] == "human_review_required"
    assert gates["baseline_gate"] == "human_review_required"
    assert gates["threshold_gate"] == "human_review_required"
