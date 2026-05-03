from pathlib import Path


def test_glossary_exists():
    path = Path("docs/sne-eco-glossary.md")
    assert path.exists()
    assert path.stat().st_size > 1200


def test_glossary_mentions_core_terms():
    text = Path("docs/sne-eco-glossary.md").read_text(encoding="utf-8")
    assert "Motilidad" in text
    assert "Inmunidad informacional" in text
    assert "Interocepción" in text
    assert "Homeostasis" in text
    assert "Baseline" in text


def test_glossary_mentions_responsible_limits():
    text = Path("docs/sne-eco-glossary.md").read_text(encoding="utf-8")
    assert "clínico" in text
    assert "diagnostican" in text
    assert "forense" in text
    assert "conciencia humana" in text
