from src.eco_core import EntericSystem, build_packet_trace, build_packet_traces, traces_to_markdown


def test_packet_trace_marks_valid_sequence_as_absorbed():
    system = EntericSystem()
    packet = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    trace = build_packet_trace(packet)

    assert trace.source == "valid_sequence"
    assert trace.payload_length == 17
    assert trace.barrier_status == "ok"
    assert trace.motility_action == "advance"
    assert trace.final_decision == "absorb"
    assert trace.absorbed is True
    assert trace.discarded is False
    assert trace.microbiota_seen_count == 1


def test_packet_trace_marks_invalid_sequence_as_rejected_discarded():
    system = EntericSystem()
    packet = system.process_dna_sequence("ACGTXYZ", source="invalid_sequence")

    trace = build_packet_trace(packet)

    assert trace.source == "invalid_sequence"
    assert trace.barrier_status == "rejected"
    assert trace.motility_action == "immune_discard"
    assert trace.final_decision == "reject"
    assert trace.rejected is True
    assert trace.discarded is True
    assert trace.absorbed is False


def test_packet_trace_marks_short_sequence_as_quarantined():
    system = EntericSystem(min_length=6)
    packet = system.process_dna_sequence("ACG", source="short_sequence")

    trace = build_packet_trace(packet)

    assert trace.source == "short_sequence"
    assert trace.barrier_status == "quarantined"
    assert trace.motility_action == "quarantine"
    assert trace.final_decision == "quarantine"
    assert trace.quarantined is True
    assert trace.absorbed is False


def test_packet_trace_marks_duplicate_with_recurrence_memory():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="first_sequence")
    duplicate = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="duplicate_sequence")

    trace = build_packet_trace(duplicate)

    assert trace.source == "duplicate_sequence"
    assert trace.motility_action == "discard_duplicate"
    assert trace.final_decision == "discard_duplicate"
    assert trace.discarded is True
    assert trace.microbiota_seen_count == 2


def test_packet_traces_render_to_markdown():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")
    system.process_dna_sequence("ACGTXYZ", source="invalid_sequence")

    traces = build_packet_traces(system.processed_packets)
    markdown = traces_to_markdown(traces)

    assert len(traces) == 2
    assert "Ruta digestiva S.N.E.-E.C.O." in markdown
    assert "valid_sequence" in markdown
    assert "invalid_sequence" in markdown
    assert "absorbed" in markdown or "absorb" in markdown
