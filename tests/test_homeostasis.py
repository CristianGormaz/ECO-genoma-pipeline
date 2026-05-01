from src.eco_core import EntericSystem
from src.eco_core.homeostasis import build_homeostasis_snapshot, safe_ratio


def test_safe_ratio_handles_zero_total():
    assert safe_ratio(1, 0) == 0.0


def test_homeostasis_snapshot_reports_idle_without_packets():
    snapshot = build_homeostasis_snapshot([])

    assert snapshot.total_packets == 0
    assert snapshot.state == "idle"
    assert snapshot.needs_attention is False
    assert snapshot.notes == ("Sin paquetes procesados.",)


def test_homeostasis_snapshot_reports_stable_absorption_flow():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_one")
    system.process_dna_sequence("TTTTCCAATGGGCGG", source="valid_two")

    snapshot = build_homeostasis_snapshot(system.processed_packets)

    assert snapshot.total_packets == 2
    assert snapshot.absorbed_packets == 2
    assert snapshot.absorption_ratio == 1.0
    assert snapshot.state == "stable"
    assert snapshot.needs_attention is False


def test_homeostasis_snapshot_reports_attention_for_quarantine_load():
    system = EntericSystem(min_length=6)
    system.process_dna_sequence("ACG", source="short_one")
    system.process_dna_sequence("TTA", source="short_two")
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid")

    snapshot = build_homeostasis_snapshot(system.processed_packets)

    assert snapshot.total_packets == 3
    assert snapshot.quarantined_packets == 2
    assert snapshot.quarantine_ratio == 0.6667
    assert snapshot.state == "attention"
    assert snapshot.needs_attention is True


def test_homeostasis_snapshot_reports_overload_for_invalid_flow():
    system = EntericSystem()
    system.process_dna_sequence("ACGTXYZ", source="bad_one")
    system.process_dna_sequence("TTTXYZ", source="bad_two")
    system.process_dna_sequence("GGGXYZ", source="bad_three")

    snapshot = build_homeostasis_snapshot(system.processed_packets)

    assert snapshot.total_packets == 3
    assert snapshot.rejected_packets == 3
    assert snapshot.immune_load >= 1.0
    assert snapshot.state == "overload"
    assert snapshot.needs_attention is True


def test_homeostasis_snapshot_detects_recurrence_from_duplicates():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="first")
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="duplicate")

    snapshot = build_homeostasis_snapshot(system.processed_packets)

    assert snapshot.duplicate_packets == 1
    assert snapshot.recurrence_ratio == 0.5
    assert any("Recurrencia detectada" in note for note in snapshot.notes)
