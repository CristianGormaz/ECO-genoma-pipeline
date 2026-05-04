from pathlib import Path


DOC = Path("docs/sne-eco-sensitive-data-governance.md")


def test_sensitive_data_governance_doc_exists():
    assert DOC.exists()


def test_sensitive_data_governance_has_allowed_conditional_blocked():
    text = DOC.read_text(encoding="utf-8")

    assert "Permitido" in text
    assert "Condicional" in text
    assert "Bloqueado" in text


def test_sensitive_data_governance_keeps_responsible_limits():
    text = DOC.read_text(encoding="utf-8")

    assert "no uso clínico" in text or "uso clínico" in text
    assert "diagnóstico" in text
    assert "forense" in text
    assert "conciencia humana" in text
    assert "sin auditoría" in text


def test_sensitive_data_governance_allows_controlled_research():
    text = DOC.read_text(encoding="utf-8")

    assert "sintético" in text
    assert "público" in text
    assert "anonimizado" in text
    assert "licencia" in text
