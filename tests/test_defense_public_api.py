from src.eco_core import DefenseSignal, evaluate_defense
from src.eco_core.barrier import evaluate_barrier
from src.eco_core.motility import decide_motility
from src.eco_core.sensor_local import analyze_payload


def test_defense_helpers_are_available_from_public_core_api():
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
    motility = decide_motility(profile, barrier)

    signal = evaluate_defense(profile, barrier, motility)

    assert isinstance(signal, DefenseSignal)
    assert signal.category == "invalid_payload"
    assert signal.should_alert is True
