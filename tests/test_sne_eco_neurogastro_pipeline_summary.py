from scripts.run_sne_eco_neurogastro_pipeline_summary import build_summary, to_markdown


def test_neurogastro_pipeline_summary_reports_attention_without_route_confusion():
    summary = build_summary(
        dashboard_payload={
            "status": "green",
            "confused_routes": 0,
            "confused_recurrence_rows": 0,
            "default_state_confused_routes": 0,
        },
        neurogastro_payload={
            "status": "attention",
            "metrics": {"rows_evaluated": 4},
            "ux_reading": {
                "suggested_action": "auditar defensa, barrera, rutas confundidas y límites responsables"
            },
            "responsible_limit": "Reporte técnico/educativo; lectura del pipeline.",
        },
        recurrence_payload={"recurrence_rows": 7, "confused_recurrence_rows": 0},
    )

    assert summary["status"] == "attention"
    assert summary["dashboard_status"] == "green"
    assert summary["metrics"]["rows_evaluated"] == 4
    assert summary["metrics"]["confused_routes"] == 0
    assert summary["metrics"]["confused_recurrence_rows"] == 0
    assert summary["metrics"]["recurrence_rows"] == 7
    assert summary["stability_locks"]["summary_only"] is True
    assert summary["stability_locks"]["baseline_modified"] is False
    assert "tensión interna" in summary["cause"]
    assert "auditar defensa" in summary["suggested_action"]


def test_neurogastro_pipeline_summary_prioritizes_confusion_over_attention():
    summary = build_summary(
        dashboard_payload={
            "status": "red",
            "confused_routes": 1,
            "confused_recurrence_rows": 1,
            "default_state_confused_routes": 1,
        },
        neurogastro_payload={
            "status": "attention",
            "metrics": {"rows_evaluated": 4},
            "ux_reading": {"suggested_action": "auditar defensa"},
        },
        recurrence_payload={"recurrence_rows": 7, "confused_recurrence_rows": 1},
    )

    assert summary["metrics"]["confused_routes"] == 1
    assert summary["metrics"]["confused_recurrence_rows"] == 1
    assert "rutas o recurrencias confundidas" in summary["cause"]
    assert "comparar contra RC1" in summary["suggested_action"]


def test_neurogastro_pipeline_summary_markdown_is_executive_and_safe():
    summary = build_summary(
        dashboard_payload={
            "status": "green",
            "confused_routes": 0,
            "confused_recurrence_rows": 0,
            "default_state_confused_routes": 0,
        },
        neurogastro_payload={
            "status": "stable",
            "metrics": {"rows_evaluated": 4},
            "ux_reading": {"suggested_action": "mantener observación y registrar métricas"},
            "responsible_limit": "Resumen técnico/educativo; lectura del pipeline.",
        },
        recurrence_payload={"recurrence_rows": 7, "confused_recurrence_rows": 0},
    )

    markdown = to_markdown(summary)

    assert "Resumen ejecutivo neurogastrocomputacional S.N.E.-E.C.O." in markdown
    assert "Estado general: 🟢 `stable`" in markdown
    assert "Rutas confundidas" in markdown
    assert "Recurrencias confundidas" in markdown
    assert "Baseline modificado: `False`" in markdown
    assert "Solo resumen: `True`" in markdown
    assert "Resumen técnico/educativo" in markdown
