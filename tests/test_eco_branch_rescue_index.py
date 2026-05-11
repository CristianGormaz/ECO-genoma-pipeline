from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_branch_rescue_index_exists_and_mentions_priorities():
    content = (
        ROOT / "docs" / "operations" / "eco-branch-rescue-index.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Índice de rescate",
        "Gobernanza y evidencia",
        "Baseline, datos y evaluación",
        "Arquitectura bioinspirada",
        "make eco-branch-decision-matrix",
        ".venv/bin/python -m pytest -q",
        "sin entrenamiento",
        "sin datos sensibles",
        "No borrar ramas no mergeadas",
    ]

    for token in required_tokens:
        assert token in content


def test_makefile_exposes_branch_rescue_index_target():
    content = (ROOT / "Makefile").read_text(encoding="utf-8")

    assert "eco-branch-rescue-index:" in content
    assert "docs/operations/eco-branch-rescue-index.md" in content


def test_readme_links_branch_rescue_index():
    content = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "docs/operations/eco-branch-rescue-index.md" in content
