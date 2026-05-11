from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_evidence_governance_index_exists_and_orders_route():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-governance-index.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Índice de gobernanza de evidencia externa",
        "Ruta recomendada",
        "Política de evidencia externa",
        "Checklist de evidencia externa",
        "Registro de evidencia externa",
        "Ejemplo de registro",
        "Guía de revisión de evidencia externa",
        "Matriz de escenarios externos",
    ]

    for token in required_tokens:
        assert token in content


def test_external_evidence_governance_index_mentions_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-governance-index.md"
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
