from pathlib import Path


def test_claims_and_limits_doc_exists():
    path = Path("docs/sne-eco-claims-and-limits.md")
    assert path.exists()
    assert path.stat().st_size > 1500


def test_claims_and_limits_mentions_allowed_and_forbidden_claims():
    text = Path("docs/sne-eco-claims-and-limits.md").read_text(encoding="utf-8")
    assert "Afirmaciones permitidas" in text
    assert "Afirmaciones no permitidas" in text
    assert "docs/sne-eco-evidence-matrix.md" in text


def test_claims_and_limits_keeps_responsible_boundaries():
    text = Path("docs/sne-eco-claims-and-limits.md").read_text(encoding="utf-8")
    assert "No tiene uso clínico" in text
    assert "no diagnóstico" in text
    assert "no forense" in text
    assert "conciencia humana" in text
