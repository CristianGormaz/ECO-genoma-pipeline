from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_stable_admission_plan_review_exists_and_sets_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-stable-admission-plan-review.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "eco-sne-stable-admission-plan",
        "No se hizo merge",
        "No se hizo cherry-pick",
        "sin entrenamiento",
        "sin datos sensibles",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin incorporación automática de evidencia externa",
        "No integrar la rama",
    ]

    for token in required_tokens:
        assert token in content


def test_stable_admission_plan_review_recommends_small_rescue():
    content = (
        ROOT / "docs" / "operations" / "eco-stable-admission-plan-review.md"
    ).read_text(encoding="utf-8")

    assert "PRs pequeños" in content
    assert "plan de admisión estable" in content
    assert "sin integración masiva de ramas antiguas" in content
