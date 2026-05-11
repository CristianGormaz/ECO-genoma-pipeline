from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_baseline_change_review_checklist_exists_and_mentions_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-baseline-change-review-checklist.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Checklist de revisión de cambios de baseline",
        "No modifica baseline",
        "No recalibra umbrales",
        "No entrena modelos",
        "No incorpora datos sensibles",
        "No incorpora datos reales",
    ]

    for token in required_tokens:
        assert token in content


def test_baseline_change_review_checklist_blocks_sensitive_changes():
    content = (
        ROOT / "docs" / "operations" / "eco-baseline-change-review-checklist.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "compare_required",
        "audit_required",
        "blocked",
        "modifica baseline sin comparación previa",
        "recalibra umbrales sin auditoría",
        "usa datos sensibles",
        "usa datos genéticos privados",
        "incorpora datos reales sin manifiesto",
        "afirmaciones biomédicas aplicadas",
    ]

    for token in required_tokens:
        assert token in content
