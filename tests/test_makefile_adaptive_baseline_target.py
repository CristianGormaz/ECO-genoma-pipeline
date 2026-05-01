from pathlib import Path


def test_makefile_exposes_adaptive_state_baseline_target():
    makefile = Path("Makefile")

    assert makefile.exists()
    content = makefile.read_text(encoding="utf-8")

    assert "sne-state-baseline" in content
    assert "scripts/run_sne_eco_state_baseline.py" in content
    assert "results/sne_eco_state_baseline_report.json" in content
    assert "results/sne_eco_state_baseline_report.md" in content
    assert "portfolio-demo: check sne-validation sne-state-dataset sne-state-baseline" in content
    assert "rm -f results/sne_eco_state_baseline_report.json results/sne_eco_state_baseline_report.md" in content
