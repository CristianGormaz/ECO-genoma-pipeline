from pathlib import Path


def test_eco_real_data_candidate_lifecycle_documents_flow_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-candidate-lifecycle.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "ciclo de vida" in text
    assert "Descubrimiento de candidato" in text
    assert "ready_for_manifest" in text
    assert "manifest_validated" in text
    assert "approved_for_structural_use" in text
    assert "Gate 1: seguridad inicial" in text
    assert "Gate 5: validación" in text
    assert "Datos genéticos humanos privados" in text
    assert "No ingiere datos reales" in text
    assert "no usa datos sensibles" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-candidate-lifecycle.md" in readme_text
