from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.run_eco_operational_maturity_score import build_report, to_markdown


SCRIPT = Path("scripts/run_eco_operational_maturity_score.py")
OUTPUT_JSON = Path("results/eco_operational_maturity_score.json")
OUTPUT_MD = Path("results/eco_operational_maturity_score.md")


def test_operational_maturity_score_contract_v1() -> None:
    report = build_report()

    assert report["status"] in {"passed", "attention"}
    assert report["global_decision"] == report["status"]
    assert report["classification"] in {"allowed", "attention_required"}
    assert report["dimensions_total"] == 9
    assert len(report["dimensions"]) == 9

    ids = {item["dimension_id"] for item in report["dimensions"]}
    expected_ids = {
        "governance_integrated",
        "decision_gates",
        "maturity_score",
        "end_to_end_panel",
        "phase_maturity",
        "robust_simulation",
        "results_comparison",
        "visible_rollback",
        "governed_admission",
    }
    assert ids == expected_ids

    for item in report["dimensions"]:
        assert item["state"] in {"passed", "attention", "missing", "future"}
        assert item["purpose"]
        assert item["evidence_expected"]
        assert item["responsible_limit"]

    boundary = report["coherence_boundary"]
    assert boundary["technical_coherence_only"] is True
    assert boundary["scientific_claims_evaluated"] is False
    assert boundary["biomedical_applied_claims_evaluated"] is False


def test_operational_maturity_score_v1_current_decision_is_attention() -> None:
    report = build_report()
    states = {item["dimension_id"]: item["state"] for item in report["dimensions"]}

    assert states["maturity_score"] == "passed"
    assert states["end_to_end_panel"] == "passed"
    assert states["phase_maturity"] == "future"
    assert states["visible_rollback"] == "passed"
    assert states["governed_admission"] == "attention"
    assert report["global_decision"] == "attention"
    assert report["classification"] == "attention_required"


def test_operational_maturity_score_script_writes_outputs() -> None:
    assert SCRIPT.exists(), "Debe existir scripts/run_eco_operational_maturity_score.py"

    run = subprocess.run(
        [sys.executable, str(SCRIPT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0, run.stderr
    assert OUTPUT_JSON.exists()
    assert OUTPUT_MD.exists()

    payload = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    markdown = OUTPUT_MD.read_text(encoding="utf-8").lower()
    inline_markdown = to_markdown(payload).lower()

    assert payload["global_decision"] in {"passed", "attention"}
    assert payload["status"] == payload["global_decision"]
    assert payload["classification"] in {"allowed", "attention_required"}
    assert payload["maturity_score_v1"] >= 0.0
    assert payload["maturity_score_v1"] <= 1.0
    assert "matriz de madurez" in markdown
    assert "frontera de interpretación" in markdown
    assert "coherencia técnica: sí." in markdown
    assert "sin datos reales" in markdown
    assert "sin entrenamiento" in markdown
    assert "sin modificación de baseline" in markdown
    assert "sin recalibración de umbrales" in markdown
    assert "sin interpretación clínica" in markdown
    assert "sin afirmaciones biomédicas aplicadas" in markdown
    assert "estado global" in inline_markdown
