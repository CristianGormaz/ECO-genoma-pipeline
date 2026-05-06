from pathlib import Path


MAKEFILE = Path("Makefile")


def test_makefile_has_eco_check_command():
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: eco-check" in text
    assert "eco-check:" in text
    assert "$(MAKE) eco-status" in text
    assert "$(MAKE) eco-validate-synthetic-demos" in text
    assert "$(MAKE) eco-synthetic-demos-suite-report" in text
    assert "$(PYTHON) -m pytest -q" in text
