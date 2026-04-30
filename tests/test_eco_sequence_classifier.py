from pathlib import Path

from src.eco_sequence_classifier import (
    build_classifier_report,
    extract_features,
    parse_labeled_sequences_tsv,
    split_train_test,
    train_centroid_classifier,
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
