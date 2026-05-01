from src.eco_core.barrier import evaluate_barrier
from src.eco_core.defense import evaluate_defense
from src.eco_core.motility import decide_motility
from src.eco_core.sensor_local import analyze_payload, build_payload_key


def _pipeline_signals(sequence, *, known_payload_keys=None, heavy_payload_threshold=10_000):
    profile = analyze_payload(
        sequence,
        packet_type="dna",
        known_payload_keys=known_payload_keys,
        heavy_payload_threshold=heavy_payload_threshold,
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
    motility = decide_motility(profile, barrier)
    return profile, barrier, motility


def test_defense_signal_none_for_valid_payload():
    profile, barrier, motility = _pipeline_signals("ACGTCCAATGGTATAAA")

    signal = evaluate_defense(profile, barrier, motility)

    assert signal.category == "none"
    assert signal.severity == "none"
    assert signal.should_alert is False
    assert signal.recommended_action == "continue"


def test_defense_signal_high_for_invalid_payload():
    profile, barrier, motility = _pipeline_signals("ACGTXYZ")

    signal = evaluate_defense(profile, barrier, motility)

    assert signal.category == "invalid_payload"
    assert signal.severity == "high"
    assert signal.should_alert is True
    assert signal.recommended_action == "discard"


def test_defense_signal_low_for_duplicate_payload():
    key = build_payload_key("ACGTCCAATGGTATAAA")
    profile, barrier, motility = _pipeline_signals(
        "ACGTCCAATGGTATAAA",
        known_payload_keys={key},
    )

    signal = evaluate_defense(profile, barrier, motility)

    assert signal.category == "redundant_payload"
    assert signal.severity == "low"
    assert signal.should_alert is False
    assert signal.recommended_action == "discard_duplicate"


def test_defense_signal_medium_for_short_retained_payload():
    profile, barrier, motility = _pipeline_signals("ACG")

    signal = evaluate_defense(profile, barrier, motility)

    assert signal.category == "retained_payload"
    assert signal.severity == "medium"
    assert signal.should_alert is True
    assert signal.recommended_action == "quarantine"


def test_defense_signal_medium_for_ambiguous_payload():
    profile, barrier, motility = _pipeline_signals("ACGTNNNN")

    signal = evaluate_defense(profile, barrier, motility)

    assert signal.category == "ambiguous_payload"
    assert signal.severity == "medium"
    assert signal.should_alert is True
    assert signal.recommended_action == "quarantine"
