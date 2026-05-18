from pathlib import Path


DOC_PATH = Path("docs/operations/eco-agentic-scaffold-proposal-example.md")


def test_agentic_scaffold_proposal_example_exists() -> None:
    assert DOC_PATH.exists(), "Debe existir el ejemplo de propuesta scaffold"


def test_agentic_scaffold_proposal_example_contract() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()

    required_tokens = [
        "Agentic Scaffold Proposal Example",
        "eco-agentic-scaffold-proposal-template.md",
        "eco-agentic-scaffold-protocol.md",
        "Candidate Module: Governed Operational Trace Scaffold",
        "Ejemplo documental — no ejecutable — pendiente de revisión humana",
        "requiere revisión",
        "pendiente de revisión humana",
        "decisión final humana",
        "no implementa función ejecutable",
        "no aprueba integración por sí misma",
        "no modifica principios admitidos",
        "archivos mínimos sugeridos",
        "tests contractuales esperados",
        "validaciones requeridas",
        "criterios de pausa",
        "checklist de revisión humana",
    ]

    for token in required_tokens:
        assert token.lower() in lower_text


def test_agentic_scaffold_proposal_example_preserves_responsible_limits() -> None:
    text = DOC_PATH.read_text(encoding="utf-8").lower()

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

    for token in required_limits:
        assert token in text


def test_agentic_scaffold_proposal_example_has_no_executable_code_blocks() -> None:
    text = DOC_PATH.read_text(encoding="utf-8").lower()

    forbidden_fences = [
        "```python",
        "```bash",
        "```sql",
        "```sh",
    ]

    for fence in forbidden_fences:
        assert fence not in text
