from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "docs" / "operations" / "eco-adaptive-dataset-cycle-snapshot.md"


def test_adaptive_dataset_cycle_snapshot_exists():
    assert SNAPSHOT.exists()


def test_adaptive_dataset_cycle_snapshot_mentions_current_cycle_prs():
    text = SNAPSHOT.read_text(encoding="utf-8")

    for pr in ["#186", "#187", "#188", "#189", "#190"]:
        assert pr in text


def test_adaptive_dataset_cycle_snapshot_links_core_files():
    text = SNAPSHOT.read_text(encoding="utf-8")

    required_paths = [
        "docs/architecture/eco-adaptive-dataset-contract.md",
        "docs/architecture/eco-adaptive-dataset-example.json",
        "docs/architecture/eco-adaptive-dataset-example.md",
        "docs/operations/eco-adaptive-dataset-index.md",
        "scripts/run_eco_adaptive_dataset_report.py",
        "scripts/run_eco_adaptive_dataset_readiness_gate.py",
        "scripts/run_eco_synthetic_operational_dashboard.py",
    ]

    for relative_path in required_paths:
        assert relative_path in text
        assert (ROOT / relative_path).exists(), relative_path


def test_adaptive_dataset_cycle_snapshot_declares_responsible_limits():
    text = SNAPSHOT.read_text(encoding="utf-8").lower()

    required_limits = [
        "no habilita entrenamiento",
        "no habilita ingestión de datos reales",
        "no modifica baseline",
        "no recalibra umbrales",
        "no produce afirmaciones biomédicas aplicadas",
    ]

    for limit in required_limits:
        assert limit in text
