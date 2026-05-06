import copy
import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_eco_synthetic_contract import validate_payload


DEMO = Path("scripts/run_eco_minimal_simulation.py")
VALIDATOR = Path("scripts/validate_eco_synthetic_contract.py")
RESULT_JSON = Path("results/eco_minimal_simulation_demo.json")


def test_validator_accepts_minimal_simulation_result():
    demo = subprocess.run([sys.executable, str(DEMO)], capture_output=True, text=True, check=False)
    assert demo.returncode == 0
    assert RESULT_JSON.exists()

    result = subprocess.run([sys.executable, str(VALIDATOR), str(RESULT_JSON)], capture_output=True, text=True, check=False)

    assert result.returncode == 0
    assert "Estado: passed" in result.stdout


def test_validator_rejects_training_enabled():
    payload = json.loads(RESULT_JSON.read_text(encoding="utf-8")) if RESULT_JSON.exists() else {
        "title": "demo",
        "scope": "synthetic educational behavior simulation",
        "trace": [{
            "tick": 1,
            "nutrient": 1,
            "signal": 1,
            "waste": 0,
            "stability": 9,
            "action": "digest",
        }],
        "summary": {
            "ticks": 1,
            "final_state": {
                "tick": 1,
                "nutrient": 1,
                "signal": 1,
                "waste": 0,
                "stability": 9,
                "action": "digest",
            },
            "classification": "allowed",
            "data_policy": "synthetic_only",
            "training": False,
            "sensitive_data": False,
            "baseline_changed": False,
            "threshold_recalibrated": False,
        },
        "limits": ["No entrena modelos."],
    }

    invalid = copy.deepcopy(payload)
    invalid["summary"]["training"] = True

    errors = validate_payload(invalid)

    assert any("summary.training" in error for error in errors)


def test_validator_rejects_negative_trace_values():
    payload = {
        "title": "demo",
        "scope": "synthetic educational behavior simulation",
        "trace": [{
            "tick": 1,
            "nutrient": -1,
            "signal": 1,
            "waste": 0,
            "stability": 9,
            "action": "digest",
        }],
        "summary": {
            "ticks": 1,
            "final_state": {
                "tick": 1,
                "nutrient": -1,
                "signal": 1,
                "waste": 0,
                "stability": 9,
                "action": "digest",
            },
            "classification": "allowed",
            "data_policy": "synthetic_only",
            "training": False,
            "sensitive_data": False,
            "baseline_changed": False,
            "threshold_recalibrated": False,
        },
        "limits": ["No entrena modelos."],
    }

    errors = validate_payload(payload)

    assert any("nutrient" in error for error in errors)
