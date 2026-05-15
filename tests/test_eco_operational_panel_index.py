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
        "510 passed",
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
