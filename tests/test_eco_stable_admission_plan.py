from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_stable_admission_plan_exists_and_defines_states():
    content = (
        ROOT / "docs" / "operations" / "eco-stable-admission-plan.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "draft",
        "review_needed",
        "candidate",
        "accepted",
        "blocked",
        "Criterios mínimos",
        "Criterios de bloqueo",
    ]

    for token in required_tokens:
        assert token in content


def test_stable_admission_plan_sets_responsible_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-stable-admission-plan.md"
    ).read_text(encoding="utf-8")

    required_limits = [
        "sin entrenamiento",
        "sin datos sensibles",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin incorporación automática de evidencia externa",
        "sin integración masiva de ramas antiguas",
    ]

    for limit in required_limits:
        assert limit in content
