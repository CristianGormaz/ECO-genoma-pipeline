from pathlib import Path


COMPARISON = Path("docs/architecture/eco-synthetic-demo-comparison.md")
INDEX = Path("docs/architecture/eco-synthetic-demos-index.md")


def test_synthetic_demo_comparison_exists_and_lists_all_demos():
    text = COMPARISON.read_text(encoding="utf-8")

    assert "Comparación de demos sintéticas E.C.O." in text
    assert "Minimal simulation" in text
    assert "Signal balance" in text
    assert "Waste pressure" in text
    assert "Absorption threshold" in text


def test_synthetic_demo_comparison_declares_responsible_limits():
    text = COMPARISON.read_text(encoding="utf-8")

    assert "demos sintéticas" in text
    assert "no datos sensibles" in text
    assert "no entrenamiento de modelos" in text
    assert "no modificación de baseline" in text
    assert "no recalibración de umbrales" in text
    assert "no convierte metáforas simbólicas" in text


def test_synthetic_demo_index_links_comparison():
    text = INDEX.read_text(encoding="utf-8")

    assert "eco-synthetic-demo-comparison.md" in text
    assert "Comparación de demos sintéticas E.C.O." in text
