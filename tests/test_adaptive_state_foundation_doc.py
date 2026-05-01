from pathlib import Path


def test_adaptive_state_foundation_document_exists_and_sets_limits():
    doc = Path("docs/fundamentos-modelo-adaptativo-eco.md")

    assert doc.exists()
    content = doc.read_text(encoding="utf-8")

    assert "estímulo → interacción local → cambio de estado interno → salida observable" in content
    assert "estado previo + señales del paquete" in content
    assert "Machine Learning" in content
    assert "No se debe presentar como modelo de conciencia humana" in content
    assert "eco-adaptive-state-dataset" in content
