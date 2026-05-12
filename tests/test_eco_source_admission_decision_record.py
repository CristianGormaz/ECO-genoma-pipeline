from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_RECORD = ROOT / "docs" / "operations" / "eco-source-admission-decision-record.md"


def test_source_admission_decision_record_exists():
    assert DECISION_RECORD.exists()


def test_source_admission_decision_record_declares_responsible_limits():
    text = DECISION_RECORD.read_text(encoding="utf-8").lower()

    required_limits = [
        "no ingiere datos reales",
        "no habilita entrenamiento",
        "no modifica baseline",
        "no recalibra umbrales",
        "no produce afirmaciones biomédicas aplicadas",
    ]

    for limit in required_limits:
        assert limit in text


def test_source_admission_decision_record_tracks_required_decisions():
    text = DECISION_RECORD.read_text(encoding="utf-8").lower()

    required_decisions = [
        "origen de datos",
        "licencia o permiso de uso",
        "ausencia de datos sensibles",
        "propósito no clínico",
        "criterios de exclusión",
        "validación documental",
        "separación entre simulación, evaluación e interpretación",
    ]

    for decision in required_decisions:
        assert decision in text


def test_source_admission_decision_record_links_existing_governance_pieces():
    text = DECISION_RECORD.read_text(encoding="utf-8")

    required_paths = [
        "docs/operations/eco-adaptive-dataset-cycle-snapshot.md",
        "data/governance/sne_eco_sensitive_source_registry.jsonl",
        "scripts/run_sne_eco_sensitive_source_registry.py",
        "docs/architecture/eco-real-data-source-manifest-validator.md",
    ]

    for relative_path in required_paths:
        assert relative_path in text
        assert (ROOT / relative_path).exists(), relative_path
