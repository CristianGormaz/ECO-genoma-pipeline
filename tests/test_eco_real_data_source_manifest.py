import json
from pathlib import Path


def test_eco_real_data_source_manifest_schema_and_doc_limits():
    root = Path(__file__).resolve().parents[1]
    schema_path = root / "docs" / "architecture" / "eco-real-data-source-manifest-schema.json"
    doc_path = root / "docs" / "architecture" / "eco-real-data-source-manifest.md"
    readme_path = root / "docs" / "architecture" / "README.md"

    assert schema_path.exists()
    assert doc_path.exists()

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = set(schema["required_fields"])
    limits = schema["responsible_limits"]
    doc_text = doc_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")

    assert schema["schema_id"] == "eco_real_data_source_manifest_v1"
    assert {"source_id", "origin", "license_or_permission", "sensitivity_classification", "readiness_decision"}.issubset(required)
    assert "condicional" in schema["allowed_values"]["sensitivity_classification"]
    assert "block" in schema["allowed_values"]["readiness_decision"]
    assert limits["ingests_real_data"] is False
    assert limits["uses_sensitive_data"] is False
    assert limits["trains_model"] is False
    assert limits["recalibrates_thresholds"] is False
    assert "No usa datos sensibles" in doc_text
    assert "no entrena modelos" in doc_text
    assert "eco-real-data-source-manifest.md" in readme_text
