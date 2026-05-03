from pathlib import Path

from scripts.run_sne_eco_empirical_train_eval_split import build_report, to_markdown


def test_empirical_train_eval_split_is_green():
    report = build_report()

    assert report["status"] == "green"
    assert report["training_split_ready"] is True
    assert report["row_count"] >= report["minimum_rows_for_split"]
    assert report["train_count"] > report["eval_count"] > 0


def test_empirical_train_eval_split_prevents_leakage():
    report = build_report()

    assert report["duplicate_ids"] == []
    assert report["id_overlap"] == []
    assert report["source_text_overlap_count"] == 0


def test_empirical_train_eval_split_preserves_label_coverage():
    report = build_report()

    assert report["missing_train_labels"] == []
    assert report["missing_eval_labels"] == []

    train_labels = report["counts"]["train_expected_decision"]
    eval_labels = report["counts"]["eval_expected_decision"]

    for label in ["absorb", "reject", "quarantine", "discard_duplicate"]:
        assert label in train_labels
        assert label in eval_labels


def test_empirical_train_eval_split_keeps_responsible_limits():
    report = build_report()
    markdown = to_markdown(report)

    assert "no clínico" in markdown
    assert "no diagnóstico" in markdown
    assert "no forense" in markdown
    assert "no conciencia humana" in markdown
    assert "seed_claim_limit_001" in report["forbidden_claim_rows"]


def test_makefile_has_empirical_train_eval_split_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-empirical-train-eval-split:" in text
    assert "scripts/run_sne_eco_empirical_train_eval_split.py" in text
