from scripts.run_sne_eco_observability_dashboard import build_dashboard, to_markdown


def test_observability_dashboard_reports_green_state_for_clean_payloads():
    confusion_payload = {
        "scenario_set": "extended",
        "test_rows": 14,
        "confused_routes": [],
        "suggested_focus": [],
    }
    recurrence_payload = {
        "recurrence_rows": 7,
        "confused_recurrence_rows": 0,
        "rows": [{"is_confused": False}],
    }

    dashboard = build_dashboard(
        confusion_payload=confusion_payload,
        recurrence_payload=recurrence_payload,
        tests_passed=153,
    )

    assert dashboard["status"] == "green"
    assert dashboard["tests_passed"] == 153
    assert dashboard["confused_routes"] == 0
    assert dashboard["confused_recurrence_rows"] == 0
    assert dashboard["default_state_confused_routes"] == 0
    assert "no recalibra reglas" in dashboard["responsible_limit"]


def test_observability_dashboard_reports_red_state_when_confusion_exists():
    confusion_payload = {
        "scenario_set": "extended",
        "test_rows": 14,
        "confused_routes": [
            {"source": "x", "matched_rule": "default_state"},
        ],
        "suggested_focus": ["add_training_route:x"],
    }
    recurrence_payload = {
        "recurrence_rows": 7,
        "confused_recurrence_rows": 1,
        "rows": [{"is_confused": True}],
    }

    dashboard = build_dashboard(
        confusion_payload=confusion_payload,
        recurrence_payload=recurrence_payload,
        tests_passed=152,
    )

    assert dashboard["status"] == "red"
    assert dashboard["confused_routes"] == 1
    assert dashboard["confused_recurrence_rows"] == 1
    assert dashboard["default_state_confused_routes"] == 1
    assert dashboard["suggested_focus"] == ["add_training_route:x"]


def test_observability_dashboard_markdown_is_explainable():
    dashboard = build_dashboard(
        confusion_payload={
            "scenario_set": "extended",
            "test_rows": 14,
            "confused_routes": [],
            "suggested_focus": [],
        },
        recurrence_payload={
            "recurrence_rows": 7,
            "confused_recurrence_rows": 0,
            "rows": [],
        },
        tests_passed=153,
    )
    markdown = to_markdown(dashboard)

    assert "Dashboard de observabilidad S.N.E.-E.C.O." in markdown
    assert "Estado: 🟢 `green`" in markdown
    assert "Rutas confundidas" in markdown
    assert "Sin focos activos" in markdown
    assert "no ejecuta nuevas reglas" in markdown
