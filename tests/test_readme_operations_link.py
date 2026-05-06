from pathlib import Path


README = Path("README.md")
GUIDE = Path("docs/operations/terminal-stop-guide.md")
SCRIPT = Path("scripts/run_eco_status.py")


def test_readme_links_terminal_stop_guide_and_status_command():
    text = README.read_text(encoding="utf-8")

    assert "Operación segura del repositorio" in text
    assert "make eco-status" in text
    assert "docs/operations/terminal-stop-guide.md" in text
    assert "Estado green" in text
    assert "Estado attention" in text


def test_operational_assets_exist():
    assert GUIDE.exists()
    assert SCRIPT.exists()
