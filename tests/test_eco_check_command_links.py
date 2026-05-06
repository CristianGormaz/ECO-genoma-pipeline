from pathlib import Path


README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
GUIDE = Path("docs/operations/eco-synthetic-demos-suite-report-guide.md")


def test_readme_mentions_eco_check():
    text = README.read_text(encoding="utf-8")
    assert "make eco-check" in text
    assert "validación global de demos sintéticas" in text


def test_project_map_mentions_eco_check():
    text = PROJECT_MAP.read_text(encoding="utf-8")
    assert "make eco-check" in text


def test_suite_report_guide_mentions_eco_check():
    text = GUIDE.read_text(encoding="utf-8")
    assert "make eco-check" in text
