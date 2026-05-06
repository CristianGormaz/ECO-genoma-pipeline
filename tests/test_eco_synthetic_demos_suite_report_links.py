from pathlib import Path


README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
GUIDE = Path("docs/operations/eco-add-synthetic-demo-guide.md")


def test_readme_links_synthetic_demos_suite_report():
    text = README.read_text(encoding="utf-8")

    assert "make eco-synthetic-demos-suite-report" in text
    assert "scripts/run_eco_synthetic_demos_suite_report.py" in text
    assert "docs/architecture/eco-synthetic-demo-registry.json" in text


def test_project_map_links_synthetic_demos_suite_report():
    text = PROJECT_MAP.read_text(encoding="utf-8")

    assert "Reporte suite sintética" in text
    assert "make eco-synthetic-demos-suite-report" in text
    assert "scripts/run_eco_synthetic_demos_suite_report.py" in text


def test_add_demo_guide_mentions_suite_report_validation():
    text = GUIDE.read_text(encoding="utf-8")

    assert "make eco-synthetic-demos-suite-report" in text
    assert "scripts/run_eco_synthetic_demos_suite_report.py" in text
    assert "eco_synthetic_demos_suite_report.json" in text
