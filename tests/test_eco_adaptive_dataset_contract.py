from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "architecture" / "eco-adaptive-dataset-contract.md"


def test_adaptive_dataset_contract_exists_and_declares_scope():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "Contrato documental de dataset adaptativo E.C.O.",
        "Clasificación: condicional",
        "No contiene datos reales",
        "No contiene datos sensibles",
        "No contiene datos genéticos privados",
        "No entrena modelos",
        "No modifica baseline",
        "No recalibra umbrales",
    ]

    for token in required_tokens:
        assert token in content


def test_adaptive_dataset_contract_mentions_allowed_fields_and_blockers():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "`record_id`",
        "`source_type`",
        "`adaptive_state`",
        "`signal_family`",
        "`evidence_level`",
        "`risk_flag`",
        "`review_status`",
        "Criterios de bloqueo",
    ]

    for token in required_tokens:
        assert token in content
