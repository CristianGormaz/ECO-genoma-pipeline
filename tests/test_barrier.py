from src.eco_core.barrier import evaluate_barrier


def test_barrier_rejects_non_text_payload():
    result = evaluate_barrier(
        is_text=False,
        is_empty=False,
        invalid_characters=[],
        length=0,
        min_length=6,
        n_percent=0.0,
        max_n_percent=25.0,
    )

    assert result.allowed is False
    assert result.status == "rejected"
    assert result.permeability == 0.0


def test_barrier_rejects_invalid_characters():
    result = evaluate_barrier(
        is_text=True,
        is_empty=False,
        invalid_characters=["X", "Z"],
        length=7,
        min_length=6,
        n_percent=0.0,
        max_n_percent=25.0,
    )

    assert result.allowed is False
    assert result.status == "rejected"
    assert "X, Z" in result.reason


def test_barrier_quarantines_short_sequence():
    result = evaluate_barrier(
        is_text=True,
        is_empty=False,
        invalid_characters=[],
        length=3,
        min_length=6,
        n_percent=0.0,
        max_n_percent=25.0,
    )

    assert result.allowed is True
    assert result.status == "quarantined"
    assert result.permeability == 0.35


def test_barrier_allows_valid_sequence():
    result = evaluate_barrier(
        is_text=True,
        is_empty=False,
        invalid_characters=[],
        length=17,
        min_length=6,
        n_percent=0.0,
        max_n_percent=25.0,
    )

    assert result.allowed is True
    assert result.status == "ok"
    assert result.permeability == 0.95
