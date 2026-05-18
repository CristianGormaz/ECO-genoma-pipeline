from pathlib import Path


DOC_PATH = Path("docs/operations/eco-agentic-scaffold-proposal-registry.md")


def test_agentic_scaffold_proposal_registry_exists() -> None:
    assert DOC_PATH.exists(), "Debe existir el registro de propuestas scaffold"


def test_agentic_scaffold_proposal_registry_contract() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()

    required_tokens = [
        "Agentic Scaffold Proposal Registry",
        "eco-agentic-scaffold-protocol.md",
        "eco-agentic-scaffold-proposal-template.md",
        "eco-agentic-scaffold-proposal-example.md",
        "ASC-PROP-001",
        "Governed Operational Trace Scaffold",
        "Candidate Module: Governed Operational Trace Scaffold",
        "pendiente de revisión humana",
        "requiere revisión",
        "decisión final humana",
        "proposal_id",
        "documento asociado",
        "módulo candidato",
        "validaciones esperadas",
        "límites responsables",
    ]

    for token in required_tokens:
        assert token.lower() in lower_text


def test_agentic_scaffold_proposal_registry_allowed_states() -> None:
    text = DOC_PATH.read_text(encoding="utf-8").lower()

    required_states = [
        "borrador",
        "pendiente de revisión humana",
        "requiere cambios",
        "aprobado documentalmente",
        "rechazado",
        "pausado",
    ]

    for state in required_states:
        assert state in text


def test_agentic_scaffold_proposal_registry_allowed_classifications() -> None:
    text = DOC_PATH.read_text(encoding="utf-8").lower()

    required_classifications = [
        "permitido",
        "requiere revisión",
        "bloqueado",
    ]

    for classification in required_classifications:
        assert classification in text


def test_agentic_scaffold_proposal_registry_preserves_responsible_limits() -> None:
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

    for limit in required_limits:
        assert limit in text


def test_agentic_scaffold_proposal_registry_has_no_executable_code_blocks() -> None:
    text = DOC_PATH.read_text(encoding="utf-8").lower()

    forbidden_fences = [
        "```python",
        "```bash",
        "```sh",
        "```sql",
    ]

    for fence in forbidden_fences:
        assert fence not in text
