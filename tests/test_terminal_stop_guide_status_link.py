from pathlib import Path


DOC = Path("docs/operations/terminal-stop-guide.md")
MAKEFILE = Path("Makefile")
SCRIPT = Path("scripts/run_eco_status.py")


def test_terminal_stop_guide_mentions_eco_status_command():
    text = DOC.read_text(encoding="utf-8")

    assert "make eco-status" in text
    assert "Estado green" in text
    assert "Estado attention" in text
    assert "No modifica archivos" in text


def test_eco_status_command_assets_exist():
    assert MAKEFILE.exists()
    assert SCRIPT.exists()

    makefile_text = MAKEFILE.read_text(encoding="utf-8")
    assert "eco-status:" in makefile_text
    assert "scripts/run_eco_status.py" in makefile_text
