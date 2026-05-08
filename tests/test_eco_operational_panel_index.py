from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_operational_panel_index_mentions_core_commands_and_states():
    content = (ROOT / "docs" / "operations" / "eco-operational-panel-index.md").read_text(
        encoding="utf-8"
    )

    required_tokens = [
        "make eco-status",
        "python -m pytest -q",
        "make eco-check",
        "make eco-check-clean",
        "make eco-validate-synthetic-demos",
        "make sne-validation",
        "green",
        "attention",
        "recovery",
        "sin entrenamiento",
        "sin datos sensibles",
        "recalibrar umbrales",
    ]

    for token in required_tokens:
        assert token in content


def test_readme_links_operational_panel_index():
    content = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "docs/operations/eco-operational-panel-index.md" in content
    assert "Índice operativo de comandos y estados E.C.O." in content


def test_makefile_exposes_operational_panel_index_target():
    content = (ROOT / "Makefile").read_text(encoding="utf-8")

    assert "eco-operational-panel-index:" in content
    assert "docs/operations/eco-operational-panel-index.md" in content
