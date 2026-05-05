from pathlib import Path

from scripts.run_sne_eco_ml_challenge_eval import build_report, to_markdown


def test_ml_challenge_eval_builds_report():
    report = build_report()

    assert report["status"] in {"green", "attention"}
    assert report["challenge_count"] >= 8
    assert report["total"] == report["challenge_count"]
    assert 0.0 <= report["accuracy"] <= 1.0


def test_ml_challenge_eval_generates_predictions():
    report = build_report()

    assert len(report["predictions"]) == report["challenge_count"]

    for row in report["predictions"]:
        assert "expected_decision" in row
        assert "predicted_decision" in row
        assert "nearest_train_id" in row
        assert "similarity" in row


def test_ml_challenge_eval_rejects_forbidden_claims():
    report = build_report()

    assert "challenge_clinical_limit_001" in report["forbidden_rows"]
    assert "challenge_diagnostic_limit_001" in report["forbidden_rows"]
    assert "challenge_forensic_limit_001" in report["forbidden_rows"]
    assert "challenge_consciousness_limit_001" in report["forbidden_rows"]
    assert report["forbidden_not_rejected"] == []
    assert report["errors"] == []


def test_ml_challenge_eval_keeps_responsible_limits():
    report = build_report()
    markdown = to_markdown(report)

    assert "no entrena modelos" in markdown
    assert "clínico" in markdown
    assert "diagnóstico" in markdown
    assert "forense" in markdown
    assert "conciencia humana" in markdown


def test_makefile_has_ml_challenge_eval_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-ml-challenge-eval:" in text
    assert "scripts/run_sne_eco_ml_challenge_eval.py" in text
