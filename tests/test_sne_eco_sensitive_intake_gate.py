from pathlib import Path

from scripts.run_sne_eco_sensitive_intake_gate import build_report, classify, to_markdown


def test_sensitive_intake_gate_builds_green_report():
    report = build_report()

    assert report["status"] == "green"
    assert report["row_count"] >= 10
    assert report["errors"] == []


def test_sensitive_intake_gate_detects_all_classes():
    report = build_report()

    assert report["counts"]["allowed"] >= 1
    assert report["counts"]["conditional"] >= 1
    assert report["counts"]["blocked"] >= 1


def test_sensitive_intake_gate_blocks_applied_sensitive_use():
    row = {
        "domain": "diagnostic",
        "source_kind": "user_case",
        "contains_personal_data": True,
        "intended_use": "applied_diagnosis",
    }

    assert classify(row) == "blocked"


def test_sensitive_intake_gate_keeps_responsible_limits():
    report = build_report()
    markdown = to_markdown(report)

    assert "no entrena modelos" in markdown
    assert "no diagnostica" in markdown
    assert "no tiene uso clínico aplicado" in markdown
    assert "no realiza inferencias forenses" in markdown
    assert "no afirma conciencia humana real" in markdown
    assert "no recalibra umbrales" in markdown
    assert "no modifica baseline estable" in markdown


def test_makefile_has_sensitive_intake_gate_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-sensitive-intake-gate:" in text
    assert "scripts/run_sne_eco_sensitive_intake_gate.py" in text
