from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_evidence_register_example_exists_and_is_synthetic():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-register-example.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Ejemplo sintético de registro de evidencia externa",
        "EXT-ECO-SYN-0001",
        "synthetic_reference_note",
        "accept_as_context",
        "No representa una fuente real",
        "No ingiere datos reales",
    ]

    for token in required_tokens:
        assert token in content


def test_external_evidence_register_example_mentions_limits_and_base_register():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-register-example.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "make eco-external-evidence-register",
        "sin entrenamiento",
        "sin datos sensibles",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin incorporación automática de evidencia externa",
        "blocked",
    ]

    for token in required_tokens:
        assert token in content
