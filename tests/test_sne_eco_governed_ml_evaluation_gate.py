from pathlib import Path

from scripts.run_sne_eco_governed_ml_evaluation_gate import build_report, to_markdown


def test_governed_ml_evaluation_gate_builds_green_report():
    report = build_report()

    assert report["status"] == "green"
    assert report["evaluation_allowed"] is True
    assert report["governance_status"] == "green"


def test_governed_ml_evaluation_gate_runs_required_steps():
    report = build_report()
    labels = {step["label"] for step in report["steps"]}

    assert "sensitive_governance_summary" in labels
    assert "empirical_train_eval_split" in labels
    assert "ml_baseline" in labels
    assert "ml_challenge_eval" in labels

    for step in report["steps"]:
        assert step["ok"] is True


def test_governed_ml_evaluation_gate_tracks_sensitive_counts():
    report = build_report()
    counts = report["governance_counts"]

    assert counts["allowed"] >= 1
    assert counts["conditional"] >= 1
    assert counts["blocked"] >= 1


def test_governed_ml_evaluation_gate_keeps_responsible_limits():
    report = build_report()
    markdown = to_markdown(report)

    assert "no ingiere datos reales" in markdown
    assert "no entrena modelos nuevos" in markdown
    assert "no diagnostica" in markdown
    assert "no tiene uso clínico aplicado" in markdown
    assert "no realiza inferencias forenses" in markdown
    assert "no afirma conciencia humana real" in markdown
    assert "no recalibra umbrales" in markdown
    assert "no modifica baseline estable" in markdown


def test_makefile_has_governed_ml_evaluation_gate_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-governed-ml-evaluation-gate:" in text
    assert "scripts/run_sne_eco_governed_ml_evaluation_gate.py" in text
