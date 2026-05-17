from pathlib import Path


def test_eco_variable_autonomy_document_contract() -> None:
    doc_path = Path("docs/operations/eco-variable-autonomy.md")
    assert doc_path.exists(), "Debe existir el documento de autonomía variable"

    text = doc_path.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert "Autonomía Variable en E.C.O." in text
    assert "autonomía variable" in lower_text
    assert "IAFA" in text
    assert "revisión humana" in lower_text
    assert "gate documental" in lower_text

    for level in ["Nivel 0", "Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4"]:
        assert level in text

    assert "baja confianza" in lower_text
    assert "trazabilidad" in lower_text

    required_limits = [
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin ejecución autónoma de herramientas",
        "sin control de agentes",
        "sin decisiones clínicas",
        "sin conciencia",
        "sin libre albedrío real",
    ]
    for item in required_limits:
        assert item in lower_text

    required_non_scope = [
        "no implementa lógica funcional",
        "sin telemetría real",
        "sin inferencia activa",
        "sin pid",
        "sin fuzzy logic",
    ]
    for item in required_non_scope:
        assert item in lower_text
