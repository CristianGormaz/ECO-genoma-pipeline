import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_absorption_threshold_demo.py")
REGISTRY = Path("docs/architecture/eco-synthetic-demo-registry.json")
CONTRACT_VALIDATOR = Path("scripts/validate_eco_synthetic_contract.py")
JSON_OUTPUT = Path("results/eco_absorption_threshold_demo.json")
MD_OUTPUT = Path("results/eco_absorption_threshold_demo.md")


def test_absorption_threshold_demo_runs_and_validates_contract():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    assert payload["summary"]["classification"] == "allowed"
    assert payload["summary"]["data_policy"] == "synthetic_only"
    assert payload["summary"]["training"] is False
    assert payload["summary"]["sensitive_data"] is False
    assert payload["summary"]["baseline_changed"] is False
    assert payload["summary"]["threshold_recalibrated"] is False
    assert payload["trace"]
    assert all(item["action"] in {"digest", "rest"} for item in payload["trace"])

    validation = subprocess.run([sys.executable, str(CONTRACT_VALIDATOR), str(JSON_OUTPUT)], capture_output=True, text=True, check=False)
    assert validation.returncode == 0, validation.stdout + validation.stderr


def test_absorption_threshold_demo_is_registered():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    demos = {demo["id"]: demo for demo in data["demos"]}

    assert "absorption_threshold" in demos
    assert demos["absorption_threshold"]["runner"] == str(SCRIPT)
    assert demos["absorption_threshold"]["json_output"] == str(JSON_OUTPUT)
    assert demos["absorption_threshold"]["markdown_output"] == str(MD_OUTPUT)
