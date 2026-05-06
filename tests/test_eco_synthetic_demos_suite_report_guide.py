from pathlib import Path


GUIDE = Path("docs/operations/eco-synthetic-demos-suite-report-guide.md")
README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")


def test_suite_report_interpretation_guide_exists():
    text = GUIDE.read_text(encoding="utf-8")

    assert "Guía de interpretación del reporte de suite sintética E.C.O." in text
    assert "make eco-synthetic-demos-suite-report" in text
    assert "Estado: passed" in text
    assert "results/eco_synthetic_demos_suite_report.json" in text
    assert "results/eco_synthetic_demos_suite_report.md" in text


def test_suite_report_guide_declares_responsible_limits():
    text = GUIDE.read_text(encoding="utf-8")

    assert "No usa datos sensibles" in text or "no usa datos sensibles" in text
    assert "no entrena modelos" in text
    assert "no modifica baseline" in text
    assert "no recalibra umbrales" in text


def test_readme_and_project_map_link_suite_report_guide():
    readme_text = README.read_text(encoding="utf-8")
    project_map_text = PROJECT_MAP.read_text(encoding="utf-8")

    assert "eco-synthetic-demos-suite-report-guide.md" in readme_text
    assert "eco-synthetic-demos-suite-report-guide.md" in project_map_text
