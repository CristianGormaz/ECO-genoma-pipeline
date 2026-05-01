from src.eco_core import EntericSystem


def test_enteric_system_absorbs_valid_dna_sequence():
    system = EntericSystem()

    packet = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    assert packet.metadata["enteric_decision"]["action"] == "absorb"
    assert "absorbed_features" in packet.metadata
    assert packet.metadata["absorbed_features"]["length"] == 17
    assert any(log.stage == "absorption" for log in packet.history)


def test_enteric_system_rejects_invalid_characters():
    system = EntericSystem()

    packet = system.process_dna_sequence("ACGTXYZ", source="invalid_sequence")

    assert packet.metadata["enteric_decision"]["action"] == "reject"
    assert packet.metadata["discard_reason"].startswith("Secuencia con caracteres no válidos")
    assert any(log.status == "discarded" for log in packet.history)


def test_enteric_system_quarantines_short_sequence():
    system = EntericSystem(min_length=6)

    packet = system.process_dna_sequence("ACG", source="short_sequence")

    assert packet.metadata["enteric_decision"]["action"] == "quarantine"
    assert "quarantine_reason" in packet.metadata
    assert "absorbed_features" not in packet.metadata
    assert any(log.stage == "enteric_quarantine" for log in packet.history)


def test_enteric_system_uses_microbiome_memory_to_discard_duplicates():
    system = EntericSystem()

    first = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="first_sequence")
    second = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="duplicate_sequence")

    assert first.metadata["enteric_decision"]["action"] == "absorb"
    assert second.metadata["enteric_decision"]["action"] == "discard_duplicate"
    assert second.metadata["microbiome_seen_count"] == 2
    assert second.metadata["discard_reason"].startswith("Secuencia duplicada")


def test_enteric_homeostasis_reports_stable_and_attention_states():
    stable_system = EntericSystem()
    stable_system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")
    stable_report = stable_system.homeostasis_report()

    assert stable_report.total_packets == 1
    assert stable_report.absorbed_packets == 1
    assert stable_report.state == "stable"

    attention_system = EntericSystem()
    attention_system.process_dna_sequence("ACGTXYZ", source="bad_one")
    attention_system.process_dna_sequence("TTTXYZ", source="bad_two")
    attention_report = attention_system.homeostasis_report()

    assert attention_report.total_packets == 2
    assert attention_report.rejected_packets == 2
    assert attention_report.state == "attention"
    assert any("Alta respuesta inmune" in note for note in attention_report.notes)
