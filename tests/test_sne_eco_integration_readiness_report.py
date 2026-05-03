from pathlib import Path

from scripts.run_sne_eco_integration_readiness_report import build_report, to_markdown


def test_integration_readiness_report_builds_green_or_attention():
    report = build_report()

    assert report["status"] in {"green", "attention"}
    assert report["manifest_step_ok"] is True
    assert report["pytest_step_ok"] is True


def test_integration_readiness_report_tracks_git_state():
    report = build_report()

    assert report["branch"]
    assert report["head"]
    assert report["origin_main"]
    assert isinstance(report["ahead_of_main"], int)
    assert isinstance(report["behind_main"], int)


def test_integration_readiness_report_checks_expected_reports():
    report = build_report()

    assert "results/sne_eco_responsible_experiment_manifest.md" in report["expected_reports"]
    assert "results/sne_eco_governed_ml_evaluation_gate.md" in report["expected_reports"]


def test_integration_readiness_report_checks_expected_targets():
    report = build_report()

    assert "sne-responsible-experiment-manifest" in report["expected_targets"]
    assert "sne-governed-ml-evaluation-gate" in report["expected_targets"]


def test_integration_readiness_report_keeps_responsible_limits():
    report = build_report()
    markdown = to_markdown(report)

    assert "no ingiere datos reales" in markdown
    assert "no entrena modelos nuevos" in markdown
    assert "no diagnostica" in markdown
    assert "no tiene uso clínico aplicado" in markdown
    assert "no realiza inferencias forenses" in markdown
    assert "no afirma conciencia humana real" in markdown
    assert "no recalibra umbrales" in markdown
    assert "no modifica baseline estable" in markdown


def test_makefile_has_integration_readiness_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-integration-readiness-report:" in text
    assert "scripts/run_sne_eco_integration_readiness_report.py" in text
