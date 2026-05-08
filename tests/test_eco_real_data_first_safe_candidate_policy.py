from pathlib import Path


def test_eco_real_data_first_safe_candidate_policy_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-first-safe-candidate-policy.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "Primer candidato seguro" in text
    assert "datos ambientales públicos agregados" in text
    assert "No contiene personas identificables" in text
    assert "No contiene datos genéticos humanos" in text
    assert "No ingiere datos reales" in text
    assert "no usa datos sensibles" in text
    assert "no entrena modelos" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-first-safe-candidate-policy.md" in readme_text
