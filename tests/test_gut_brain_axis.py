from src.eco_core.gut_brain_axis import build_gut_brain_report
from src.eco_core.homeostasis import HomeostasisSnapshot


def make_snapshot(**overrides):
    data = {
        "total_packets": 10,
        "absorbed_packets": 8,
        "quarantined_packets": 0,
        "discarded_packets": 0,
        "rejected_packets": 0,
        "duplicate_packets": 0,
        "defense_alerts": 0,
        "absorption_ratio": 0.8,
        "immune_load": 0.0,
        "quarantine_ratio": 0.0,
        "recurrence_ratio": 0.0,
        "state": "stable",
        "notes": ("Homeostasis estable: flujo informacional dentro de rangos esperados.",),
    }
    data.update(overrides)
    return HomeostasisSnapshot(**data)


def test_gut_brain_report_summarizes_stable_state():
    report = build_gut_brain_report(make_snapshot())

    assert report.state == "stable"
    assert report.attention_required is False
    assert report.key_metrics["absorption_ratio"] == 0.8
    assert report.recommended_actions == ("Mantener flujo actual y registrar el estado como referencia estable.",)


def test_gut_brain_report_marks_attention_required():
    report = build_gut_brain_report(
        make_snapshot(
            absorbed_packets=3,
            rejected_packets=5,
            absorption_ratio=0.3,
            immune_load=0.5,
            state="attention",
            notes=("Alta respuesta inmune: revisar calidad de entrada.",),
        )
    )

    assert report.attention_required is True
    assert "requiere atención" in report.summary
    assert any("calidad de entrada" in action for action in report.recommended_actions)


def test_gut_brain_report_recommends_duplicate_review():
    report = build_gut_brain_report(
        make_snapshot(
            duplicate_packets=2,
            recurrence_ratio=0.2,
            notes=("Recurrencia detectada: la microbiota informacional identificó repetición.",),
        )
    )

    assert any("duplicados" in action for action in report.recommended_actions)


def test_gut_brain_report_renders_markdown():
    report = build_gut_brain_report(make_snapshot())
    markdown = report.to_markdown()

    assert markdown.startswith("# Reporte eje intestino-cerebro E.C.O.")
    assert "## Métricas clave" in markdown
    assert "## Acciones sugeridas" in markdown
    assert "`absorption_ratio`: 0.8" in markdown
