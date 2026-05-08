from pathlib import Path


def test_eco_real_data_candidate_manifest_example_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-candidate-manifest-example.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "Example candidate manifest" in text
    assert "eco_real_data_candidate_manifest_example_v1" in text
    assert "documentation_example_only" in text
    assert "example_only_not_approved_source" in text
    assert "No debe guardarse todavía" in text
    assert "No ingiere datos reales" in text
    assert "no usa datos sensibles" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-candidate-manifest-example.md" in readme_text
