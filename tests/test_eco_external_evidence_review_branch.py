from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_evidence_review_branch_doc_exists_and_names_branch():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-review-branch.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Revisión de rama: eco-sne-external-evidence-review",
        "documental / auditoría",
        "No se hizo merge",
        "No se hizo cherry-pick",
        "No se incorporó evidencia externa automáticamente",
    ]

    for token in required_tokens:
        assert token in content


def test_external_evidence_review_branch_doc_mentions_rescue_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-review-branch.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "No integrar la rama completa",
        "Piezas potencialmente rescatables",
        "sin entrenamiento",
        "sin datos sensibles",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin integración masiva de ramas antiguas",
    ]

    for token in required_tokens:
        assert token in content
