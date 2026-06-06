from pathlib import Path
import json

import pytest

from src.eco_sequence_classifier import (
    LabeledSequence,
    build_classifier_report,
    confidence_from_distances,
    extract_feature_map,
    extract_features,
    kmer_frequencies,
    parse_labeled_sequences_tsv,
    prediction_from_features,
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


def test_confidence_from_distances_returns_zero_for_exact_tie():
    confidence = confidence_from_distances({"regulatory": 0.0, "non_regulatory": 0.0})

    assert confidence == 0.0


def test_confidence_from_distances_preserves_non_ambiguous_margin():
    confidence = confidence_from_distances({"regulatory": 1.0, "non_regulatory": 2.0})

    assert confidence == 0.5


def test_parse_labeled_sequences_accepts_unique_sequence_ids(tmp_path):
    input_path = tmp_path / "unique_sequences.tsv"
    input_path.write_text(
        "sequence_id\tsequence\tlabel\tsplit\n"
        "seq_a\tAAAAAA\tregulatory\ttrain\n"
        "seq_b\tGGGCGG\tnon_regulatory\ttest\n",
        encoding="utf-8",
    )

    records = parse_labeled_sequences_tsv(input_path)

    assert [record.sequence_id for record in records] == ["seq_a", "seq_b"]


def test_parse_labeled_sequences_rejects_duplicate_sequence_id(tmp_path):
    input_path = tmp_path / "duplicate_sequences.tsv"
    input_path.write_text(
        "sequence_id\tsequence\tlabel\tsplit\n"
        "dup\tAAAAAA\tregulatory\ttrain\n"
        "dup\tGGGCGG\tnon_regulatory\ttest\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="sequence_id único: dup"):
        parse_labeled_sequences_tsv(input_path)


def test_extract_feature_map_rejects_duplicate_sequence_id():
    records = [
        LabeledSequence(sequence_id="dup", sequence="AAAAAA", label="regulatory"),
        LabeledSequence(sequence_id="dup", sequence="GGGCGG", label="non_regulatory"),
    ]

    with pytest.raises(ValueError, match="sequence_id único: dup"):
        extract_feature_map(records)


def test_training_rejects_duplicate_sequence_id_before_centroids():
    records = [
        LabeledSequence(sequence_id="dup", sequence="AAAAAA", label="regulatory", split="train"),
        LabeledSequence(sequence_id="train_ok", sequence="GGGCGG", label="non_regulatory", split="train"),
        LabeledSequence(sequence_id="dup", sequence="TTTTTT", label="regulatory", split="test"),
    ]

    with pytest.raises(ValueError, match="sequence_id único: dup"):
        build_classifier_report(records)


def test_prediction_from_features_uses_raw_distances_to_break_rounded_tie():
    record = LabeledSequence(sequence_id="seq_tie_margin", sequence="A", label="regulatory")
    features = {"axis": 0.0}
    centroids = {
        "non_regulatory": {"axis": 0.000049},
        "regulatory": {"axis": 0.000041},
    }

    prediction = prediction_from_features(record, features, centroids)

    assert prediction.predicted_label == "regulatory"
    assert prediction.confidence == 0.1633
    assert prediction.distances == {"non_regulatory": 0.0, "regulatory": 0.0}


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
