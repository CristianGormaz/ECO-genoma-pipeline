from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "architecture" / "eco-adaptive-state-foundation.md"


def test_adaptive_state_foundation_exists_and_defines_states():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "Fundamentos de estado adaptativo E.C.O.",
        "`observed`",
        "`review_needed`",
        "`candidate`",
        "`accepted`",
        "`blocked`",
        "Ciclo adaptativo mínimo",
    ]

    for token in required_tokens:
        assert token in content


def test_adaptive_state_foundation_keeps_responsible_limits():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "No entrena modelos",
        "No modifica baseline",
        "No recalibra umbrales",
        "No incorpora datos sensibles",
        "sin datos genéticos privados",
        "sin afirmaciones biomédicas aplicadas",
        "sin integración masiva de ramas antiguas",
    ]

    for token in required_tokens:
        assert token in content
