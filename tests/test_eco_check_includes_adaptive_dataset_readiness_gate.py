from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_eco_check_includes_adaptive_dataset_readiness_gate():
    makefile = ROOT / "Makefile"
    text = makefile.read_text(encoding="utf-8")

    start = text.index("eco-check:")
    end = text.index("\n\n", start)
    block = text[start:end]

    assert "$(MAKE) eco-adaptive-dataset-readiness-gate" in block


def test_eco_clean_results_removes_adaptive_dataset_readiness_gate_outputs():
    cleaner = ROOT / "scripts" / "clean_eco_results.py"
    text = cleaner.read_text(encoding="utf-8")

    assert "results/eco_adaptive_dataset_readiness_gate.json" in text
    assert "results/eco_adaptive_dataset_readiness_gate.md" in text
