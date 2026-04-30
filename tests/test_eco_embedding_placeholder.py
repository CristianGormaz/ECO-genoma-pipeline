from pathlib import Path

from scripts.run_eco_embedding_placeholder import (
    build_embedding_report,
    build_placeholder_embedding,
    kmer_index,
)
from src.eco_sequence_classifier import parse_labeled_sequences_tsv


def test_kmer_index_encodes_dna_windows_base4():
    assert kmer_index("AAA") == 0
    assert kmer_index("AAC") == 1
    assert kmer_index("AAG") == 2
    assert kmer_index("AAT") == 3
    assert kmer_index("TTT") == 63


def test_placeholder_embedding_normalizes_valid_kmer_windows():
    vector = build_placeholder_embedding("AAACCC", k=3, dimensions=64)

    assert len(vector) == 64
    assert round(sum(vector.values()), 6) == 1.0
    assert vector[f"embed_{kmer_index('AAA'):02d}"] == 0.25
    assert vector[f"embed_{kmer_index('AAC'):02d}"] == 0.25
    assert vector[f"embed_{kmer_index('ACC'):02d}"] == 0.25
    assert vector[f"embed_{kmer_index('CCC'):02d}"] == 0.25


def test_embedding_placeholder_report_keeps_comparison_contract():
    records = parse_labeled_sequences_tsv(Path("examples/eco_labeled_sequences.tsv"))
    report = build_embedding_report(records, k=3, dimensions=64)

    embedding = report["embedding_report"]
    assert embedding["embedding_type"] == "kmer_frequency_placeholder"
    assert embedding["embedding_k"] == 3
    assert embedding["embedding_dimensions"] == 64
    assert embedding["feature_scaling"] == "minmax_train"

    comparison_models = {row["model"] for row in report["comparison"]}
    assert comparison_models == {"baseline_v1", "baseline_v3", "embedding_placeholder"}
    assert report["best_model_by_test_macro_f1"]["model"] in comparison_models

    macro_f1 = embedding["test_evaluation"]["classification_metrics"]["macro_avg"]["f1"]
    assert 0.0 <= macro_f1 <= 1.0
    assert embedding["test_evaluation"]["total"] > 0
