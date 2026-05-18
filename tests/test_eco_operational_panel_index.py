from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_operational_panel_index_exists():
    index_path = ROOT / "docs" / "operations" / "eco-operational-panel-index.md"

    assert index_path.exists()


def test_operational_panel_index_mentions_snapshot_and_governance_state():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_tokens = [
        "Snapshot estable actual",
        "docs/operations/eco-post-governance-snapshot.md",
        "8 componentes",
        "governance panel integrado",
        "autodesarrollo gobernado activo",
        "pytest passing",
    ]

    for token in required_tokens:
        assert token in content


def test_operational_panel_index_preserves_responsible_limits():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_limits = [
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
    ]

    for token in required_limits:
        assert token in content


def test_operational_panel_index_links_release_checklist_and_timeline():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_tokens = [
        "docs/operations/eco-sprint-release-checklist.md",
        "checklist de liberación",
        "antes de abrir PR",
        "antes de mergear",
        "después de mergear",
        "pytest passing",
        "Límites responsables",
    ]

    for token in required_tokens:
        assert token in content


def test_operational_panel_index_links_agentic_scaffold_protocol():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_tokens = [
        "docs/operations/eco-agentic-scaffold-protocol.md",
        "Agentic Scaffold Protocol",
        "autodesarrollo asistido",
        "autodesarrollo gobernado",
        "agente generativo",
        "plantillas",
        "revisión humana",
        "nuevas funciones",
        "nueva función",
        "módulo candidato",
        "sin autonomía real",
        "sin conciencia",
        "sin libre albedrío real",
    ]

    for token in required_tokens:
        assert token in content


def test_operational_panel_index_links_agentic_scaffold_proposal_template():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_tokens = [
        "docs/operations/eco-agentic-scaffold-proposal-template.md",
        "Agentic Scaffold Proposal Template",
        "nuevas funciones o módulos candidatos",
        "clasificación inicial",
        "permitido",
        "requiere revisión",
        "bloqueado",
        "archivos mínimos sugeridos",
        "tests contractuales esperados",
        "validaciones requeridas",
        "revisión humana",
        "decisión final humana",
        "No aprueba integración por sí misma",
        "sin autonomía real",
        "sin conciencia",
        "sin libre albedrío real",
    ]

    for token in required_tokens:
        assert token in content


def test_operational_panel_index_links_agentic_scaffold_proposal_example():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_tokens = [
        "docs/operations/eco-agentic-scaffold-proposal-example.md",
        "Agentic Scaffold Proposal Example",
        "Agentic Scaffold Proposal Template",
        "ejemplo rellenado de módulo candidato",
        "Candidate Module: Governed Operational Trace Scaffold",
        "ejemplo es documental",
        "no ejecutable",
        "pendiente de revisión humana",
        "revisión humana",
        "decisión final humana",
        "No aprueba integración por sí misma",
        "sin autonomía real",
        "sin conciencia",
        "sin libre albedrío real",
    ]

    for token in required_tokens:
        assert token in content


def test_operational_panel_index_links_agentic_scaffold_proposal_registry():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )
    lowered = content.lower()

    required_tokens = [
        "docs/operations/eco-agentic-scaffold-proposal-registry.md",
        "agentic scaffold proposal registry",
        "catálogo",
        "listado",
        "propuestas agentic scaffold",
        "estado",
        "clasificación",
        "revisión humana",
        "decisión final humana",
        "asc-prop-001",
        "candidate module: governed operational trace scaffold",
        "no aprueba integración por sí mismo",
        "sin autonomía real",
        "sin conciencia",
        "sin libre albedrío real",
    ]

    for token in required_tokens:
        assert token in lowered


def test_operational_panel_index_links_current_capabilities_map_and_laos_contract():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_tokens = [
        "docs/operations/eco-current-capabilities-map.md",
        "mapa de capacidades actuales",
        "capacidades existentes",
        "cómo se validan",
        "qué falta",
        "docs/operations/eco-laos-agency-formula.md",
        "docs/operations/eco-laos-governance-gate.md",
        "LAOS",
        "Libre Albedrío Operativo Simulado",
        "LAOS Governance Gate",
        "agencia simulada",
        "compuerta sintética de gobernanza",
        "pausa",
        "revisión humana",
        "avance controlado",
        "no activa autonomía real",
        "sin libre albedrío real",
        "sin conciencia",
        "pytest passing",
        "snapshot",
        "checklist",
        "Límites responsables",
    ]

    for token in required_tokens:
        assert token in content
