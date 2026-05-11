from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_admission_review_template_exists_and_mentions_core_sections():
    content = (
        ROOT / "docs" / "operations" / "eco-admission-review-template.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Plantilla de revisión de admisión",
        "Identificación de la pieza",
        "Clasificación responsable",
        "Preguntas de admisión",
        "Decisión",
        "Validación mínima sugerida",
    ]

    for token in required_tokens:
        assert token in content


def test_admission_review_template_mentions_responsible_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-admission-review-template.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "sin entrenamiento",
        "sin datos sensibles",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin integración masiva de ramas antiguas",
    ]

    for token in required_tokens:
        assert token in content
