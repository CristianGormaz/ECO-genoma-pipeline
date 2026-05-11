from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_evidence_review_guide_exists_and_defines_flow():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-review-guide.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Guía operativa de revisión de evidencia externa E.C.O.",
        "Flujo recomendado",
        "Estados de decisión",
        "accepted",
        "review_needed",
        "blocked",
    ]

    for token in required_tokens:
        assert token in content


def test_external_evidence_review_guide_mentions_responsible_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-review-guide.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "sin entrenamiento",
        "sin datos sensibles",
        "sin datos genéticos privados",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin incorporación automática de evidencia externa",
    ]

    for token in required_tokens:
        assert token in content
