from pathlib import Path


README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
SYNTHETIC_INDEX = Path("docs/architecture/eco-synthetic-demos-index.md")


def test_readme_links_synthetic_demos_index():
    text = README.read_text(encoding="utf-8")

    assert "docs/architecture/eco-synthetic-demos-index.md" in text
    assert "Índice de demos sintéticas E.C.O." in text


def test_project_map_links_synthetic_demos_index():
    text = PROJECT_MAP.read_text(encoding="utf-8")

    assert "docs/architecture/eco-synthetic-demos-index.md" in text
    assert "demos sintéticas" in text


def test_synthetic_demos_index_exists():
    assert SYNTHETIC_INDEX.exists()
