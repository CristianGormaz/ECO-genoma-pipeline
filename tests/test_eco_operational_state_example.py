import json
from pathlib import Path


def test_eco_operational_state_example_matches_schema_and_limits():
    root = Path(__file__).resolve().parents[1]
    schema_path = root / "docs" / "architecture" / "eco-operational-state-schema.json"
    example_path = root / "docs" / "architecture" / "eco-operational-state-example-dashboard.json"
    doc_path = root / "docs" / "architecture" / "eco-operational-state-example.md"
    index_path = root / "docs" / "architecture" / "README.md"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))
    required_fields = set(schema["required_fields"])

    assert required_fields.issubset(example.keys())
    assert example["classification"] in schema["allowed_values"]["classification"]
    assert example["state_kind"] in schema["allowed_values"]["state_kind"]
    assert example["status"] in schema["allowed_values"]["status"]

    limits = example["responsible_limits"]
    assert limits["uses_sensitive_data"] is False
    assert limits["trains_model"] is False
    assert limits["modifies_baseline"] is False
    assert limits["recalibrates_thresholds"] is False
    assert limits["makes_applied_biomedical_claims"] is False

    doc_text = doc_path.read_text(encoding="utf-8")
    index_text = index_path.read_text(encoding="utf-8")
    assert "eco_synthetic_operational_dashboard_v1" in doc_text
    assert "No usa datos sensibles" in doc_text
    assert "eco-operational-state-example.md" in index_text
