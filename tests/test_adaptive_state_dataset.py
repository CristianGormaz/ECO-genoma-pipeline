from src.eco_core import (
    DEFAULT_TRANSITION_PACKETS,
    AdaptiveStateRow,
    adaptive_rows_to_markdown,
    build_adaptive_state_rows,
    rows_to_dicts,
)


def test_adaptive_state_rows_generate_one_row_per_packet():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)

    assert len(rows) == len(DEFAULT_TRANSITION_PACKETS)
    assert all(isinstance(row, AdaptiveStateRow) for row in rows)
    assert rows[0].source == "valid_sequence"
    assert rows[0].state_before == "idle"
    assert rows[0].total_packets_before == 0
    assert rows[0].total_packets_after == 1


def test_adaptive_state_rows_capture_digestive_signals():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    by_source = {row.source: row for row in rows}

    valid = by_source["valid_sequence"]
    invalid = by_source["invalid_sequence"]
    short = by_source["short_sequence"]
    duplicate = by_source["duplicate_sequence"]

    assert valid.final_decision == "absorb"
    assert valid.barrier_status == "ok"
    assert valid.motility_action == "advance"

    assert invalid.final_decision == "reject"
    assert invalid.defense_severity in {"warning", "critical"}

    assert short.final_decision == "quarantine"
    assert short.quarantine_ratio_after > short.quarantine_ratio_before

    assert duplicate.final_decision == "discard_duplicate"
    assert duplicate.microbiota_seen_count == 2
    assert duplicate.recurrence_ratio_after > duplicate.recurrence_ratio_before


def test_adaptive_state_rows_export_to_dicts():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    payload = rows_to_dicts(rows)

    assert len(payload) == 4
    assert payload[0]["state_before"] == "idle"
    assert "state_after" in payload[0]
    assert "immune_load_after" in payload[0]
    assert "responsible_limit" in payload[0]


def test_adaptive_state_rows_markdown_mentions_limits():
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    markdown = adaptive_rows_to_markdown(rows)

    assert "Dataset adaptativo E.C.O." in markdown
    assert "state_before" in markdown
    assert "state_after" in markdown
    assert "no modela conciencia humana" in markdown
    assert "valid_sequence" in markdown
