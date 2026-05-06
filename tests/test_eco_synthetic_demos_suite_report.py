import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_synthetic_demos_suite_report.py")
JSON_OUTPUT = Path("results/eco_synthetic_demos_suite_report.json")
MD_OUTPUT = Path("results/eco_synthetic_demos_suite_report.md")


def test_synthetic_demos_suite_report_runs_and_lists_registered_demos():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    demo_ids = set(payload["summary"]["demo_ids"])

    assert payload["classification"] == "allowed"
    assert payload["data_policy"] == "synthetic_only"
    assert payload["training"] is False
    assert payload["sensitive_data"] is False
    assert payload["baseline_changed"] is False
    assert payload["threshold_recalibrated"] is False
    assert payload["summary"]["registered_demos"] == 4
    assert "minimal_simulation" in demo_ids
    assert "signal_balance" in demo_ids
    assert "waste_pressure" in demo_ids
    assert "absorption_threshold" in demo_ids


def test_synthetic_demos_suite_report_markdown_mentions_limits():
    subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    text = MD_OUTPUT.read_text(encoding="utf-8")

    assert "E.C.O. synthetic demos suite report" in text
    assert "Datos sintéticos solamente" in text
    assert "Sin entrenamiento de modelos" in text
    assert "Sin datos sensibles" in text
