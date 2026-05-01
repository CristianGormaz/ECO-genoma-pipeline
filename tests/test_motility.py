from src.eco_core.barrier import evaluate_barrier
from src.eco_core.motility import decide_motility
from src.eco_core.sensor_local import analyze_payload, build_payload_key


def test_motility_advances_valid_payload():
    profile = analyze_payload("ACGTCCAATGGTATAAA", packet_type="dna")
    barrier = evaluate_barrier(
        is_text=profile.is_text,
        is_empty=profile.is_empty,
        invalid_characters=list(profile.invalid_characters),
        length=profile.length,
        min_length=6,
        n_percent=profile.n_percent,
        max_n_percent=25.0,
    )

    decision = decide_motility(profile, barrier)

    assert decision.action == "advance"
    assert decision.status == "ok"
    assert decision.route == "submucosal_absorption"
    assert decision.can_continue is True
    assert decision.transit_score == 0.95


def test_motility_sends_invalid_payload_to_immune_discard():
    profile = analyze_payload("ACGTXYZ", packet_type="dna")
    barrier = evaluate_barrier(
        is_text=profile.is_text,
        is_empty=profile.is_empty,
        invalid_characters=list(profile.invalid_characters),
        length=profile.length,
        min_length=6,
        n_percent=profile.n_percent,
        max_n_percent=25.0,
    )

    decision = decide_motility(profile, barrier)

    assert decision.action == "immune_discard"
    assert decision.status == "rejected"
    assert decision.can_continue is False
    assert decision.transit_score == 0.0


def test_motility_quarantines_short_payload():
    profile = analyze_payload("ACG", packet_type="dna")
    barrier = evaluate_barrier(
        is_text=profile.is_text,
        is_empty=profile.is_empty,
        invalid_characters=list(profile.invalid_characters),
        length=profile.length,
        min_length=6,
        n_percent=profile.n_percent,
        max_n_percent=25.0,
    )

    decision = decide_motility(profile, barrier)

    assert decision.action == "quarantine"
    assert decision.status == "quarantined"
    assert decision.route == "quarantine"
    assert decision.can_continue is False
    assert decision.transit_score == 0.35


def test_motility_discards_duplicate_before_absorption():
    known_key = build_payload_key("ACGTCCAATGGTATAAA")
    profile = analyze_payload(
        "ACGTCCAATGGTATAAA",
        packet_type="dna",
        known_payload_keys={known_key},
    )
    barrier = evaluate_barrier(
        is_text=profile.is_text,
        is_empty=profile.is_empty,
        invalid_characters=list(profile.invalid_characters),
        length=profile.length,
        min_length=6,
        n_percent=profile.n_percent,
        max_n_percent=25.0,
    )

    decision = decide_motility(profile, barrier)

    assert decision.action == "discard_duplicate"
    assert decision.status == "discarded"
    assert decision.route == "controlled_discard"
    assert decision.can_continue is False
    assert decision.transit_score == 0.1


def test_motility_marks_heavy_payload_for_batch_flow():
    profile = analyze_payload("ACGTACGT", packet_type="dna", heavy_payload_threshold=8)
    barrier = evaluate_barrier(
        is_text=profile.is_text,
        is_empty=profile.is_empty,
        invalid_characters=list(profile.invalid_characters),
        length=profile.length,
        min_length=6,
        n_percent=profile.n_percent,
        max_n_percent=25.0,
    )

    decision = decide_motility(profile, barrier)

    assert decision.action == "batch_advance"
    assert decision.status == "batched"
    assert decision.route == "myenteric_batch_flow"
    assert decision.can_continue is True
    assert decision.transit_score == 0.65
