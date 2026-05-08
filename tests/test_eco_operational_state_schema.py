import json
from pathlib import Path


def test_eco_operational_state_schema_limits_and_index_link():
    root = Path(__file__).resolve().parents[1]
    schema_path = root / "docs" / "architecture" / "eco-operational-state-schema.json"
    doc_path = root / "docs" / "architecture" / "eco-operational-state-schema.md"
    index_path = root / "docs" / "architecture" / "README.md"

    assert schema_path.exists()
    assert doc_path.exists()
    assert index_path.exists()

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = set(schema["required_fields"])
    limits = schema["responsible_limits"]

    assert schema["schema_id"] == "eco_operational_state_schema_v1"
    assert {"state_id", "state_kind", "classification", "status", "responsible_limits"}.issubset(required)
    assert "permitido" in schema["allowed_values"]["classification"]
    assert "blocked" in schema["allowed_values"]["status"]

    assert limits["uses_sensitive_data"] is False
    assert limits["trains_model"] is False
    assert limits["modifies_baseline"] is False
    assert limits["recalibrates_thresholds"] is False
    assert limits["makes_applied_biomedical_claims"] is False

    doc_text = doc_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    assert "No usa datos sensibles" in doc_text
    assert "no entrena modelos" in doc_text
    assert "eco-operational-state-schema.md" in index_text
