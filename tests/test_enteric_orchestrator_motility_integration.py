from src.eco_core import EntericSystem


def test_enteric_system_stores_myenteric_motility_decision_for_valid_sequence():
    system = EntericSystem()

    packet = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    motility = packet.metadata["myenteric_motility_decision"]
    assert motility["action"] == "advance"
    assert motility["status"] == "ok"
    assert motility["route"] == "submucosal_absorption"
    assert motility["transit_score"] == 0.95
    assert packet.metadata["enteric_decision"]["action"] == "absorb"


def test_enteric_system_routes_heavy_payload_through_batch_flow():
    system = EntericSystem(heavy_payload_threshold=8)

    packet = system.process_dna_sequence("ACGTACGT", source="heavy_sequence")

    motility = packet.metadata["myenteric_motility_decision"]
    assert motility["action"] == "batch_advance"
    assert packet.metadata["enteric_decision"]["action"] == "batch_absorb"
    assert packet.metadata["batch_recommended"] is True
    assert any(log.stage == "enteric_batch_flow" for log in packet.history)


def test_enteric_system_uses_myenteric_motility_for_duplicate_discard():
    system = EntericSystem()

    first = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="first_sequence")
    second = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="duplicate_sequence")

    assert first.metadata["myenteric_motility_decision"]["action"] == "advance"
    assert second.metadata["myenteric_motility_decision"]["action"] == "discard_duplicate"
    assert second.metadata["enteric_decision"]["action"] == "discard_duplicate"
    assert second.metadata["discard_reason"].startswith("Secuencia duplicada")


def test_enteric_system_uses_myenteric_motility_for_quarantine():
    system = EntericSystem(min_length=6)

    packet = system.process_dna_sequence("ACG", source="short_sequence")

    assert packet.metadata["myenteric_motility_decision"]["action"] == "quarantine"
    assert packet.metadata["enteric_decision"]["action"] == "quarantine"
    assert "quarantine_reason" in packet.metadata
