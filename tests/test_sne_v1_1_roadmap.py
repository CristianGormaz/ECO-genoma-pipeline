from pathlib import Path


def test_sne_v1_1_roadmap_exists_and_defines_next_steps():
    content = Path("docs/roadmap-sne-eco-v1-1.md").read_text(encoding="utf-8")

    assert "Roadmap S.N.E.-E.C.O. v1.1" in content
    assert "Trazabilidad del paquete" in content
    assert "Reporte HTML S.N.E.-E.C.O." in content
    assert "docs/api-publica-sne-eco.md" in content
    assert "python scripts/run_sne_eco_validation.py --scenario extended" in content
    assert "v1.1 = el sistema se explica, se muestra y se defiende mejor" in content
