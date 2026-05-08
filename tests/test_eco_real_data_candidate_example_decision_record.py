from pathlib import Path


def test_eco_real_data_candidate_example_decision_record_documents_safe_example_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-candidate-example-decision-record.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "example decision record" in text
    assert "documentation_example_only" in text
    assert "accepted_for_manifest" in text
    assert "eco_candidate_public_environmental_example" in text
    assert "No es una fuente real aprobada" in text
    assert "No contiene personas identificables" in text
    assert "No contiene datos genéticos humanos privados" in text
    assert "No ingiere datos reales" in text
    assert "no usa datos sensibles" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-candidate-example-decision-record.md" in readme_text
