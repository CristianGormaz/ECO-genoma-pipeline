from pathlib import Path


def test_evidence_matrix_exists():
    path = Path("docs/sne-eco-evidence-matrix.md")
    assert path.exists()
    assert path.stat().st_size > 1200


def test_evidence_matrix_mentions_core_artifacts():
    text = Path("docs/sne-eco-evidence-matrix.md").read_text(encoding="utf-8")
    assert "README.md" in text
    assert "docs/sne-eco-glossary.md" in text
    assert "results/sne_eco_neurogastro_context_report.json" in text
    assert "pytest" in text


def test_evidence_matrix_keeps_responsible_limits():
    text = Path("docs/sne-eco-evidence-matrix.md").read_text(encoding="utf-8")
    assert "No tiene uso clínico" in text
    assert "diagnóstico" in text
    assert "forense" in text
    assert "No modela conciencia humana" in text
