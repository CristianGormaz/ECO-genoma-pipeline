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
        "7 componentes",
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


def test_operational_panel_index_links_current_capabilities_map():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_tokens = [
        "docs/operations/eco-current-capabilities-map.md",
        "mapa de capacidades actuales",
        "capacidades existentes",
        "cómo se validan",
        "qué falta",
        "pytest passing",
        "docs/operations/eco-post-governance-snapshot.md",
        "docs/operations/eco-sprint-release-checklist.md",
        "Límites responsables",
    ]

    for token in required_tokens:
        assert token in content
