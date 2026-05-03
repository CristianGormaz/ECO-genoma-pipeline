from pathlib import Path


def test_makefile_has_compare_v1_1_target():
    text = Path("Makefile").read_text(encoding="utf-8")
    assert "sne-compare-v1-1:" in text
    assert "scripts/run_sne_eco_compare_against_v1_1.py" in text
