from pathlib import Path


DOC_PATH = Path("docs/operations/eco-operational-readiness-panel.md")


def test_operational_readiness_panel_exists():
    assert DOC_PATH.exists()


def test_operational_readiness_panel_core_sections():
    text = DOC_PATH.read_text(encoding="utf-8")

    required_sections = [
        "# E.C.O. Operational Readiness Panel v1",
        "## Propósito",
        "## Estado operativo esperado",
        "## Qué tiene E.C.O.",
        "## Qué valida",
        "## Qué bloquea",
        "## Qué reporta",
        "## Qué falta",
        "## Decisión operativa",
        "## Límite responsable",
        "## Fórmula simple del panel",
        "## Lectura simple",
    ]

    for section in required_sections:
        assert section in text


def test_operational_readiness_panel_validation_terms():
    text = DOC_PATH.read_text(encoding="utf-8")

    required_terms = [
        "main",
        "HEAD",
        "origin/main",
        "árbol de trabajo",
        "make eco-status",
        "green",
        "pytest",
        "PR",
        "checks",
        "post-merge",
    ]

    for term in required_terms:
        assert term in text


def test_operational_readiness_panel_responsible_limits():
    text = DOC_PATH.read_text(encoding="utf-8")

    required_limits = [
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "diagnóstico clínico",
        "datos genéticos privados",
        "metáforas simbólicas",
        "conclusiones científicas",
    ]

    for limit in required_limits:
        assert limit in text


def test_operational_readiness_panel_decision_logic():
    text = DOC_PATH.read_text(encoding="utf-8")

    required_decisions = [
        "detenerse",
        "recuperar",
        "continuar",
        "abrir PR",
        "modo recuperación",
        "sprint panel",
        "micro-sprint",
    ]

    for decision in required_decisions:
        assert decision in text
