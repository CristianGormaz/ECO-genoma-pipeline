from pathlib import Path


def test_eco_current_capabilities_map_exists_and_contains_required_sections() -> None:
    doc_path = Path("docs/operations/eco-current-capabilities-map.md")
    assert doc_path.exists(), "Debe existir docs/operations/eco-current-capabilities-map.md"

    content = doc_path.read_text(encoding="utf-8")
    lowered = content.lower()

    required_phrases = [
        "pytest passing",
        "dashboard sintético operativo con 7 componentes",
        "governance panel",
        "checklist de liberación",
        "snapshot post-governance",
        "demos sintéticas",
        "s.n.e.-e.c.o.",
        "validaciones disponibles",
        "límites responsables",
        "qué no hace todavía e.c.o.",
        "próximo salto recomendado",
    ]

    for phrase in required_phrases:
        assert phrase in lowered, f"Falta mención requerida: {phrase}"
