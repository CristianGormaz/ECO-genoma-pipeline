from pathlib import Path

from scripts.run_sne_eco_sensitive_source_registry import (
    build_report,
    classify_source,
    to_markdown,
)


def test_sensitive_source_registry_builds_green_report():
    report = build_report()

    assert report["status"] == "green"
    assert report["source_count"] >= 12
    assert report["errors"] == []


def test_sensitive_source_registry_detects_all_statuses():
    report = build_report()

    assert report["counts"]["allowed"] >= 1
    assert report["counts"]["conditional"] >= 1
    assert report["counts"]["blocked"] >= 1


def test_sensitive_source_registry_blocks_personal_data():
    row = {
        "source_kind": "personal_medical_record",
        "license_status": "not_allowed",
        "permitted_use": "study",
        "contains_personal_data": True,
        "gate_required": True,
    }

    assert classify_source(row) == "blocked"


def test_sensitive_source_registry_marks_review_sources_conditional():
    row = {
        "source_kind": "public_dataset",
        "license_status": "requires_review",
        "permitted_use": "study",
        "contains_personal_data": False,
        "gate_required": True,
    }

    assert classify_source(row) == "conditional"


def test_sensitive_source_registry_keeps_responsible_limits():
    report = build_report()
    markdown = to_markdown(report)

    assert "no ingiere datos reales" in markdown
    assert "no entrena modelos" in markdown
    assert "no diagnostica" in markdown
    assert "no tiene uso clínico aplicado" in markdown
    assert "no realiza inferencias forenses" in markdown
    assert "no afirma conciencia humana real" in markdown
    assert "no recalibra umbrales" in markdown
    assert "no modifica baseline estable" in markdown


def test_makefile_has_sensitive_source_registry_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-sensitive-source-registry:" in text
    assert "scripts/run_sne_eco_sensitive_source_registry.py" in text
