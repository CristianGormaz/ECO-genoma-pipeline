from pathlib import Path


README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
REGISTRY = Path("docs/architecture/eco-synthetic-demo-registry.md")


def test_readme_links_synthetic_demo_registry():
    text = README.read_text(encoding="utf-8")

    assert "Registro de demos sintéticas E.C.O." in text
    assert "docs/architecture/eco-synthetic-demo-registry.md" in text
    assert "make eco-validate-synthetic-demos" in text


def test_project_map_links_synthetic_demo_registry():
    text = PROJECT_MAP.read_text(encoding="utf-8")

    assert "Registro sintético" in text
    assert "eco-synthetic-demo-registry.md" in text
    assert "make eco-validate-synthetic-demos" in text


def test_synthetic_demo_registry_asset_exists():
    assert REGISTRY.exists()
