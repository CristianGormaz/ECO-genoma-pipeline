from pathlib import Path


MAKEFILE = Path("Makefile")

CRITICAL_SCRIPT_TARGETS = {
    "eco-status": "scripts/run_eco_status.py",
    "eco-governance-panel": "scripts/run_eco_governance_panel.py",
    "eco-validate-adaptive-dataset-example": "scripts/validate_eco_adaptive_dataset_example.py",
    "eco-adaptive-dataset-readiness-gate": "scripts/run_eco_adaptive_dataset_readiness_gate.py",
    "eco-validate-real-data-source-manifest": "scripts/validate_eco_real_data_source_manifest.py",
    "eco-real-biological-data-admission-dry-run": "scripts/run_eco_real_biological_data_admission_dry_run.py",
    "eco-validate-operational-state-examples": "scripts/validate_eco_operational_state_examples.py",
    "eco-operational-state-examples-report": "scripts/run_eco_operational_state_examples_report.py",
    "eco-validate-synthetic-demos": "scripts/validate_eco_synthetic_demos.py",
    "eco-synthetic-demos-suite-report": "scripts/run_eco_synthetic_demos_suite_report.py",
    "eco-synthetic-demo-comparison-report": "scripts/run_eco_synthetic_demo_comparison_report.py",
    "eco-synthetic-signal-matrix-report": "scripts/run_eco_synthetic_signal_matrix_report.py",
    "eco-synthetic-operational-dashboard": "scripts/run_eco_synthetic_operational_dashboard.py",
    "eco-clean-results": "scripts/clean_eco_results.py",
    "sne-empirical-seed-report": "scripts/run_sne_eco_empirical_seed_report.py",
    "sne-training-readiness": "scripts/run_sne_eco_training_readiness.py",
    "sne-empirical-train-eval-split": "scripts/run_sne_eco_empirical_train_eval_split.py",
    "sne-ml-baseline": "scripts/run_sne_eco_ml_baseline.py",
    "sne-ml-challenge-eval": "scripts/run_sne_eco_ml_challenge_eval.py",
    "sne-sensitive-intake-gate": "scripts/run_sne_eco_sensitive_intake_gate.py",
    "sne-sensitive-source-registry": "scripts/run_sne_eco_sensitive_source_registry.py",
    "sne-sensitive-governance-summary": "scripts/run_sne_eco_sensitive_governance_summary.py",
    "sne-governed-ml-evaluation-gate": "scripts/run_sne_eco_governed_ml_evaluation_gate.py",
    "sne-responsible-experiment-manifest": "scripts/run_sne_eco_responsible_experiment_manifest.py",
    "sne-integration-readiness-report": "scripts/run_sne_eco_integration_readiness_report.py",
    "sne-pr-package-check": "scripts/run_sne_eco_pr_package_check.py",
}

PROHIBITED_DIRECT_PYTHON = (
    "python3 scripts/",
    ".venv/bin/python scripts/",
    ".venv/bin/python3 scripts/",
)


def target_block(text: str, target: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith(f"{target}:"):
            start = index
            break
    assert start is not None, f"Missing Makefile target: {target}"

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith((" ", "\t")) and ":" in line:
            end = index
            break
    return "\n".join(lines[start:end])


def executable_recipe_lines(block: str) -> list[str]:
    lines = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("@#"):
            continue
        lines.append(stripped)
    return lines


def test_makefile_defines_portable_python_variables():
    text = MAKEFILE.read_text(encoding="utf-8")

    assert "PYTHON ?=" in text
    assert "VENV ?=" in text
    assert "PY :=" in text


def test_critical_python_targets_use_py_variable():
    text = MAKEFILE.read_text(encoding="utf-8")

    for target, script_path in CRITICAL_SCRIPT_TARGETS.items():
        block = target_block(text, target)
        executable_lines = "\n".join(executable_recipe_lines(block))

        assert script_path in block
        assert "$(PY)" in executable_lines
        for prohibited in PROHIBITED_DIRECT_PYTHON:
            assert prohibited not in executable_lines


def test_key_targets_still_point_to_expected_scripts():
    text = MAKEFILE.read_text(encoding="utf-8")

    assert "scripts/run_eco_real_biological_data_admission_dry_run.py" in target_block(
        text, "eco-real-biological-data-admission-dry-run"
    )
    assert "scripts/clean_eco_results.py" in target_block(text, "eco-clean-results")
    assert "scripts/run_sne_eco_ml_baseline.py" in target_block(text, "sne-ml-baseline")
    assert "scripts/run_sne_eco_training_readiness.py" in target_block(text, "sne-training-readiness")


def test_eco_check_keeps_dry_run_admission_gate_without_running_make():
    text = MAKEFILE.read_text(encoding="utf-8")
    block = target_block(text, "eco-check")

    assert "$(MAKE) eco-real-biological-data-admission-dry-run" in block
