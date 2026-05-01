from src.eco_core import (
    DEFAULT_TRANSITION_PACKETS,
    EXTENDED_TRANSITION_PACKETS,
    build_adaptive_state_rows,
    get_transition_packets,
)


def test_extended_transition_packets_keep_default_catalog_intact():
    assert get_transition_packets(extended=False) == DEFAULT_TRANSITION_PACKETS
    assert len(DEFAULT_TRANSITION_PACKETS) == 4
    assert len(EXTENDED_TRANSITION_PACKETS) >= 12
    assert len(get_transition_packets(extended=True)) == len(EXTENDED_TRANSITION_PACKETS)


def test_extended_transition_rows_cover_more_digestive_routes():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)

    assert len(rows) == len(EXTENDED_TRANSITION_PACKETS)
    decisions = {row.final_decision for row in rows}
    barriers = {row.barrier_status for row in rows}
    defenses = {row.defense_category for row in rows}
    states = {row.state_after for row in rows}

    assert "absorb" in decisions
    assert "reject" in decisions
    assert "quarantine" in decisions
    assert "discard_duplicate" in decisions
    assert "ok" in barriers
    assert {"invalid_payload", "retained_payload", "redundant_payload"}.issubset(defenses)
    assert {"stable", "watch", "attention"}.issubset(states)


def test_extended_transition_rows_include_recurrence_and_responsible_limit():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)

    assert any(row.microbiota_seen_count > 1 for row in rows)
    assert all("no modela conciencia humana" in row.responsible_limit for row in rows)
