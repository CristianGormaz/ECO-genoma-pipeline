import importlib.util
import json
from pathlib import Path


REGISTRY = Path("docs/architecture/eco-synthetic-demo-registry.json")
REGISTRY_DOC = Path("docs/architecture/eco-synthetic-demo-registry.md")
VALIDATOR = Path("scripts/validate_eco_synthetic_demos.py")


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_eco_synthetic_demos", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_registry_json_exists_and_declares_safe_scope():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    assert data["classification"] == "allowed"
    assert data["data_policy"] == "synthetic_only"
    assert data["training"] is False
    assert data["sensitive_data"] is False
    assert data["baseline_changed"] is False
    assert data["threshold_recalibrated"] is False


def test_registry_json_lists_current_demos():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    demo_ids = {demo["id"] for demo in data["demos"]}

    assert "minimal_simulation" in demo_ids
    assert "signal_balance" in demo_ids


def test_validator_loads_registry():
    module = load_validator_module()
    data = module.load_registry()

    demo_ids = {demo["id"] for demo in data["demos"]}
    assert "minimal_simulation" in demo_ids
    assert "signal_balance" in demo_ids
    assert "waste_pressure" in demo_ids
    assert data["data_policy"] == "synthetic_only"


def test_registry_doc_mentions_operational_manifest():
    text = REGISTRY_DOC.read_text(encoding="utf-8")

    assert "eco-synthetic-demo-registry.json" in text
    assert "make eco-validate-synthetic-demos" in text
