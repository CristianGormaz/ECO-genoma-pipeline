from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_stable_admission_dry_run_review_exists_and_mentions_decision():
    content = (
        ROOT / "docs" / "operations" / "eco-stable-admission-dry-run-review.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "eco-sne-stable-admission-dry-run",
        "Identificación de la pieza",
        "Clasificación responsable",
        "Preguntas de admisión",
        "No integrar la rama",
        "sin integración masiva de ramas antiguas",
    ]

    for token in required_tokens:
        assert token in content


def test_stable_admission_dry_run_review_mentions_responsible_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-stable-admission-dry-run-review.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "sin entrenamiento",
        "sin datos sensibles",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin incorporación automática de evidencia externa",
    ]

    for token in required_tokens:
        assert token in content
