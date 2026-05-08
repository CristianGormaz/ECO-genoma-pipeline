from pathlib import Path


def test_eco_real_data_readiness_gate_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    gate = root / "docs" / "architecture" / "eco-real-data-readiness-gate.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert gate.exists()
    text = gate.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "Datos sintéticos" in text
    assert "Datos reales no sensibles" in text
    assert "bloqueado" in text
    assert "No usa datos sensibles" in text
    assert "no entrena modelos" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-readiness-gate.md" in readme_text
