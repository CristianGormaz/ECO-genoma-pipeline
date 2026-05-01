from src.eco_core.microbiota import InformationalMicrobiota, update_microbiota_memory


def test_microbiota_detects_payload_after_observation():
    microbiota = InformationalMicrobiota()

    assert microbiota.has_seen("ACGTCCAATGGTATAAA") is False

    record = microbiota.observe(
        "ACGTCCAATGGTATAAA",
        packet_id="packet-1",
        source="first",
        action="absorb",
        status="ok",
    )

    assert record.seen_count == 1
    assert record.is_recurrent is False
    assert microbiota.has_seen("ACGTCCAATGGTATAAA") is True


def test_microbiota_counts_repeated_payloads():
    microbiota = InformationalMicrobiota()

    microbiota.observe("ACGTCCAATGGTATAAA", packet_id="packet-1", source="first")
    record = microbiota.observe(
        "ACGTCCAATGGTATAAA",
        packet_id="packet-2",
        source="second",
        action="discard_duplicate",
        status="discarded",
    )

    assert record.seen_count == 2
    assert record.is_recurrent is True
    assert record.last_packet_id == "packet-2"
    assert record.last_action == "discard_duplicate"
    assert record.last_status == "discarded"


def test_microbiota_exports_memory_without_exposing_internal_state():
    microbiota = InformationalMicrobiota()
    microbiota.observe(" acgt ", packet_id="packet-1", source="normalized")

    exported = microbiota.export_memory()
    exported["ACGT"]["seen_count"] = 99

    assert microbiota.export_memory()["ACGT"]["seen_count"] == 1


def test_update_microbiota_memory_updates_existing_mapping():
    memory = {}

    first = update_microbiota_memory(
        memory,
        "ACGTCCAATGGTATAAA",
        packet_id="packet-1",
        source="first",
        action="absorb",
        status="ok",
    )
    second = update_microbiota_memory(
        memory,
        "ACGTCCAATGGTATAAA",
        packet_id="packet-2",
        source="second",
        action="discard_duplicate",
        status="discarded",
    )

    assert first.seen_count == 1
    assert second.seen_count == 2
    assert memory["ACGTCCAATGGTATAAA"]["seen_count"] == 2
    assert memory["ACGTCCAATGGTATAAA"]["last_source"] == "second"
