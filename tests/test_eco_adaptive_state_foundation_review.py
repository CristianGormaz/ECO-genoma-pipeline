from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adaptive_state_foundation_review_exists_and_mentions_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-adaptive-state-foundation-review.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Revisión de rama: eco-adaptive-state-foundation",
        "documental / auditoría",
        "No se hizo merge",
        "No se hizo cherry-pick",
        "No se modificó baseline",
        "No se recalibraron umbrales",
        "No se entrenaron modelos",
        "No se incorporaron datos sensibles",
    ]

    for token in required_tokens:
        assert token in content


def test_adaptive_state_foundation_review_blocks_sensitive_rescue():
    content = (
        ROOT / "docs" / "operations" / "eco-adaptive-state-foundation-review.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "No integrar `eco-adaptive-state-foundation` como bloque",
        "datasets",
        "cambios de baseline",
        "scripts de entrenamiento",
        "scripts de evaluación aplicada",
        "cambios de umbral",
        "afirmación biomédica aplicada",
        "sin integración masiva de ramas antiguas",
    ]

    for token in required_tokens:
        assert token in content
