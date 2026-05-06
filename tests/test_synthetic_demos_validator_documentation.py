from pathlib import Path


README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
DEMOS_INDEX = Path("docs/architecture/eco-synthetic-demos-index.md")
VALIDATOR = Path("scripts/validate_eco_synthetic_demos.py")


def test_readme_mentions_global_synthetic_demos_validator():
    text = README.read_text(encoding="utf-8")
    assert "Validación global de demos sintéticas E.C.O." in text
    assert "make eco-validate-synthetic-demos" in text


def test_project_map_mentions_global_synthetic_demos_validator():
    text = PROJECT_MAP.read_text(encoding="utf-8")
    assert "Validación sintética global" in text
    assert "make eco-validate-synthetic-demos" in text


def test_synthetic_demos_index_mentions_global_validator():
    text = DEMOS_INDEX.read_text(encoding="utf-8")
    assert "Validador global" in text
    assert "make eco-validate-synthetic-demos" in text
    assert "sin usar datos sensibles" in text


def test_global_validator_asset_exists():
    assert VALIDATOR.exists()
