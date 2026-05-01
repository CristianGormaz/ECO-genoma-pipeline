from pathlib import Path


def test_sne_v1_index_document_exists_and_mentions_demo_artifacts():
    doc = Path("docs/sne-eco-v1-indice-demo.md")

    assert doc.exists()
    content = doc.read_text(encoding="utf-8")
    assert "S.N.E.-E.C.O. v1.0" in content
    assert "results/sne_eco_validation_report.md" in content
    assert "results/sne_eco_validation_report.json" in content
    assert "Sistema bioinformático educativo" in content


def test_makefile_connects_sne_validation_to_portfolio_demo():
    makefile = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-validation:" in makefile
    assert "portfolio-demo: check sne-validation" in makefile
    assert "docs/sne-eco-v1-indice-demo.md" in makefile
    assert "results/sne_eco_validation_report.md" in makefile
