from src.eco_core.ingestion import ingest_text
from src.eco_core.sensor_local import analyze_packet, analyze_payload, build_payload_key


def test_sensor_local_profiles_valid_dna_payload():
    profile = analyze_payload("ACGTCCAATGGTATAAA", source="valid_sequence", packet_type="dna")

    assert profile.is_text is True
    assert profile.is_empty is False
    assert profile.length == 17
    assert profile.invalid_characters == tuple()
    assert profile.is_duplicate is False
    assert profile.is_heavy is False
    assert profile.payload_key == "ACGTCCAATGGTATAAA"


def test_sensor_local_detects_invalid_characters():
    profile = analyze_payload("ACGTXYZ", source="invalid_sequence", packet_type="dna")

    assert profile.invalid_characters == ("X", "Y", "Z")
    assert any("caracteres no válidos" in issue for issue in profile.filter_issues)


def test_sensor_local_detects_non_text_payload():
    profile = analyze_payload({"seq": "ACGT"}, source="dict_payload", packet_type="dna")

    assert profile.is_text is False
    assert profile.payload_type == "dict"
    assert profile.length == 0
    assert profile.filter_issues == ("El payload no es texto.",)


def test_sensor_local_detects_duplicate_payload_key():
    known_key = build_payload_key("ACGTCCAATGGTATAAA")
    profile = analyze_payload(
        "ACGTCCAATGGTATAAA",
        source="duplicate_sequence",
        packet_type="dna",
        known_payload_keys={known_key},
    )

    assert profile.is_duplicate is True


def test_sensor_local_detects_heavy_payload():
    profile = analyze_payload("ACGTACGT", packet_type="dna", heavy_payload_threshold=8)

    assert profile.is_heavy is True


def test_sensor_local_analyzes_ecopacket_with_traceability():
    packet = ingest_text("ACGTCCAATGGTATAAA", source="packet_source", packet_type="dna")
    profile = analyze_packet(packet)

    assert profile.packet_id == packet.packet_id
    assert profile.source == "packet_source"
    assert profile.packet_type == "dna"
    assert profile.to_dict()["packet_id"] == packet.packet_id
    assert isinstance(profile.to_dict()["invalid_characters"], list)
