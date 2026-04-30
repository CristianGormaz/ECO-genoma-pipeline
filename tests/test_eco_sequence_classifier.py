from pathlib import Path

from src.eco_sequence_classifier import (
    build_classifier_report,
    extract_features,
    parse_labeled_sequences_tsv,
    train_centroid_classifier,
)


def test_extract_features_detects_basic_motifs():
    features = extract_features("ACGTCCAATTTTTTTTATAAAGGGCGGAATAAA")
    assert features["motif_count"] >= 4
    assert features["has_tata"] == 1.0
    assert features["has_caat"] == 1.0
    assert features["has_gc_box"] == 1.0
    assert features["has_polya"] == 1.0


def test_classifier_baseline_demo_dataset_runs():
    records = parse_labeled_sequences_tsv(Path("examples/eco_labeled_sequences.tsv"))
    assert len(records) == 8
    centroids = train_centroid_classifier(records)
    assert set(centroids) == {"non_regulatory", "regulatory"}

    report = build_classifier_report(records)
    assert report["model_type"] == "centroid_baseline_explicable"
    assert report["evaluation"]["total"] == 8
    assert report["evaluation"]["accuracy"] >= 0.75
