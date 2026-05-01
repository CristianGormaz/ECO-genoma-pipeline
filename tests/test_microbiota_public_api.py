from src.eco_core import InformationalMicrobiota, MicrobiotaRecord, update_microbiota_memory


def test_microbiota_helpers_are_available_from_public_core_api():
    memory = {}

    record = update_microbiota_memory(
        memory,
        "ACGTCCAATGGTATAAA",
        packet_id="packet-1",
        source="public_api",
        action="absorb",
        status="ok",
    )

    assert isinstance(record, MicrobiotaRecord)
    assert record.seen_count == 1
    assert InformationalMicrobiota(memory).has_seen("ACGTCCAATGGTATAAA") is True
