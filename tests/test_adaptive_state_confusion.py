from src.eco_core import (
    EXTENDED_TRANSITION_PACKETS,
    analyze_confused_routes,
    build_adaptive_state_rows,
    confused_routes_to_markdown,
)


def test_confused_route_analysis_runs_on_extended_holdout():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    report = analyze_confused_routes(rows)

    assert report.test_rows >= 6
    assert isinstance(report.confused_routes, tuple)
    assert isinstance(report.suggested_focus, tuple)
    assert "no representa desempeño general" in report.responsible_limit


def test_confused_route_analysis_avoids_default_state_after_recurrence_guard():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    report = analyze_confused_routes(rows)

    default_routes = [route for route in report.confused_routes if route.matched_rule == "default_state"]

    assert not default_routes
    assert len(report.confused_routes) == 0
    assert report.suggested_focus == ()


def test_confused_route_report_to_dict_and_markdown_are_actionable():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    report = analyze_confused_routes(rows)
    payload = report.to_dict()
    markdown = confused_routes_to_markdown(report)

    assert payload["test_rows"] >= 6
    assert "confused_routes" in payload
    assert "suggested_focus" in payload
    assert payload["confused_routes"] == []
    assert not payload["suggested_focus"]
    assert "Análisis de rutas confundidas E.C.O." in markdown
    assert "Focos sugeridos" in markdown
    assert "Sin rutas confundidas relevantes" in markdown
