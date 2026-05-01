from src.eco_core import (
    DEFAULT_TRANSITION_PACKETS,
    build_adaptive_state_rows,
    evaluate_state_transition_holdout,
    holdout_report_to_markdown,
    split_rows_holdout,
)


def test_split_rows_holdout_uses_even_rows_for_training_and_odd_for_test():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    train, test = split_rows_holdout(rows)

    assert len(train) == 2
    assert len(test) == 2
    assert [row.source for row in train] == ["valid_sequence", "short_sequence"]
    assert [row.source for row in test] == ["invalid_sequence", "duplicate_sequence"]


def test_holdout_evaluation_reports_generalization_gap_on_minimal_dataset():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)

    assert evaluation.model_name == "adaptive_state_baseline_v0_holdout"
    assert evaluation.training_rows == 2
    assert evaluation.test_rows == 2
    assert 0.0 <= evaluation.accuracy_holdout <= 1.0
    assert 0.0 <= evaluation.macro_f1_holdout <= 1.0
    assert evaluation.predictions
    assert any(prediction.matched_rule == "default_state" for prediction in evaluation.predictions)
    assert "no representa desempeño general" in evaluation.responsible_limit


def test_holdout_evaluation_to_dict_contains_confusion_matrix():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)
    payload = evaluation.to_dict()

    assert payload["training_rows"] == 2
    assert payload["test_rows"] == 2
    assert "confusion_matrix" in payload
    assert "predictions" in payload
    assert len(payload["predictions"]) == 2


def test_holdout_report_markdown_mentions_matrix_and_limit():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)
    markdown = holdout_report_to_markdown(evaluation)

    assert "Evaluación holdout del baseline adaptativo E.C.O. v0" in markdown
    assert "Accuracy holdout" in markdown
    assert "Macro-F1 holdout" in markdown
    assert "Matriz de confusión" in markdown
    assert "no representa desempeño general" in markdown
