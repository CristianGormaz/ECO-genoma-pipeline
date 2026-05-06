from pathlib import Path


DOC = Path("docs/architecture/eco-simulation-scope.md")


def test_eco_simulation_scope_exists():
    assert DOC.exists()


def test_eco_simulation_scope_defines_responsible_separation():
    text = DOC.read_text(encoding="utf-8")

    assert "Alcance de simulación E.C.O." in text
    assert "Estudiar datos" in text
    assert "Simular comportamiento" in text
    assert "Entrenar modelos" in text
    assert "Evaluar resultados" in text
    assert "Generar hipótesis" in text
    assert "Hacer afirmaciones aplicadas" in text


def test_eco_simulation_scope_declares_limits():
    text = DOC.read_text(encoding="utf-8")

    assert "No usar datos sensibles" in text
    assert "No entrenar modelos con datos sensibles" in text
    assert "No modificar baseline estable" in text
    assert "No recalibrar umbrales" in text
    assert "No hacer afirmaciones biomédicas aplicadas" in text
    assert "No convertir metáforas simbólicas en conclusiones científicas" in text
