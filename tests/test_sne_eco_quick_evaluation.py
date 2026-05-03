from pathlib import Path


def test_quick_evaluation_doc_exists():
    path = Path("docs/sne-eco-quick-evaluation.md")
    assert path.exists()
    assert path.stat().st_size > 500


def test_quick_evaluation_mentions_demo_command():
    text = Path("docs/sne-eco-quick-evaluation.md").read_text(encoding="utf-8")
    assert "make sne-portfolio-demo" in text
    assert "S.N.E.-E.C.O. portfolio demo ready" in text


def test_quick_evaluation_keeps_responsible_limits():
    text = Path("docs/sne-eco-quick-evaluation.md").read_text(encoding="utf-8").lower()
    assert "no tiene uso clínico" in text
    assert "diagnóstico" in text
    assert "forense" in text
    assert "conciencia humana" in text
