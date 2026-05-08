from pathlib import Path


def test_eco_real_data_activation_rollback_policy_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-activation-rollback-policy.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "rollback" in text
    assert "freno de emergencia" in text
    assert "needs_review" in text
    assert "blocked" in text
    assert "No autoriza entrenamiento, ingestión ni recalibración" in text
    assert "No ingiere datos reales" in text
    assert "no modifica baseline" in text
    assert "no recalibra umbrales" in text
    assert "no realiza afirmaciones biomédicas aplicadas" in text
    assert "eco-real-data-activation-rollback-policy.md" in readme_text
