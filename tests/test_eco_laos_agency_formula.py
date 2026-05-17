from pathlib import Path


def test_eco_laos_agency_formula_document_contract() -> None:
    doc_path = Path("docs/operations/eco-laos-agency-formula.md")
    assert doc_path.exists(), "Debe existir el documento LAOS"

    text = doc_path.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert "LAOS" in text
    assert "IAFA" in text
    assert "Libre Albedrío Operativo Simulado" in text
    assert "Índice de Agencia Funcional Adaptativa" in text
    assert "alias conceptual" in lower_text
    assert "agencia simulada" in lower_text

    assert "LAOS(t)" in text
    assert "O × M × P × V × K" in text
    assert "1 + R + I + N + A" in text
    assert "heurística documental v1" in lower_text
    assert "no es métrica productiva final" in lower_text

    for symbol in ["O", "M", "P", "V", "K", "R", "I", "N", "A"]:
        assert symbol in text

    assert "normalización entre 0 y 1" in lower_text
    assert "autodesarrollo gobernado" in lower_text
    assert "revisión humana" in lower_text
    assert "autonomía variable" in lower_text
    assert "revisión humana graduada" in lower_text
    assert "sin telemetría real" in lower_text
    assert "sin inferencia activa" in lower_text
    assert "sin pid" in lower_text
    assert "sin fuzzy logic" in lower_text
    assert "sin control de agentes" in lower_text
    assert "sin ejecución autónoma de herramientas" in lower_text

    assert "no representa libre albedrío real" in lower_text

    required_limits = [
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin conciencia",
        "sin libre albedrío real",
    ]
    for item in required_limits:
        assert item in lower_text
