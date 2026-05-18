from pathlib import Path


def test_eco_current_capabilities_map_exists_and_contains_required_sections() -> None:
    doc_path = Path("docs/operations/eco-current-capabilities-map.md")
    assert doc_path.exists(), "Debe existir docs/operations/eco-current-capabilities-map.md"

    content = doc_path.read_text(encoding="utf-8")
    lowered = content.lower()

    required_phrases = [
        "pytest passing",
        "dashboard sintético operativo con 8 componentes",
        "governance panel",
        "checklist de liberación",
        "snapshot post-governance",
        "demos sintéticas",
        "s.n.e.-e.c.o.",
        "validaciones disponibles",
        "límites responsables",
        "qué no hace todavía e.c.o.",
        "próximo salto recomendado",
        "eco-laos-agency-formula.md",
        "laos",
        "libre albedrío operativo simulado",
        "agencia simulada",
        "autodesarrollo gobernado",
        "no representa libre albedrío real ni conciencia",
        "docs/operations/eco-laos-governance-gate.md",
        "laos governance gate",
        "compuerta de gobernanza",
        "pausar",
        "revisión humana",
        "avanzar con control",
        "sin libre albedrío real",
        "sin conciencia",
        "docs/operations/eco-agentic-scaffold-protocol.md",
        "agentic scaffold protocol",
        "autodesarrollo asistido",
        "agente generativo",
        "plantilla",
        "módulos candidatos",
        "nuevas funciones",
        "sin autonomía real",
        "no implica autonomía real",
        "docs/operations/eco-agentic-scaffold-proposal-template.md",
        "agentic scaffold proposal template",
        "nuevas funciones o módulos candidatos",
        "clasificación inicial",
        "permitido",
        "requiere revisión",
        "bloqueado",
        "archivos mínimos sugeridos",
        "tests contractuales esperados",
        "validaciones requeridas",
        "decisión final humana",
    ]

    for phrase in required_phrases:
        assert phrase in lowered, f"Falta mención requerida: {phrase}"
