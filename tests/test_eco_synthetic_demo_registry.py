from pathlib import Path


REGISTRY = Path("docs/architecture/eco-synthetic-demo-registry.md")
INDEX = Path("docs/architecture/eco-synthetic-demos-index.md")


def test_synthetic_demo_registry_exists_and_lists_demos():
    text = REGISTRY.read_text(encoding="utf-8")

    assert "Registro de demos sintéticas E.C.O." in text
    assert "Minimal simulation" in text
    assert "Signal balance" in text
    assert "scripts/run_eco_minimal_simulation.py" in text
    assert "scripts/run_eco_signal_balance_demo.py" in text


def test_synthetic_demo_registry_declares_outputs_and_validator():
    text = REGISTRY.read_text(encoding="utf-8")

    assert "results/eco_minimal_simulation_demo.json" in text
    assert "results/eco_signal_balance_demo.json" in text
    assert "scripts/validate_eco_synthetic_contract.py" in text
    assert "make eco-validate-synthetic-demos" in text


def test_synthetic_demo_registry_declares_responsible_limits():
    text = REGISTRY.read_text(encoding="utf-8")

    assert "no entrena modelos" in text
    assert "no modifica baseline" in text
    assert "no recalibra umbrales" in text
    assert "no usa datos sensibles" in text


def test_synthetic_demos_index_links_registry():
    text = INDEX.read_text(encoding="utf-8")

    assert "eco-synthetic-demo-registry.md" in text
    assert "Registro de demos" in text
