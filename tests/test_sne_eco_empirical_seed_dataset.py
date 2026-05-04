from pathlib import Path
import json


DATASET = Path("data/training/sne_eco_empirical_seed_dataset.jsonl")
DOC = Path("docs/sne-eco-empirical-data-contract.md")


def read_rows():
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_empirical_data_contract_exists():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    assert "no afirma modelar biología humana real" in text
    assert "Datos admisibles" in text
    assert "Datos no admisibles" in text


def test_empirical_seed_dataset_exists_and_has_rows():
    assert DATASET.exists()
    rows = read_rows()
    assert len(rows) >= 6


def test_empirical_seed_dataset_has_required_fields():
    required = {"id", "input_type", "source_text", "expected_barrier", "expected_motility", "expected_decision", "expected_state", "defense_category", "responsible_limit"}
    for row in read_rows():
        assert required.issubset(row.keys())


def test_empirical_seed_dataset_keeps_responsible_limits():
    rows = read_rows()
    limits = " ".join(row["responsible_limit"] for row in rows)
    assert "not_clinical" in limits or "reject_clinical" in limits
    assert "reject_human_consciousness_claim" in limits


def test_empirical_seed_dataset_has_expected_training_labels():
    decisions = {row["expected_decision"] for row in read_rows()}
    assert "absorb" in decisions
    assert "reject" in decisions
    assert "quarantine" in decisions
    assert "discard_duplicate" in decisions
