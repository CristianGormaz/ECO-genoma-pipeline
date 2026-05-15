from pathlib import Path

SNAPSHOT = Path("docs/operations/eco-post-governance-snapshot.md")


def test_post_governance_snapshot_exists_and_mentions_expected_state():
    assert SNAPSHOT.exists(), "El snapshot post-governance debe existir"

    text = SNAPSHOT.read_text(encoding="utf-8").lower()

    assert "dashboard sintético" in text
    assert "7 componentes" in text
    assert "governance panel" in text
    assert "autodesarrollo gobernado" in text
    assert "511 passed" in text
    assert "límites responsables" in text
    assert "sin datos reales" in text
    assert "sin entrenamiento" in text
    assert "sin modificación de baseline" in text
    assert "sin recalibración de umbrales" in text
    assert "siguiente paso lógico" in text
