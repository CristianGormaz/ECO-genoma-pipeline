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
    assert payload["panel_kind"] == "end_to_end_operational_panel_v1"
    assert payload["status"] in {"passed", "attention", "red"}
    assert payload["classification"] in {"allowed", "conditional", "attention_required", "blocked"}
    assert payload["final_decision"] in {"advance", "pause", "review", "reject"}
    assert payload["component_count"] == 9
    assert isinstance(payload["components_all_passed"], bool)
    assert payload["components_all_passed"] is True
    assert "datos sintéticos" in payload["limit"]
    assert "sin entrenamiento" in payload["limit"]
    assert "sin datos sensibles" in payload["limit"]
    assert "sin modificación de baseline" in payload["limit"]
    assert "sin recalibración" in payload["limit"]
    assert "sin afirmaciones biomédicas aplicadas" in payload["limit"]
    assert "sin libre albedrío real" in payload["limit"]
    assert "sin conciencia" in payload["limit"]
    assert payload["repo_status"]["state"] in {"green", "attention"}
    assert isinstance(payload["repo_status"]["tree_clean"], bool)
    assert "branch" in payload["repo_status"]
    assert payload["maturity_score"]["global_decision"] in {"passed", "attention"}
    assert payload["maturity_score"]["score_v1"] >= 0.0
    assert payload["maturity_score"]["score_v1"] <= 1.0
    gate_ids = {item["id"] for item in payload["relevant_gates"]}
    assert "source_admission_decision_summary" in gate_ids
    assert "sensitive_intake_gate" in gate_ids
    assert "governed_ml_evaluation_gate" in gate_ids
    for gate in payload["relevant_gates"]:
        assert gate["status"] in {"passed", "attention", "red"}
    assert payload["rollback_evidence"]["status"] in {"passed", "attention"}
    assert isinstance(payload["rollback_evidence"]["evidence_available"], bool)
    assert payload["current_risks"]
    assert payload["decision_reason"]
    assert payload["responsible_limits"]
    labels = {component["label"] for component in payload["components"]}
    assert "adaptive dataset readiness gate" in labels
    assert "source admission decision summary" in labels
    assert "synthetic demos suite report" in labels
    assert "synthetic demo comparison report" in labels
    assert "synthetic signal matrix report" in labels
    assert "adaptive dataset operational report" in labels
    assert "governance panel" in labels
    assert "capabilities report" in labels
    assert "LAOS Governance Gate" in labels
    statuses = {component["status"] for component in payload["components"]}
    assert statuses == {"passed"}
    md = MD_OUTPUT.read_text(encoding="utf-8")
    assert "E.C.O. synthetic operational dashboard" in md
    assert "Repo / eco-status" in md
    assert "Score de madurez" in md
    assert "Gates relevantes" in md
    assert "Riesgos actuales" in md
    assert "Evidencia de rollback" in md
    assert "Límites responsables" in md
    assert "Decisión final" in md
    assert "source admission decision summary" in md
    assert "synthetic signal matrix report" in md
    assert "adaptive dataset operational report" in md
    assert "adaptive dataset readiness gate" in md
    assert "governance panel" in md
    assert "capabilities report" in md
    assert "LAOS Governance Gate" in md
    assert "advance" in md
    assert "pause" in md
    assert "review" in md
    assert "reject" in md
    assert "sin libre albedrío real" in md
    assert "sin conciencia" in md


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


def test_synthetic_operational_dashboard_includes_capabilities_report():
    text = SCRIPT.read_text(encoding="utf-8")

    assert "capabilities_report" in text
    assert "scripts/run_eco_capabilities_report.py" in text
    assert "eco_capabilities_report.json" in text
    assert 'Path("results/eco_capabilities_report.json")' in text


def test_synthetic_operational_dashboard_includes_laos_governance_gate():
    text = SCRIPT.read_text(encoding="utf-8")

    assert "laos_governance_gate" in text
    assert "LAOS Governance Gate" in text
    assert "scripts/run_eco_laos_governance_gate_demo.py" in text
    assert "eco_laos_governance_gate_demo.json" in text
    assert 'Path("results/eco_laos_governance_gate_demo.json")' in text


def test_synthetic_operational_dashboard_includes_end_to_end_operational_fields():
    text = SCRIPT.read_text(encoding="utf-8")

    assert "repo_status" in text
    assert "maturity_score" in text
    assert "relevant_gates" in text
    assert "current_risks" in text
    assert "rollback_evidence" in text
    assert "final_decision" in text
    assert "advance" in text
    assert "pause" in text
    assert "review" in text
    assert "reject" in text
