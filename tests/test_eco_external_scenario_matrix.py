from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_scenario_matrix_exists_and_defines_states():
    content = (
        ROOT / "docs" / "operations" / "eco-external-scenario-matrix.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Matriz de escenarios externos sintéticos",
        "`permitted`",
        "`review_needed`",
        "`blocked`",
        "Matriz operativa",
        "Criterios para permitir",
        "Criterios para revisión",
        "Criterios para bloquear",
    ]

    for token in required_tokens:
        assert token in content


def test_external_scenario_matrix_mentions_responsible_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-external-scenario-matrix.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "sin entrenamiento",
        "sin datos sensibles",
        "sin datos genéticos privados",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin incorporación automática de evidencia externa",
        "sin integración masiva de ramas antiguas",
    ]

    for token in required_tokens:
        assert token in content
