from pathlib import Path

from scripts.run_sne_eco_sensitive_governance_summary import build_report, to_markdown


def test_sensitive_governance_summary_builds_green_report():
    report = build_report()

    assert report["status"] == "green"
    assert report["intake_status"] == "green"
    assert report["source_registry_status"] == "green"
    assert report["intake_row_count"] >= 10
    assert report["source_count"] >= 12


def test_sensitive_governance_summary_counts_all_classes():
    report = build_report()
    counts = report["combined_counts"]

    assert counts["allowed"] >= 1
    assert counts["conditional"] >= 1
    assert counts["blocked"] >= 1


def test_sensitive_governance_summary_tracks_blocked_items():
    report = build_report()

    assert "intake_blocked_real_diagnosis_001" in report["blocked_intake_rows"]
    assert "source_blocked_user_diagnosis_case_001" in report["blocked_sources"]
    assert "source_blocked_forensic_person_case_001" in report["blocked_sources"]


def test_sensitive_governance_summary_keeps_responsible_limits():
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


def test_makefile_has_sensitive_governance_summary_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-sensitive-governance-summary:" in text
    assert "scripts/run_sne_eco_sensitive_governance_summary.py" in text
