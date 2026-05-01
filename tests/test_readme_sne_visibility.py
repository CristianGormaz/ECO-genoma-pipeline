from pathlib import Path


def test_readme_highlights_sne_eco_v1_visibility():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "S.N.E.-E.C.O. v1.0" in content
    assert "make sne-validation" in content
    assert "docs/sne-eco-v1-indice-demo.md" in content
    assert "results/sne_eco_validation_report.md" in content
    assert "results/sne_eco_validation_report.json" in content
    assert "Sistema Nervioso Entérico" in content
