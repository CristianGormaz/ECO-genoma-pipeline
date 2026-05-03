from pathlib import Path


def test_portfolio_check_tracks_v1_1_comparison_report():
    text = Path("scripts/run_sne_eco_portfolio_check.py").read_text(encoding="utf-8")
    assert "results/sne_eco_compare_against_v1_1.json" in text
    assert "results/sne_eco_compare_against_rc1.json" in text
