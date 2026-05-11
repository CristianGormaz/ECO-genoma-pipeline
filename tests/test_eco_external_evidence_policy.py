from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_evidence_policy_exists_and_defines_states():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-policy.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "Política mínima de evidencia externa",
        "Estados de evidencia externa",
        "mentioned",
        "contextual",
        "candidate",
        "accepted_reference",
        "blocked",
    ]

    for token in required_tokens:
        assert token in content


def test_external_evidence_policy_mentions_responsible_boundaries():
    content = (
        ROOT / "docs" / "operations" / "eco-external-evidence-policy.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "sin entrenamiento",
        "sin datos sensibles",
        "sin ingestión automática de datos reales",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin incorporación automática de evidencia externa",
    ]

    for token in required_tokens:
        assert token in content
