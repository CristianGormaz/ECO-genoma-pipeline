from pathlib import Path


GUIDE = Path("docs/operations/eco-add-synthetic-demo-guide.md")
README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")


def test_add_synthetic_demo_guide_exists_and_mentions_required_files():
    text = GUIDE.read_text(encoding="utf-8")

    assert "Guía para agregar una demo sintética E.C.O." in text
    assert "scripts/run_eco_<nombre>_demo.py" in text
    assert "eco-synthetic-demo-registry.json" in text
    assert "eco-synthetic-demo-registry.md" in text
    assert "eco-synthetic-demos-index.md" in text


def test_add_synthetic_demo_guide_mentions_validation_commands():
    text = GUIDE.read_text(encoding="utf-8")

    assert "make eco-status" in text
    assert "make eco-validate-synthetic-demos" in text
    assert "python3 -m pytest -q" in text
    assert "git status --short" in text


def test_add_synthetic_demo_guide_declares_responsible_limits():
    text = GUIDE.read_text(encoding="utf-8")

    assert "No usar datos sensibles" in text
    assert "No entrenar modelos" in text
    assert "No modificar baseline estable" in text
    assert "No recalibrar umbrales" in text
    assert "No hacer afirmaciones biomédicas aplicadas" in text


def test_add_synthetic_demo_guide_is_linked():
    readme_text = README.read_text(encoding="utf-8")
    project_map_text = PROJECT_MAP.read_text(encoding="utf-8")

    assert "docs/operations/eco-add-synthetic-demo-guide.md" in readme_text
    assert "eco-add-synthetic-demo-guide.md" in project_map_text
