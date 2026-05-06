from pathlib import Path


DOC = Path("docs/architecture/eco-synthetic-demos-index.md")
MINIMAL_SCRIPT = Path("scripts/run_eco_minimal_simulation.py")
SIGNAL_SCRIPT = Path("scripts/run_eco_signal_balance_demo.py")
VALIDATOR = Path("scripts/validate_eco_synthetic_contract.py")


def test_synthetic_demos_index_exists():
    assert DOC.exists()


def test_synthetic_demos_index_mentions_available_demos():
    text = DOC.read_text(encoding="utf-8")

    assert "Índice de demos sintéticas E.C.O." in text
    assert "make eco-minimal-simulation-demo" in text
    assert "make eco-signal-balance-demo" in text
    assert "make eco-validate-synthetic-contract" in text
    assert "make eco-validate-signal-balance-demo" in text
    assert "digest" in text
    assert "rest" in text
    assert "No usar datos sensibles" in text
    assert "No entrenar modelos" in text
    assert "No recalibrar umbrales" in text


def test_synthetic_demo_assets_exist():
    assert MINIMAL_SCRIPT.exists()
    assert SIGNAL_SCRIPT.exists()
    assert VALIDATOR.exists()
