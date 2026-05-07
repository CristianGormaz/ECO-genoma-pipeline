from pathlib import Path


def test_eco_architecture_index_links_synthetic_state_timeline():
    root = Path(__file__).resolve().parents[1]
    index_path = root / "docs" / "architecture" / "README.md"
    timeline_path = root / "docs" / "architecture" / "eco-synthetic-state-timeline.md"

    assert index_path.exists()
    assert timeline_path.exists()

    index_text = index_path.read_text(encoding="utf-8")
    timeline_text = timeline_path.read_text(encoding="utf-8")

    assert "eco-synthetic-state-timeline.md" in index_text
    assert "No usa datos sensibles" in timeline_text
    assert "no entrena modelos" in timeline_text
    assert "no recalibra umbrales" in timeline_text
