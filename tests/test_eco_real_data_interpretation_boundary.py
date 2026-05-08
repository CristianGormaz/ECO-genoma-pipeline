from pathlib import Path


def test_eco_real_data_interpretation_boundary_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-interpretation-boundary.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "observar datos reales" in text
    assert "generar hipótesis" in text
    assert "No diagnosticar" in text
    assert "No usa datos sensibles" in text
    assert "no ingiere datos reales" in text
    assert "no entrena modelos" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-interpretation-boundary.md" in readme_text
