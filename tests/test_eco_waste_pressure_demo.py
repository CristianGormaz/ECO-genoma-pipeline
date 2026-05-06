import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_waste_pressure_demo.py")
REGISTRY = Path("docs/architecture/eco-synthetic-demo-registry.json")
CONTRACT_VALIDATOR = Path("scripts/validate_eco_synthetic_contract.py")
JSON_OUTPUT = Path("results/eco_waste_pressure_demo.json")
MD_OUTPUT = Path("results/eco_waste_pressure_demo.md")


def test_waste_pressure_demo_runs_and_validates_contract():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    assert payload["summary"]["classification"] == "allowed"
    assert payload["summary"]["data_policy"] == "synthetic_only"
    assert payload["summary"]["training"] is False
    assert payload["summary"]["sensitive_data"] is False

    validation = subprocess.run([sys.executable, str(CONTRACT_VALIDATOR), str(JSON_OUTPUT)], capture_output=True, text=True, check=False)
    assert validation.returncode == 0, validation.stdout + validation.stderr


def test_waste_pressure_demo_is_registered():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    demo_ids = {demo["id"] for demo in data["demos"]}

    assert "waste_pressure" in demo_ids
    assert any(demo["runner"] == "scripts/run_eco_waste_pressure_demo.py" for demo in data["demos"])


def test_waste_pressure_demo_uses_allowed_actions_only():
    subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    actions = {item["action"] for item in payload["trace"]}

    assert actions <= {"digest", "rest"}
