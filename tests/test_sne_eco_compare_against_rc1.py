from scripts.run_sne_eco_compare_against_rc1 import build_comparison, to_markdown


def test_compare_against_rc1_reports_green_when_current_improves_tests_and_stays_clean():
    comparison = build_comparison(
        dashboard_payload={
            "tests_passed": 156,
            "confused_routes": 0,
            "confused_recurrence_rows": 0,
            "default_state_confused_routes": 0,
            "status": "green",
        }
    )

    assert comparison["status"] == "green"
    assert comparison["deltas"]["tests_passed"] == 3
    assert comparison["deltas"]["confused_routes"] == 0
    assert comparison["regressions"] == []
    assert comparison["baseline"]["tag"] == "sne-eco-v1.0-rc1"


def test_compare_against_rc1_reports_red_when_confusion_regresses():
    comparison = build_comparison(
        dashboard_payload={
            "tests_passed": 156,
            "confused_routes": 1,
            "confused_recurrence_rows": 1,
            "default_state_confused_routes": 1,
            "status": "red",
        }
    )

    assert comparison["status"] == "red"
    assert "confused_routes_increased" in comparison["regressions"]
    assert "confused_recurrence_rows_increased" in comparison["regressions"]
    assert "default_state_confused_routes_increased" in comparison["regressions"]
    assert "dashboard_red" in comparison["regressions"]


def test_compare_against_rc1_markdown_is_explainable():
    comparison = build_comparison(
        dashboard_payload={
            "tests_passed": 156,
            "confused_routes": 0,
            "confused_recurrence_rows": 0,
            "default_state_confused_routes": 0,
            "status": "green",
        }
    )
    markdown = to_markdown(comparison)

    assert "Comparación S.N.E.-E.C.O. contra RC1" in markdown
    assert "sne-eco-v1.0-rc1" in markdown
    assert "Sin regresiones respecto a RC1" in markdown
    assert "Tests passing" in markdown
