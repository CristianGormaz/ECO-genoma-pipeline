from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_branch_decision_matrix_exists_and_mentions_core_decisions():
    content = (
        ROOT / "docs" / "operations" / "eco-branch-decision-matrix.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Matriz de decisión",
        "no destructivo",
        "REVISAR PRIMERO - gobernanza/evidencia",
        "REVISAR PRIMERO - sensible por baseline/datos",
        "CONSERVAR - arquitectura bioinspirada",
        "NO TOCAR - respaldo local",
    ]

    for token in required_tokens:
        assert token in content


def test_readme_links_branch_decision_matrix():
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/operations/eco-branch-decision-matrix.md" in content


def test_makefile_exposes_branch_decision_matrix_target():
    content = (ROOT / "Makefile").read_text(encoding="utf-8")
    assert "eco-branch-decision-matrix:" in content
