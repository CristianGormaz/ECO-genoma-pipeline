from pathlib import Path


DOC = Path("docs/operations/project-map.md")
README = Path("README.md")
MAKEFILE = Path("Makefile")
STATUS_SCRIPT = Path("scripts/run_eco_status.py")
TERMINAL_GUIDE = Path("docs/operations/terminal-stop-guide.md")
RESEARCH_INDEX = Path("docs/research/eco-research-index.md")


def test_project_map_exists_and_mentions_core_assets():
    text = DOC.read_text(encoding="utf-8")

    assert "Mapa operativo del proyecto E.C.O." in text
    assert "README.md" in text
    assert "Makefile" in text
    assert "make eco-status" in text
    assert "make eco-vacuum-state-demo" in text
    assert "docs/operations/" in text
    assert "docs/research/" in text
    assert "scripts/" in text
    assert "tests/" in text


def test_project_map_responsible_limit():
    text = DOC.read_text(encoding="utf-8")

    assert "No usa datos sensibles" in text
    assert "no entrena modelos" in text
    assert "no modifica baseline" in text
    assert "no recalibra umbrales" in text


def test_project_map_referenced_assets_exist():
    assert README.exists()
    assert MAKEFILE.exists()
    assert STATUS_SCRIPT.exists()
    assert TERMINAL_GUIDE.exists()
    assert RESEARCH_INDEX.exists()
