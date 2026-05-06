from pathlib import Path


README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
CONTRACT = Path("docs/architecture/eco-synthetic-data-contract.md")


def test_readme_links_synthetic_data_contract():
    text = README.read_text(encoding="utf-8")

    assert "Contrato de datos sintéticos E.C.O." in text
    assert "docs/architecture/eco-synthetic-data-contract.md" in text


def test_project_map_links_synthetic_data_contract():
    text = PROJECT_MAP.read_text(encoding="utf-8")

    assert "eco-synthetic-data-contract.md" in text
    assert "contrato mínimo" in text
    assert "datos sintéticos" in text


def test_synthetic_data_contract_asset_exists():
    assert CONTRACT.exists()
