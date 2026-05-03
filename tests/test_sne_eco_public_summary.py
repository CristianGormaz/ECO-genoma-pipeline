from pathlib import Path


def test_public_summary_exists_and_has_core_sections():
    path = Path("docs/sne-eco-public-summary.md")
    assert path.exists()

    text = path.read_text(encoding="utf-8")

    required = [
        "Resumen público",
        "E.C.O. — Entérico Codificador Orgánico",
        "make sne-portfolio-demo",
        "arquitectura experimental y educativa",
        "No diagnostica",
        "software bioinspirado",
        "validación automatizada",
    ]

    for item in required:
        assert item in text


def test_public_summary_is_linked_from_portfolio_index_and_readme():
    index_text = Path("docs/sne-eco-portfolio-index.md").read_text(encoding="utf-8")
    readme_text = Path("README.md").read_text(encoding="utf-8")

    assert "docs/sne-eco-public-summary.md" in index_text
    assert "docs/sne-eco-public-summary.md" in readme_text
