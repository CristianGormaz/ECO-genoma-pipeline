from pathlib import Path


def test_eco_real_data_candidate_manifest_template_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-candidate-manifest-template.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "Esta plantilla no es un manifiesto activo" in text
    assert "candidate_id" in text
    assert "source_name" in text
    assert "license_or_terms" in text
    assert "contains_personal_data" in text
    assert "contains_clinical_data" in text
    assert "contains_private_genetic_data" in text
    assert "checklist_result" in text
    assert "ready_for_manifest" in text
    assert "No ingiere datos reales" in text
    assert "no usa datos sensibles" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-candidate-manifest-template.md" in readme_text
