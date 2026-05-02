from pathlib import Path


def test_readme_documents_admission_governance_command():
    content = Path("README.md").read_text(encoding="utf-8")

    required_terms = [
        "make sne-admission-governance",
        "Gobernanza de admisión posterior a RC1",
        "sne-eco-v1.0-rc1",
        "Dataset estable modificado: False",
        "Baseline modificado: False",
        "yellow no representa falla",
    ]

    for term in required_terms:
        assert term in content
