from src.eco_core import GutBrainReport, build_gut_brain_report
from src.eco_core.homeostasis import HomeostasisSnapshot


def test_gut_brain_report_is_available_from_public_core_api():
    snapshot = HomeostasisSnapshot(
        total_packets=0,
        absorbed_packets=0,
        quarantined_packets=0,
        discarded_packets=0,
        rejected_packets=0,
        duplicate_packets=0,
        defense_alerts=0,
        absorption_ratio=0.0,
        immune_load=0.0,
        quarantine_ratio=0.0,
        recurrence_ratio=0.0,
        state="idle",
        notes=("Sin paquetes procesados.",),
    )

    report = build_gut_brain_report(snapshot)

    assert isinstance(report, GutBrainReport)
    assert report.state == "idle"
    assert report.attention_required is False
    assert "Reporte eje intestino-cerebro E.C.O." in report.to_markdown()
