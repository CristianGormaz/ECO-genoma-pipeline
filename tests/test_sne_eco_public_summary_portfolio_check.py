from pathlib import Path


def test_portfolio_check_requires_public_summary():
    script = Path("scripts/run_sne_eco_portfolio_check.py")
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "docs/sne-eco-public-summary.md" in text


def test_public_summary_is_present_for_portfolio_check():
    path = Path("docs/sne-eco-public-summary.md")
    assert path.exists()

    text = path.read_text(encoding="utf-8")

    assert "Resumen público" in text
    assert "E.C.O. — Entérico Codificador Orgánico" in text
    assert "No diagnostica" in text
