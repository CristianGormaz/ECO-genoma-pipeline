from src.eco_core import EntericSystem


def test_enteric_system_stores_defense_signal_for_valid_sequence():
    system = EntericSystem()

    packet = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    defense = packet.metadata["enteric_defense_signal"]
    assert defense["category"] == "none"
    assert defense["severity"] == "none"
    assert defense["should_alert"] is False
    assert defense["recommended_action"] == "continue"
    assert any(log.stage == "enteric_defense" for log in packet.history)


def test_enteric_system_stores_high_defense_signal_for_invalid_sequence():
    system = EntericSystem()

    packet = system.process_dna_sequence("ACGTXYZ", source="invalid_sequence")

    defense = packet.metadata["enteric_defense_signal"]
    assert defense["category"] == "invalid_payload"
    assert defense["severity"] == "high"
    assert defense["should_alert"] is True
    assert defense["recommended_action"] == "discard"


def test_enteric_system_stores_redundant_defense_signal_for_duplicate_sequence():
    system = EntericSystem()

    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="first_sequence")
    packet = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="duplicate_sequence")

    defense = packet.metadata["enteric_defense_signal"]
    assert defense["category"] == "redundant_payload"
    assert defense["severity"] == "low"
    assert defense["should_alert"] is False
    assert defense["recommended_action"] == "discard_duplicate"


def test_enteric_system_stores_retained_defense_signal_for_short_sequence():
    system = EntericSystem(min_length=6)

    packet = system.process_dna_sequence("ACG", source="short_sequence")

    defense = packet.metadata["enteric_defense_signal"]
    assert defense["category"] == "retained_payload"
    assert defense["severity"] == "medium"
    assert defense["should_alert"] is True
    assert defense["recommended_action"] == "quarantine"
