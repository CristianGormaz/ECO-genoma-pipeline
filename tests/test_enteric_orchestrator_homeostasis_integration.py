from src.eco_core import EntericSystem
from src.eco_core.homeostasis import build_homeostasis_snapshot


def test_enteric_system_homeostasis_delegates_to_snapshot_module():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    report = system.homeostasis_report()
    snapshot = build_homeostasis_snapshot(system.processed_packets)

    assert report.total_packets == snapshot.total_packets
    assert report.absorbed_packets == snapshot.absorbed_packets
    assert report.quarantined_packets == snapshot.quarantined_packets
    assert report.discarded_packets == snapshot.discarded_packets
    assert report.rejected_packets == snapshot.rejected_packets
    assert report.duplicate_packets == snapshot.duplicate_packets
    assert report.state == snapshot.state
    assert report.notes == list(snapshot.notes)


def test_enteric_system_homeostasis_reports_overload_from_defense_layer():
    system = EntericSystem()
    system.process_dna_sequence("ACGTXYZ", source="bad_one")
    system.process_dna_sequence("TTTXYZ", source="bad_two")

    report = system.homeostasis_report()

    assert report.total_packets == 2
    assert report.rejected_packets == 2
    assert report.state == "overload"
    assert any("Sobrecarga defensiva" in note for note in report.notes)


def test_enteric_system_homeostasis_preserves_idle_compatibility():
    system = EntericSystem()

    report = system.homeostasis_report()

    assert report.total_packets == 0
    assert report.state == "idle"
    assert report.notes == ["Sin paquetes procesados."]
