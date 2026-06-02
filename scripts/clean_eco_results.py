from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ARTIFACTS = (
    "results/eco_minimal_simulation_demo.json",
    "results/eco_minimal_simulation_demo.md",
    "results/eco_signal_balance_demo.json",
    "results/eco_signal_balance_demo.md",
    "results/eco_waste_pressure_demo.json",
    "results/eco_waste_pressure_demo.md",
    "results/eco_absorption_threshold_demo.json",
    "results/eco_absorption_threshold_demo.md",
    "results/eco_synthetic_demos_suite_report.json",
    "results/eco_synthetic_demos_suite_report.md",
    "results/eco_synthetic_demo_comparison_report.json",
    "results/eco_synthetic_demo_comparison_report.md",
    "results/eco_synthetic_signal_matrix_report.json",
    "results/eco_synthetic_signal_matrix_report.md",
    "results/eco_agentic_scaffold_proposal_registry_report.json",
    "results/eco_agentic_scaffold_proposal_registry_report.md",
    "results/eco_synthetic_operational_dashboard.json",
    "results/eco_synthetic_operational_dashboard.md",
    "results/eco_governed_experimental_cycle.json",
    "results/eco_governed_experimental_cycle.md",
    "results/eco_real_biological_data_admission_dry_run.json",
    "results/eco_real_biological_data_admission_dry_run.md",
    "results/eco_laos_agency_demo.json",
    "results/eco_laos_agency_demo.md",
    "results/eco_laos_governance_gate_demo.json",
    "results/eco_laos_governance_gate_demo.md",
    "results/eco_operational_state_examples_report.json",
    "results/eco_operational_state_examples_report.md",
    "results/eco_adaptive_dataset_report.json",
    "results/eco_adaptive_dataset_report.md",
    "results/eco_adaptive_dataset_readiness_gate.json",
    "results/eco_adaptive_dataset_readiness_gate.md",
    "results/eco_governance_panel.json",
    "results/eco_governance_panel.md",
    "results/eco_capabilities_report.json",
    "results/eco_capabilities_report.md",
)


def clean_artifacts() -> int:
    removed = 0
    for relative_path in ARTIFACTS:
        path = ROOT / relative_path
        if not path.is_file() and not path.is_symlink():
            continue
        try:
            path.unlink()
        except FileNotFoundError:
            continue
        removed += 1
    return removed


def main() -> int:
    removed = clean_artifacts()
    print(f"Removed {removed} E.C.O. result artifact(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
