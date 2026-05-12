from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adaptive_dataset_index_exists_and_links_core_files():
    index = ROOT / "docs" / "operations" / "eco-adaptive-dataset-index.md"
    assert index.exists()

    text = index.read_text(encoding="utf-8")

    required_paths = [
        "docs/architecture/eco-adaptive-dataset-contract.md",
        "docs/architecture/eco-adaptive-dataset-example.json",
        "docs/architecture/eco-adaptive-dataset-example.md",
        "scripts/validate_eco_adaptive_dataset_example.py",
        "scripts/run_eco_adaptive_dataset_report.py",
        "docs/operations/eco-adaptive-dataset-report-guide.md",
        "scripts/run_eco_synthetic_operational_dashboard.py",
    ]

    for relative_path in required_paths:
        assert relative_path in text
        assert (ROOT / relative_path).exists(), relative_path


def test_adaptive_dataset_index_declares_responsible_limits():
    index = ROOT / "docs" / "operations" / "eco-adaptive-dataset-index.md"
    text = index.read_text(encoding="utf-8").lower()

    required_tokens = [
        "sin datos reales",
        "sin datos sensibles",
        "sin datos genéticos privados",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
    ]

    for token in required_tokens:
        assert token in text


def test_readme_links_adaptive_dataset_index():
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")

    assert "docs/operations/eco-adaptive-dataset-index.md" in text
