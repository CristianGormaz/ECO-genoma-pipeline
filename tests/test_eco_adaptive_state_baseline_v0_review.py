from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adaptive_state_baseline_v0_review_exists_and_mentions_branch():
    content = (
        ROOT / "docs" / "operations" / "eco-adaptive-state-baseline-v0-review.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "eco-adaptive-state-baseline-v0",
        "baseline adaptativo",
        "No se hizo merge",
        "No se hizo cherry-pick",
        "No se modificó baseline",
        "No se recalibraron umbrales",
    ]

    for token in required_tokens:
        assert token in content


def test_adaptive_state_baseline_v0_review_mentions_responsible_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-adaptive-state-baseline-v0-review.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "sin entrenamiento",
        "sin datos sensibles",
        "sin datos genéticos privados",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin integración masiva de ramas antiguas",
    ]

    for token in required_tokens:
        assert token in content
