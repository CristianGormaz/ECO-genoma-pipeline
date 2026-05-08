from pathlib import Path


def test_eco_real_data_manifest_activation_gate_documents_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "architecture" / "eco-real-data-manifest-activation-gate.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")

    assert "Puerta de activación" in text
    assert "docs/architecture/real-data-source-manifests/" in text
    assert "No activa ingestión de datos" in text
    assert "No contiene datos sensibles" in text
    assert "No modifica baseline" in text
    assert "no recalibra umbrales" in text
    assert "no realiza afirmaciones biomédicas aplicadas" in text
    assert "eco-real-data-manifest-activation-gate.md" in readme_text
