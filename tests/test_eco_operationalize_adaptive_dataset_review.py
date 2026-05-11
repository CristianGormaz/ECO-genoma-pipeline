from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "operations" / "eco-operationalize-adaptive-dataset-review.md"


def test_operationalize_adaptive_dataset_review_exists_and_mentions_risks():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "eco-operationalize-adaptive-dataset",
        "Clasificación: condicional",
        "No se hizo merge",
        "No se hizo cherry-pick",
        "No se incorporaron datasets",
        "No se modificó baseline",
        "No se recalibraron umbrales",
    ]

    for token in required_tokens:
        assert token in content


def test_operationalize_adaptive_dataset_review_keeps_responsible_limits():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "sin entrenamiento",
        "sin datos sensibles",
        "sin datos genéticos privados",
        "sin incorporación de datasets reales",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
    ]

    for token in required_tokens:
        assert token in content
