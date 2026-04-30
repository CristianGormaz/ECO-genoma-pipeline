from pathlib import Path
import json

from src.eco_sequence_classifier import (
    build_classifier_report,
    extract_features,
    kmer_frequencies,
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


def test_kmer_frequencies_normalize_valid_windows():
    features = kmer_frequencies("ACGT", k=2)
    assert features["kmer_2_AC"] == 0.3333
    assert features["kmer_2_CG"] == 0.3333
    assert features["kmer_2_GT"] == 0.3333
    assert features["kmer_2_AA"] == 0.0


def test_extract_features_motif_kmer_mode_adds_kmer_features():
    features = extract_features("ACGTCCAATTTTTTTTATAAAGGGCGGAATAAA", feature_mode="motif_kmer", kmer_k=2)
    assert features["motif_count"] >= 4
    assert "kmer_2_AC" in features
    assert "kmer_2_TA" in features
    assert "kmer_2_GC" in features


def test_classifier_baseline_demo_dataset_runs_with_explicit_split():
    records = parse_labeled_sequences_tsv(Path("examples/eco_labeled_sequences.tsv"))
    assert len(records) >= 20

    train_records, test_records = split_train_test(records)
    assert len(train_records) >= 12
    assert len(test_records) >= 8
    assert {record.label for record in train_records} == {"non_regulatory", "regulatory"}
    assert {record.label for record in test_records} == {"non_regulatory", "regulatory"}
    assert any("amb" in record.sequence_id for record in records)

    centroids = train_centroid_classifier(train_records)
    assert set(centroids) == {"non_regulatory", "regulatory"}

    report = build_classifier_report(records)
    assert report["model_type"] == "centroid_baseline_explicable"
    assert report["feature_mode"] == "motif"
    assert report["data_split"]["train"] == len(train_records)
    assert report["data_split"]["test"] == len(test_records)
    assert report["train_evaluation"]["total"] == len(train_records)
    assert report["test_evaluation"]["total"] == len(test_records)
    assert 0.0 <= report["test_evaluation"]["accuracy"] <= 1.0


def test_classifier_baseline_v2_reports_kmer_mode():
    records = parse_labeled_sequences_tsv(Path("examples/eco_labeled_sequences.tsv"))
    report = build_classifier_report(records, feature_mode="motif_kmer", kmer_k=2)

    assert report["model_type"] == "centroid_baseline_motif_kmer"
    assert report["feature_mode"] == "motif_kmer"
    assert report["kmer_k"] == 2
    assert report["test_evaluation"]["total"] >= 8
    first_prediction = report["test_evaluation"]["predictions"][0]
    assert any(key.startswith("kmer_2_") for key in first_prediction["features"])


def test_classifier_baseline_reports_per_class_metrics():
    records = parse_labeled_sequences_tsv(Path("examples/eco_labeled_sequences.tsv"))
    _, test_records = split_train_test(records)
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

    assert test_metrics["macro_avg"]["support"] == len(test_records)
    assert 0.0 <= test_metrics["macro_avg"]["f1"] <= 1.0
    assert test_metrics["weighted_avg"]["support"] == len(test_records)
    assert 0.0 <= test_metrics["weighted_avg"]["f1"] <= 1.0


def test_write_json_report_allows_existing_output_directory(tmp_path):
    output_dir = tmp_path / "results"
    output_dir.mkdir()
    output_path = output_dir / "classifier_report.json"
    payload = {"status": "ok", "stage": "classifier-baseline"}

    write_json_report(payload, output_path)

    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == payload
