from pathlib import Path


def test_eco_real_data_candidate_review_checklist_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-candidate-review-checklist.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "Checklist de revisión" in text
    assert "Aceptar para manifiesto" in text
    assert "Revisar antes de avanzar" in text
    assert "Bloquear" in text
    assert "No contiene personas identificables" in text
    assert "No contiene datos genéticos humanos privados" in text
    assert "No se usará para entrenar modelos" in text
    assert "No ingiere datos reales" in text
    assert "no usa datos sensibles" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-candidate-review-checklist.md" in readme_text
