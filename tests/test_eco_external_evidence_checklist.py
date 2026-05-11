from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_evidence_checklist_exists_and_has_decisions():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-checklist.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Checklist de admisión de evidencia externa",
        "accept_as_context",
        "accept_as_reference",
        "review_needed",
        "blocked",
        "make eco-external-evidence-policy",
    ]

    for token in required_tokens:
        assert token in content


def test_external_evidence_checklist_mentions_blockers_and_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-checklist.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Datos sensibles",
        "Datos genéticos privados",
        "Diagnóstico clínico",
        "sin entrenamiento",
        "sin datos sensibles",
        "sin ingestión automática de datos reales",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
    ]

    for token in required_tokens:
        assert token in content
