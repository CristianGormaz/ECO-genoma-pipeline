from pathlib import Path


def test_admission_governance_index_exists_and_documents_chain():
    content = Path("docs/sne-eco-admission-governance-index.md").read_text(
        encoding="utf-8"
    )

    required_terms = [
        "sne-eco-v1.0-rc1",
        "external scenario probe",
        "external evidence review",
        "external evidence policy",
        "stable admission plan",
        "stable admission dry-run",
        "comparison against RC1",
        "Dataset estable modificado: False",
        "Baseline modificado: False",
        "No modela conciencia humana",
    ]

    for term in required_terms:
        assert term in content
