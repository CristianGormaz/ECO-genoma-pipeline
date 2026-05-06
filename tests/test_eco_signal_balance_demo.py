import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_signal_balance_demo.py")
VALIDATOR = Path("scripts/validate_eco_synthetic_contract.py")
JSON_PATH = Path("results/eco_signal_balance_demo.json")
MD_PATH = Path("results/eco_signal_balance_demo.md")
MAKEFILE = Path("Makefile")


def cleanup_outputs():
    JSON_PATH.unlink(missing_ok=True)
    MD_PATH.unlink(missing_ok=True)


def test_signal_balance_demo_script_exists():
    assert SCRIPT.exists()


def test_signal_balance_demo_make_targets_exist():
    text = MAKEFILE.read_text(encoding="utf-8")
    assert "eco-signal-balance-demo" in text
    assert "eco-validate-signal-balance-demo" in text


def test_signal_balance_demo_generates_contract_valid_payload():
    cleanup_outputs()
    try:
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
        assert result.returncode == 0
        assert "E.C.O. signal balance simulation demo" in result.stdout
        assert JSON_PATH.exists()
        assert MD_PATH.exists()

        validation = subprocess.run([sys.executable, str(VALIDATOR), str(JSON_PATH)], capture_output=True, text=True, check=False)
        assert validation.returncode == 0
        assert "Estado: passed" in validation.stdout

        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["summary"]["data_policy"] == "synthetic_only"
        assert data["summary"]["training"] is False
        assert data["summary"]["sensitive_data"] is False
        assert data["summary"]["baseline_changed"] is False
        assert data["summary"]["threshold_recalibrated"] is False
        assert data["summary"]["final_state"] == data["trace"][-1]
        assert {item["action"] for item in data["trace"]} <= {"digest", "rest"}
    finally:
        cleanup_outputs()
