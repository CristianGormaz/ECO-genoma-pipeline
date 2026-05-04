from pathlib import Path

from scripts.run_sne_eco_training_readiness import build_report, to_markdown


def test_training_readiness_allows_training_when_seed_dataset_reaches_minimum():
    report = build_report()

    assert report["status"] == "green"
    assert report["training_allowed"] is True
    assert report["row_count"] >= 6
    assert report["row_count"] >= report["minimum_rows_for_training"]


def test_training_readiness_keeps_expected_decision_coverage():
    report = build_report()
    decisions = report["counts"]["expected_decision"]

    assert "absorb" in decisions
    assert "reject" in decisions
    assert "quarantine" in decisions
    assert "discard_duplicate" in decisions


def test_training_readiness_detects_responsible_limit_rows():
    report = build_report()

    assert "seed_claim_limit_001" in report["forbidden_claim_rows"]
    assert "seed_consciousness_limit_001" in report["forbidden_claim_rows"]
    assert report["errors"] == []


def test_training_readiness_markdown_keeps_responsible_limit():
    markdown = to_markdown(build_report())

    assert "Preparación de entrenamiento" in markdown
    assert "no tiene uso clínico" in markdown
    assert "no modela conciencia humana" in markdown


def test_makefile_has_training_readiness_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-training-readiness:" in text
    assert "scripts/run_sne_eco_training_readiness.py" in text
