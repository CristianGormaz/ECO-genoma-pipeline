from pathlib import Path


DOC_PATH = Path("docs/operations/eco-agentic-scaffold-proposal-template.md")


def test_agentic_scaffold_proposal_template_exists() -> None:
    assert DOC_PATH.exists(), "Debe existir la plantilla de propuesta scaffold"


def test_agentic_scaffold_proposal_template_contract() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()

    required_tokens = [
        "Agentic Scaffold Proposal Template",
        "eco-agentic-scaffold-protocol.md",
        "Identificación de la propuesta",
        "Propósito operativo",
        "Módulo o habitación propuesta",
        "Clasificación inicial",
        "permitido",
        "requiere revisión",
        "bloqueado",
        "Archivos mínimos sugeridos",
        "Tests contractuales esperados",
        "Validaciones requeridas",
        "Decisión final humana",
    ]

    for token in required_tokens:
        assert token.lower() in lower_text

    assert "criterios de pausa" in lower_text or "revisión humana" in lower_text

    required_limits = [
        "sin autonomía real",
        "sin conciencia",
        "sin libre albedrío real",
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
    ]

    for item in required_limits:
        assert item in lower_text
