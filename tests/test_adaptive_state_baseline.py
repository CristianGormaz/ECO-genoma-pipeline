from src.eco_core import (
    DEFAULT_TRANSITION_PACKETS,
    baseline_report_to_markdown,
    build_adaptive_state_rows,
    evaluate_state_transition_baseline,
    feature_key,
    train_state_transition_baseline,
)


def test_state_transition_baseline_trains_from_adaptive_rows():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    model = train_state_transition_baseline(rows)

    assert model.training_rows == 4
    assert model.default_state in {"stable", "watch", "attention"}
    assert len(model.transition_table) >= 3
    assert len(model.digestive_table) >= 3
    assert len(model.defense_table) >= 3
    assert feature_key(rows[0]) in model.transition_table


def test_state_transition_baseline_predicts_known_rows():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    model = train_state_transition_baseline(rows)
    prediction = model.predict(rows[0])

    assert prediction.source == "valid_sequence"
    assert prediction.observed_state == rows[0].state_after
    assert prediction.predicted_state == rows[0].state_after
    assert prediction.matched_rule == "feature_key"
    assert prediction.correct is True


def test_state_transition_baseline_report_is_auditable():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    report = evaluate_state_transition_baseline(rows)

    assert report["model_name"] == "adaptive_state_baseline_v0_hierarchical"
    assert report["training_rows"] == 4
    assert report["accuracy_demo"] == 1.0
    assert report["digestive_rule_count"] >= 3
    assert report["defense_rule_count"] >= 3
    assert len(report["predictions"]) == 4
    assert "no representa desempeño general" in report["responsible_limit"]


def test_state_transition_baseline_markdown_mentions_limits():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    report = evaluate_state_transition_baseline(rows)
    markdown = baseline_report_to_markdown(report)

    assert "Baseline adaptativo E.C.O. v0" in markdown
    assert "Reglas digestivas aprendidas" in markdown
    assert "Reglas defensivas aprendidas" in markdown
    assert "Accuracy demostrativa" in markdown
    assert "valid_sequence" in markdown
    assert "no representa desempeño general" in markdown
