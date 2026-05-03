from pathlib import Path


def test_architecture_map_exists():
    path = Path("docs/sne-eco-architecture-map.md")
    assert path.exists()
    assert path.stat().st_size > 700


def test_architecture_map_mentions_core_flow():
    text = Path("docs/sne-eco-architecture-map.md").read_text(encoding="utf-8")
    assert "entrada → barrera → motilidad → defensa → estado → reporte" in text
    assert "make sne-portfolio-demo" in text


def test_architecture_map_mentions_responsible_limits():
    text = Path("docs/sne-eco-architecture-map.md").read_text(encoding="utf-8")
    assert "clínico" in text
    assert "diagnóstico" in text
    assert "forense" in text
    assert "conciencia humana" in text
