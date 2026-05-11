from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_evidence_register_exists_and_has_core_fields():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-register.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Registro de evidencia externa",
        "evidence_id",
        "source_label",
        "source_type",
        "intended_use",
        "admission_decision",
        "responsible_limits",
        "requires_real_data_manifest",
        "baseline_or_threshold_impact",
    ]

    for token in required_tokens:
        assert token in content


def test_external_evidence_register_links_policy_checklist_and_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-register.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "make eco-external-evidence-policy",
        "make eco-external-evidence-checklist",
        "accept_as_context",
        "accept_as_reference",
        "review_needed",
        "blocked",
        "sin entrenamiento",
        "sin datos sensibles",
        "sin ingestión automática de datos reales",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
    ]

    for token in required_tokens:
        assert token in content
