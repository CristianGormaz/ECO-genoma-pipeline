from pathlib import Path


def test_eco_real_data_reactivation_policy_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-reactivation-policy.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "reactivación" in text
    assert "Reactivar no significa usar datos reales automáticamente" in text
    assert "needs_review" in text
    assert "blocked" in text
    assert "No autoriza ingerir datos reales" in text
    assert "No autoriza entrenar modelos" in text
    assert "No autoriza modificar baseline" in text
    assert "No autoriza recalibrar umbrales" in text
    assert "no realiza afirmaciones biomédicas aplicadas" in text
    assert "eco-real-data-reactivation-policy.md" in readme_text
