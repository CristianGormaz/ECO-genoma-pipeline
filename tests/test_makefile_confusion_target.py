from pathlib import Path


def test_makefile_exposes_confused_route_analysis_target():
    makefile = Path("Makefile")

    assert makefile.exists()
    content = makefile.read_text(encoding="utf-8")

    assert "sne-state-confusion" in content
    assert "scripts/run_sne_eco_state_confusion.py" in content
    assert "results/sne_eco_state_confusion_report.json" in content
    assert "results/sne_eco_state_confusion_report.md" in content
    assert "portfolio-demo: check sne-validation sne-state-dataset sne-state-baseline sne-state-holdout sne-state-coverage sne-state-confusion" in content
    assert "rm -f results/sne_eco_state_confusion_report.json results/sne_eco_state_confusion_report.md" in content
