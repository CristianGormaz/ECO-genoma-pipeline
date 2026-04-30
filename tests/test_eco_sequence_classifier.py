from pathlib import Path
import json

from src.eco_sequence_classifier import (
    build_classifier_report,
    extract_features,
    parse_labeled_sequences_tsv,
    split_train_test,
    train_centroid_classifier,
    write_json_report,
)


def test_extract_features_detects_basic_motifs():
    features = extract_features("ACGTCCAATTTTTTTTATAAAGGGCGGAATAAA")
    assert features["motif_count"] >= 4
    assert features["has_tata"] == 1.0
    assert features["has_caat"] == 1.0
    assert features["has_gc_box"] == 1.0
    assert features["has_polya"] == 1.0


def test_classifier_baseline_demo_dataset_runs_with_explicit_split():
    records = parse_labeled_sequences_tsv(Path("examples/eco_labeled_sequences.tsv"))
    assert len(records) == 10

    train_records, test_records = split_train_test(records)
    assert len(train_records) == 6
    assert len(test_records) == 4

    centroids = train_centroid_classifier(train_records)
    assert set(centroids) == {"non_regulatory", "regulatory"}

    report = build_classifier_report(records)
    assert report["model_type"] == "centroid_baseline_explicable"
    assert report["data_split"] == {
        "train": 6,
        "test": 4,
        "note": "Entrena con split=train y evalúa desempeño reportable en split=test.",
    }
    assert report["train_evaluation"]["total"] == 6
    assert report["test_evaluation"]["total"] == 4
    assert report["test_evaluation"]["accuracy"] >= 0.75


def test_classifier_baseline_reports_per_class_metrics():
    records = parse_labeled_sequences_tsv(Path("examples/eco_labeled_sequences.tsv"))
    report = build_classifier_report(records)
    test_metrics = report["test_evaluation"]["classification_metrics"]

    assert set(test_metrics) == {"per_class", "macro_avg", "weighted_avg"}
    assert set(test_metrics["per_class"]) == {"non_regulatory", "regulatory"}

    for label in ("non_regulatory", "regulatory"):
        values = test_metrics["per_class"][label]
        assert set(values) == {"precision", "recall", "f1", "support"}
        assert 0.0 <= values["precision"] <= 1.0
        assert 0.0 <= values["recall"] <= 1.0
        assert 0.0 <= values["f1"] <= 1.0
        assert values["support"] >= 1

    assert test_metrics["macro_avg"]["support"] == 4
    assert 0.0 <= test_metrics["macro_avg"]["f1"] <= 1.0
    assert test_metrics["weighted_avg"]["support"] == 4
    assert 0.0 <= test_metrics["weighted_avg"]["f1"] <= 1.0


def test_write_json_report_allows_existing_output_directory(tmp_path):
    output_dir = tmp_path / "results"
    output_dir.mkdir()
    output_path = output_dir / "classifier_report.json"
    payload = {"status": "ok", "stage": "classifier-baseline"}

    write_json_report(payload, output_path)

    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == payload
