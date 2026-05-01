from src.eco_core.enteric_orchestrator import EntericSystem as IntegratedEntericSystem
from src.eco_core.enteric_system import EntericSystem as CompatibleEntericSystem


def test_enteric_system_wrapper_preserves_legacy_import():
    assert CompatibleEntericSystem is IntegratedEntericSystem


def test_enteric_system_sense_delegates_to_submucosal_sensor():
    system = CompatibleEntericSystem(heavy_payload_threshold=8)

    packet = system.ingest("ACGTACGT", source="delegation_test", packet_type="dna")
    profile = system.sense(packet)

    assert profile["source"] == "delegation_test"
    assert profile["packet_type"] == "dna"
    assert profile["payload_key"] == "ACGTACGT"
    assert profile["is_heavy"] is True
    assert isinstance(profile["invalid_characters"], list)


def test_enteric_system_sense_uses_microbiome_memory_for_duplicates():
    system = CompatibleEntericSystem()

    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="first")
    second_packet = system.ingest("ACGTCCAATGGTATAAA", source="second", packet_type="dna")
    profile = system.sense(second_packet)

    assert profile["is_duplicate"] is True
    assert profile["payload_key"] == "ACGTCCAATGGTATAAA"
