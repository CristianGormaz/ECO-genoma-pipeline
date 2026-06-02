import json
import subprocess
import sys
from pathlib import Path

from scripts.run_eco_governed_experimental_cycle import build_report


SCRIPT = Path("scripts/run_eco_governed_experimental_cycle.py")
OUTPUT_JSON = Path("results/eco_governed_experimental_cycle.json")
OUTPUT_MD = Path("results/eco_governed_experimental_cycle.md")


def test_governed_experimental_cycle_contract() -> None:
    report = build_report()

    assert report["cycle_id"] == "eco-governed-experimental-cycle-v1"
    assert report["status"] in {"passed", "attention", "blocked"}
    assert set(report["allowed_states"]) == {"passed", "attention", "missing", "future", "blocked"}
    assert set(report["allowed_decisions"]) == {"advance", "pause", "review", "reject"}
    assert report["final_decision"] in {"advance", "pause", "review", "reject"}
    assert report["decision_reason"]

    phase_maturity = report["phase_maturity"]
    assert phase_maturity["current_phase"] == "governed_experimental"
    assert phase_maturity["status"] == "passed"
    phase_ids = {item["phase"] for item in phase_maturity["phases"]}
    assert phase_ids == {"draft", "synthetic", "governed_experimental", "stable_candidate", "blocked"}
    phase_states = {item["phase"]: item["state"] for item in phase_maturity["phases"]}
    assert phase_states["draft"] == "passed"
    assert phase_states["synthetic"] == "passed"
    assert phase_states["governed_experimental"] == "passed"
    assert phase_states["stable_candidate"] == "future"
    assert phase_states["blocked"] == "passed"

    governed_admission = report["governed_admission"]
    assert governed_admission["status"] == "passed"
    admission_checks = {item["id"]: item["state"] for item in governed_admission["checks"]}
    assert admission_checks == {
        "intake_gate": "passed",
        "source_guard": "passed",
        "maturity_score": "passed",
        "rollback_visibility": "passed",
        "responsible_limits": "passed",
        "final_decision": "passed",
    }

    gate_ids = {item["id"] for item in report["gates"]}
    assert gate_ids == {
        "source_admission_decision_summary",
        "sensitive_intake_gate",
        "governed_ml_evaluation_gate",
    }
    for gate in report["gates"]:
        assert gate["state"] in {"passed", "attention", "missing", "future", "blocked"}

    rollback = report["rollback_visibility"]
    assert rollback["status"] == "passed"
    assert rollback["evidence_available"] is True
    assert rollback["dry_run_only"] is True
    assert rollback["lock_breach"] is False

    assert report["maturity_score_v1"]["before_reference"]["maturity_score_v1"] == 0.8611
    assert report["maturity_score_v1"]["after"]["maturity_score_v1"] == 1.0
    assert report["maturity_score_v1"]["after"]["global_decision"] == "passed"
    assert report["final_decision"] == "advance"

    limits = " ".join(report["responsible_limits"])
    for token in [
        "sin datos reales",
        "sin entrenamiento",
        "sin datos sensibles",
        "sin diagnóstico",
        "sin interpretación clínica",
        "sin baseline changes",
        "sin threshold recalibration",
        "sin conciencia",
        "sin libre albedrío real",
    ]:
        assert token in limits

    boundary = report["interpretation_boundary"]
    assert boundary["uses_real_data"] is False
    assert boundary["training_enabled"] is False
    assert boundary["baseline_changed"] is False
    assert boundary["threshold_recalibration"] is False
    assert boundary["clinical_or_biomedical_applied_claim"] is False


def test_governed_experimental_cycle_script_writes_outputs() -> None:
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert OUTPUT_JSON.exists()
    assert OUTPUT_MD.exists()

    payload = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    markdown = OUTPUT_MD.read_text(encoding="utf-8")

    assert payload["final_decision"] in {"advance", "pause", "review", "reject"}
    assert payload["phase_maturity"]["status"] == "passed"
    assert payload["governed_admission"]["status"] == "passed"
    assert "Madurez por fase" in markdown
    assert "Admisión gobernada" in markdown
    assert "Gates evaluados" in markdown
    assert "Rollback visible" in markdown
    assert "Maturity score v1" in markdown
    assert "Límites responsables" in markdown
    assert "sin datos reales" in markdown
    assert "sin libre albedrío real" in markdown
