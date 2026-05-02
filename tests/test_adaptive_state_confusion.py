from src.eco_core import (
    EXTENDED_TRANSITION_PACKETS,
    analyze_confused_routes,
    build_adaptive_state_rows,
    confused_routes_to_markdown,
)


def test_confused_route_analysis_finds_holdout_failures():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    report = analyze_confused_routes(rows)

    assert report.test_rows >= 6
    assert report.confused_routes
    assert report.suggested_focus
    assert "no representa desempeño general" in report.responsible_limit


def test_confused_route_analysis_uses_hierarchical_fallback_before_default_state():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    report = analyze_confused_routes(rows)

    default_routes = [route for route in report.confused_routes if route.matched_rule == "default_state"]
    hierarchical_routes = [
        route
        for route in report.confused_routes
        if route.matched_rule in {"digestive_key", "defense_key"}
    ]

    assert not default_routes
    assert hierarchical_routes
    assert all("add_training_route" not in route.suggested_scenario for route in hierarchical_routes)


def test_confused_route_report_to_dict_and_markdown_are_actionable():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    report = analyze_confused_routes(rows)
    payload = report.to_dict()
    markdown = confused_routes_to_markdown(report)

    assert payload["test_rows"] >= 6
    assert "confused_routes" in payload
    assert "suggested_focus" in payload
    assert "Análisis de rutas confundidas E.C.O." in markdown
    assert "Focos sugeridos" in markdown
    assert "suggested_scenario" in markdown
