from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_governance_evidence_review_exists_and_mentions_core_limits():
    content = (
        ROOT / "docs" / "operations" / "eco-governance-evidence-review.md"
    ).read_text(encoding="utf-8")

    required_tokens = [
        "gobernanza",
        "evidencia externa",
        "sin entrenamiento",
        "sin datos sensibles",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin incorporación automática de evidencia externa",
        "No hace cherry-pick",
        "No borra ramas",
    ]

    for token in required_tokens:
        assert token in content


def test_governance_evidence_review_mentions_priority_branches():
    content = (
        ROOT / "docs" / "operations" / "eco-governance-evidence-review.md"
    ).read_text(encoding="utf-8")

    required_branches = [
        "eco-sne-stable-admission-plan",
        "eco-sne-stable-admission-dry-run",
        "eco-sne-external-evidence-policy",
        "eco-sne-external-evidence-review",
        "eco-sne-external-scenario-expansion",
        "eco-sne-admission-governance-command",
    ]

    for branch in required_branches:
        assert branch in content


def test_readme_links_governance_evidence_review():
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/operations/eco-governance-evidence-review.md" in content
