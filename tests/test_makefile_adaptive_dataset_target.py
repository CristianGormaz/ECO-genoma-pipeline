from pathlib import Path


def test_makefile_exposes_adaptive_state_dataset_target():
    makefile = Path("Makefile")

    assert makefile.exists()
    content = makefile.read_text(encoding="utf-8")

    assert "sne-state-dataset" in content
    assert "scripts/run_sne_eco_state_dataset.py" in content
    assert "results/sne_eco_state_dataset.json" in content
    assert "results/sne_eco_state_dataset.tsv" in content
    assert "portfolio-demo: check sne-validation sne-state-dataset" in content
    assert "rm -f results/sne_eco_state_dataset.json results/sne_eco_state_dataset.tsv" in content
