from pathlib import Path


def test_demo_walkthrough_exists():
    path = Path("docs/sne-eco-demo-walkthrough.md")
    assert path.exists()
    assert path.stat().st_size > 500


def test_demo_walkthrough_mentions_main_command():
    text = Path("docs/sne-eco-demo-walkthrough.md").read_text(encoding="utf-8")
    assert "make sne-portfolio-demo" in text
    assert "189 passed" in text
    assert "S.N.E.-E.C.O. portfolio demo ready" in text


def test_portfolio_index_links_demo_walkthrough():
    text = Path("docs/sne-eco-portfolio-index.md").read_text(encoding="utf-8")
    assert "docs/sne-eco-demo-walkthrough.md" in text
    assert "make sne-portfolio-demo" in text
