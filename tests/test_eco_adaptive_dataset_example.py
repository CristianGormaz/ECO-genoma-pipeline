import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_DOC = ROOT / "docs" / "architecture" / "eco-adaptive-dataset-example.json"
MD_DOC = ROOT / "docs" / "architecture" / "eco-adaptive-dataset-example.md"

REQUIRED_RECORD_KEYS = {
    "record_id",
    "source_type",
    "adaptive_state",
    "signal_family",
    "evidence_level",
    "risk_flag",
    "review_status",
    "notes",
}

ALLOWED_SOURCE_TYPES = {"synthetic", "documental", "mock"}
ALLOWED_REVIEW_STATUSES = {"draft", "review_needed", "candidate", "accepted", "blocked"}


def test_adaptive_dataset_example_files_exist():
    assert JSON_DOC.exists()
    assert MD_DOC.exists()


def test_adaptive_dataset_example_declares_responsible_limits():
    payload = json.loads(JSON_DOC.read_text(encoding="utf-8"))

    assert payload["classification"] == "permitido"
    assert payload["scope"] == "synthetic_documental_example"
    assert payload["contract"] == "docs/architecture/eco-adaptive-dataset-contract.md"

    limits = payload["limits"]
    assert limits["synthetic_only"] is True
    assert limits["no_real_data"] is True
    assert limits["no_sensitive_data"] is True
    assert limits["no_private_genetic_data"] is True
    assert limits["no_training"] is True
    assert limits["no_baseline_change"] is True
    assert limits["no_threshold_recalibration"] is True
    assert limits["no_biomedical_claims"] is True


def test_adaptive_dataset_example_records_follow_contract_shape():
    payload = json.loads(JSON_DOC.read_text(encoding="utf-8"))
    records = payload["records"]

    assert len(records) == 2

    for record in records:
        assert set(record) == REQUIRED_RECORD_KEYS
        assert record["source_type"] in ALLOWED_SOURCE_TYPES
        assert record["review_status"] in ALLOWED_REVIEW_STATUSES
        assert record["record_id"].startswith("eco-synth-adaptive-")


def test_adaptive_dataset_example_markdown_explains_blocked_use():
    content = MD_DOC.read_text(encoding="utf-8")

    required_tokens = [
        "Ejemplo sintético de dataset adaptativo E.C.O.",
        "No contiene datos reales.",
        "No contiene datos sensibles.",
        "No contiene datos genéticos privados.",
        "No entrena modelos.",
        "No modifica baseline.",
        "No recalibra umbrales.",
        "No usar este ejemplo como fuente de entrenamiento",
    ]

    for token in required_tokens:
        assert token in content
