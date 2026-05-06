from pathlib import Path


MAKEFILE = Path("Makefile")
README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
GUIDE = Path("docs/operations/eco-synthetic-demos-suite-report-guide.md")


def test_makefile_has_eco_check_clean_command():
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: eco-check-clean" in text
    assert "eco-check-clean:" in text
    assert "$(MAKE) eco-check" in text
    assert "$(MAKE) eco-clean-results" in text


def test_docs_mention_eco_check_clean_command():
    readme_text = README.read_text(encoding="utf-8")
    project_map_text = PROJECT_MAP.read_text(encoding="utf-8")
    guide_text = GUIDE.read_text(encoding="utf-8")

    assert "make eco-check-clean" in readme_text
    assert "make eco-check-clean" in project_map_text
    assert "make eco-check-clean" in guide_text
