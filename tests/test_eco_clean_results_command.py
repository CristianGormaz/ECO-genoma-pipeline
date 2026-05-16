import subprocess
import shutil
import sys
from pathlib import Path


MAKEFILE = Path("Makefile")
README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
GUIDE = Path("docs/operations/eco-synthetic-demos-suite-report-guide.md")

RESULTS = [
    Path("results/eco_minimal_simulation_demo.json"),
    Path("results/eco_minimal_simulation_demo.md"),
    Path("results/eco_signal_balance_demo.json"),
    Path("results/eco_signal_balance_demo.md"),
    Path("results/eco_waste_pressure_demo.json"),
    Path("results/eco_waste_pressure_demo.md"),
    Path("results/eco_absorption_threshold_demo.json"),
    Path("results/eco_absorption_threshold_demo.md"),
    Path("results/eco_synthetic_demos_suite_report.json"),
    Path("results/eco_synthetic_demos_suite_report.md"),
    Path("results/eco_synthetic_demo_comparison_report.json"),
    Path("results/eco_synthetic_demo_comparison_report.md"),
    Path("results/eco_synthetic_signal_matrix_report.json"),
    Path("results/eco_synthetic_signal_matrix_report.md"),
    Path("results/eco_synthetic_operational_dashboard.json"),
    Path("results/eco_synthetic_operational_dashboard.md"),
    Path("results/eco_laos_agency_demo.json"),
    Path("results/eco_laos_agency_demo.md"),
    Path("results/eco_operational_state_examples_report.json"),
    Path("results/eco_operational_state_examples_report.md"),
    Path("results/eco_adaptive_dataset_report.json"),
    Path("results/eco_adaptive_dataset_report.md"),
    Path("results/eco_adaptive_dataset_readiness_gate.json"),
    Path("results/eco_adaptive_dataset_readiness_gate.md"),
    Path("results/eco_governance_panel.json"),
    Path("results/eco_governance_panel.md"),
    Path("results/eco_capabilities_report.json"),
    Path("results/eco_capabilities_report.md"),
]


def _make_target_block(text: str, target: str) -> str:
    lines = text.splitlines()
    start = lines.index(f"{target}:")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith("\t") and not line.startswith(" "):
            end = index
            break
    return "\n".join(lines[start:end])


def test_makefile_has_eco_clean_results_command():
    text = MAKEFILE.read_text(encoding="utf-8")
    block = _make_target_block(text, "eco-clean-results")

    assert ".PHONY: eco-clean-results" in text
    assert "eco-clean-results:" in text
    assert "python3 scripts/clean_eco_results.py" in block
    assert "rm -f" not in block


def test_eco_clean_results_removes_generated_artifacts():
    for path in RESULTS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("temporary synthetic artifact", encoding="utf-8")

    command = (
        ["make", "eco-clean-results"]
        if shutil.which("make")
        else [sys.executable, "scripts/clean_eco_results.py"]
    )
    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    for path in RESULTS:
        assert not path.exists()


def test_operational_docs_mention_eco_clean_results():
    for path in [README, PROJECT_MAP, GUIDE]:
        text = path.read_text(encoding="utf-8")
        assert "make eco-clean-results" in text
        assert "results/" in text
        assert "no elimina código" in text
