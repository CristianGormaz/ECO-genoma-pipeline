from pathlib import Path

from scripts.run_sne_eco_ml_baseline import build_report, to_markdown


def test_ml_baseline_builds_report():
    report = build_report()

    assert report["status"] in {"green", "attention"}
    assert report["train_count"] > report["eval_count"] > 0
    assert report["total"] == report["eval_count"]
    assert 0.0 <= report["accuracy"] <= 1.0


def test_ml_baseline_generates_predictions():
    report = build_report()

    assert len(report["predictions"]) == report["eval_count"]

    for row in report["predictions"]:
        assert "expected_decision" in row
        assert "predicted_decision" in row
        assert "nearest_train_id" in row
        assert "similarity" in row


def test_ml_baseline_keeps_responsible_limits():
    report = build_report()
    markdown = to_markdown(report)

    assert "no clínico" in markdown
    assert "diagnóstico" in markdown
    assert "forense" in markdown
    assert "conciencia humana" in markdown
    assert report["errors"] == []


def test_ml_baseline_tracks_eval_distribution():
    report = build_report()

    expected = report["expected_counts"]

    assert "absorb" in expected
    assert "reject" in expected
    assert "quarantine" in expected
    assert "discard_duplicate" in expected


def test_makefile_has_ml_baseline_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-ml-baseline:" in text
    assert "scripts/run_sne_eco_ml_baseline.py" in text
