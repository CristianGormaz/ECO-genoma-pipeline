from pathlib import Path


def test_makefile_exposes_admission_governance_target():
    content = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-admission-governance" in content
    assert "scripts/run_sne_eco_admission_governance_command.py" in content
    assert "results/sne_eco_admission_governance_command.md" in content
