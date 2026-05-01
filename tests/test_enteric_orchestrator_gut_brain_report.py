from src.eco_core import EntericSystem
from src.eco_core.gut_brain_axis import GutBrainReport
from src.eco_core.homeostasis import HomeostasisSnapshot


def test_enteric_system_builds_homeostasis_snapshot_from_processed_packets():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    snapshot = system.homeostasis_snapshot()

    assert isinstance(snapshot, HomeostasisSnapshot)
    assert snapshot.total_packets == 1
    assert snapshot.absorbed_packets == 1
    assert snapshot.state == "stable"


def test_enteric_system_builds_gut_brain_report():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    report = system.gut_brain_report()

    assert isinstance(report, GutBrainReport)
    assert report.title == "Reporte eje intestino-cerebro E.C.O."
    assert report.state == "stable"
    assert report.attention_required is False
    assert report.key_metrics["total_packets"] == 1


def test_enteric_system_exports_gut_brain_markdown():
    system = EntericSystem()
    system.process_dna_sequence("ACGTXYZ", source="invalid_sequence")

    markdown = system.gut_brain_markdown()

    assert "# Reporte eje intestino-cerebro E.C.O." in markdown
    assert "## Métricas clave" in markdown
    assert "immune_load" in markdown
    assert "## Acciones sugeridas" in markdown


def test_historical_homeostasis_report_still_works():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    legacy_report = system.homeostasis_report()
    snapshot = system.homeostasis_snapshot()

    assert legacy_report.total_packets == snapshot.total_packets
    assert legacy_report.absorbed_packets == snapshot.absorbed_packets
    assert legacy_report.state == "stable"
