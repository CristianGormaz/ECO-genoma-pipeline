from pathlib import Path


def test_eco_real_data_candidate_decision_record_documents_fields_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-candidate-decision-record.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "decision record" in text
    assert "accepted_for_manifest" in text
    assert "needs_review" in text
    assert "blocked" in text
    assert "decision_date" in text
    assert "decision_reason" in text
    assert "responsible_limit" in text
    assert "No ingiere datos reales" in text
    assert "no usa datos sensibles" in text
    assert "no recalibra umbrales" in text
    assert "eco-real-data-candidate-decision-record.md" in readme_text
