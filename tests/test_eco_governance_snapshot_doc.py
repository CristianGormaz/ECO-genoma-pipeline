from pathlib import Path


def test_eco_governance_snapshot_document_contract() -> None:
    doc_path = Path("docs/operations/eco-governance-snapshot.md")
    assert doc_path.exists(), "Debe existir el snapshot de gobernanza E.C.O."

    text = doc_path.read_text(encoding="utf-8")
    lower_text = text.lower()

    required_text = [
        "Snapshot de Gobernanza E.C.O.",
        "IAFA",
        "LAOS",
        "alias conceptual",
        "Autonomía Variable",
        "índice operativo",
        "validación flexible",
        "cantidad de tests puede cambiar",
        "main limpio",
        "HEAD sincronizado con origin/main",
        "eco-status green",
        "suite passing",
        "sin PR abierto",
    ]
    for item in required_text:
        assert item in text

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
