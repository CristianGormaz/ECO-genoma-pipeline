from scripts.compare_eco_classifier_baselines import (
    build_html,
    build_markdown,
    compare_rows,
    interpretation,
    summarize_report,
)
from src.eco_sequence_classifier import build_classifier_report, parse_labeled_sequences_tsv


def _reports():
    records = parse_labeled_sequences_tsv("examples/eco_labeled_sequences.tsv")
    v1_report = build_classifier_report(records, feature_mode="motif")
    v2_report = build_classifier_report(records, feature_mode="motif_kmer", kmer_k=2, normalize_features=True)
    v3_report = build_classifier_report(records, feature_mode="motif_kmer", kmer_k=3, normalize_features=True)
    return v1_report, v2_report, v3_report


def test_summarize_report_extracts_comparable_fields():
    v1_report, v2_report, v3_report = _reports()
    v1 = summarize_report("baseline_v1", v1_report)
    v2 = summarize_report("baseline_v2", v2_report)
    v3 = summarize_report("baseline_v3", v3_report)

    assert v1["name"] == "baseline_v1"
    assert v1["feature_mode"] == "motif"
    assert v1["feature_scaling"] == "none"
    assert v1["kmer_k"] == "no_aplica"
    assert v2["name"] == "baseline_v2"
    assert v2["feature_mode"] == "motif_kmer"
    assert v2["feature_scaling"] == "minmax_train"
    assert v2["kmer_k"] == 2
    assert v3["name"] == "baseline_v3"
    assert v3["feature_mode"] == "motif_kmer"
    assert v3["feature_scaling"] == "minmax_train"
    assert v3["kmer_k"] == 3
    assert v1["test"] >= 8
    assert v1["test"] == v2["test"] == v3["test"]
    assert 0.0 <= v1["test_macro_f1"] <= 1.0
    assert 0.0 <= v2["test_macro_f1"] <= 1.0
    assert 0.0 <= v3["test_macro_f1"] <= 1.0


def test_compare_rows_contains_v1_v2_and_v3():
    v1_report, v2_report, v3_report = _reports()
    v1 = summarize_report("baseline_v1", v1_report)
    v2 = summarize_report("baseline_v2", v2_report)
    v3 = summarize_report("baseline_v3", v3_report)
    rows = compare_rows([v1, v2, v3])

    assert len(rows) == 3
    assert rows[0][0] == "baseline_v1"
    assert rows[1][0] == "baseline_v2"
    assert rows[2][0] == "baseline_v3"
    assert rows[0][2] == "motif"
    assert rows[1][2] == "motif_kmer"
    assert rows[2][2] == "motif_kmer"
    assert rows[0][3] == "none"
    assert rows[1][3] == "minmax_train"
    assert rows[2][3] == "minmax_train"


def test_comparison_markdown_and_html_include_prudent_reading():
    v1_report, v2_report, v3_report = _reports()
    v1 = summarize_report("baseline_v1", v1_report)
    v2 = summarize_report("baseline_v2", v2_report)
    v3 = summarize_report("baseline_v3", v3_report)

    reading = interpretation(v1, v2, v3)
    markdown = build_markdown(v1, v2, v3)
    html = build_html(v1, v2, v3)

    assert "Comparación de baselines" in markdown
    assert "baseline_v1" in markdown
    assert "baseline_v2" in markdown
    assert "baseline_v3" in markdown
    assert "Scaling" in markdown
    assert "minmax_train" in markdown
    assert reading in markdown
    assert "E.C.O. - Comparación de baselines" in html
    assert "baseline_v1" in html
    assert "baseline_v2" in html
    assert "baseline_v3" in html
    assert "minmax_train" in html
