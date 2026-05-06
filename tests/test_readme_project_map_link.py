from pathlib import Path


README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
TERMINAL_GUIDE = Path("docs/operations/terminal-stop-guide.md")


def test_readme_links_project_map():
    text = README.read_text(encoding="utf-8")

    assert "docs/operations/project-map.md" in text
    assert "Mapa operativo del proyecto" in text


def test_project_map_assets_exist():
    assert PROJECT_MAP.exists()
    assert TERMINAL_GUIDE.exists()
