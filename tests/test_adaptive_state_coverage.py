from src.eco_core import (
    EXTENDED_TRANSITION_PACKETS,
    build_adaptive_state_rows,
    build_coverage_diagnostics,
    coverage_report_to_markdown,
    evaluate_state_transition_holdout,
)


def test_coverage_diagnostics_counts_extended_routes():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)
    diagnostics = build_coverage_diagnostics(rows, evaluation=evaluation)

    assert diagnostics.row_count == len(EXTENDED_TRANSITION_PACKETS)
    assert diagnostics.unique_feature_routes >= 6
    assert diagnostics.state_counts["stable"] >= 3
    assert diagnostics.state_counts["watch"] >= 2
    assert diagnostics.state_counts["attention"] >= 3
    assert diagnostics.fallback_predictions >= 0
    assert diagnostics.incorrect_predictions >= 0


def test_coverage_diagnostics_warns_about_fallback_or_errors():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)
    diagnostics = build_coverage_diagnostics(rows, evaluation=evaluation)

    assert diagnostics.coverage_warnings
    assert any("predictions" in warning for warning in diagnostics.coverage_warnings)
    assert "no representa desempeño general" in diagnostics.responsible_limit


def test_coverage_diagnostics_to_dict_and_markdown_are_explainable():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)
    diagnostics = build_coverage_diagnostics(rows, evaluation=evaluation)
    payload = diagnostics.to_dict()
    markdown = coverage_report_to_markdown(diagnostics)

    assert payload["row_count"] == len(EXTENDED_TRANSITION_PACKETS)
    assert "decision_counts" in payload
    assert "defense_counts" in payload
    assert "Diagnóstico de cobertura adaptativa E.C.O." in markdown
    assert "Advertencias accionables" in markdown
    assert "Límite responsable" in markdown
