# Revisión de rama: eco-operationalize-adaptive-dataset

Este documento registra una inspección segura de la rama antigua `eco-operationalize-adaptive-dataset`.

## Objetivo

Revisar si la rama contiene piezas rescatables relacionadas con estado adaptativo y dataset operativo, sin integrar datos ni modificar el comportamiento estable del repositorio.

## Clasificación

- Tipo de sprint: documental / auditoría.
- Clasificación: condicional.
- Motivo: la rama puede tocar dataset, evaluación o preparación operativa.
- Acción realizada: inspección de commits, archivos y diff contra `main`.
- No se hizo merge.
- No se hizo cherry-pick.
- No se incorporaron datasets.
- No se entrenaron modelos.
- No se modificó baseline.
- No se recalibraron umbrales.

## Resumen técnico

| Campo | Valor |
|---|---|
| Rama objetivo | `eco-operationalize-adaptive-dataset` |
| Referencia usada | `eco-operationalize-adaptive-dataset` |
| Commits únicos | `2` |
| Archivos cambiados | `297` |
| Último commit | Add test for adaptive dataset make target |

## Lectura operativa

La rama debe tratarse como fuente de ideas, no como paquete listo para integración.

Si contiene archivos de `data/`, `scripts/`, evaluación, entrenamiento, baseline, resultados generados o cambios amplios en `Makefile`, no debe integrarse completa.

## Riesgo detectado

El concepto de dataset adaptativo puede ser útil, pero es sensible porque puede confundirse con entrenamiento, evaluación aplicada o modificación de baseline.

Por seguridad, cualquier rescate futuro debe separar claramente:

1. documentación;
2. ejemplos sintéticos;
3. contratos de datos;
4. scripts operativos;
5. evaluación;
6. baseline;
7. umbrales.

## Áreas sensibles

No rescatar sin revisión separada:

- `data/`;
- datasets reales o semi-reales;
- manifiestos de entrenamiento;
- scripts de evaluación;
- cambios de baseline;
- cambios de umbral;
- resultados generados en `results/`;
- cambios grandes de CI o Makefile.

## Piezas potencialmente rescatables

Rescatar solo en PRs pequeños:

1. Contrato documental de dataset adaptativo.
2. Glosario de campos permitidos.
3. Ejemplo sintético mínimo.
4. Checklist de admisión de dataset.
5. Test documental que bloquee datos sensibles y baseline.

## Decisión recomendada

No integrar `eco-operationalize-adaptive-dataset` como bloque.

El siguiente sprint lógico, si esta revisión queda aceptada, debería ser crear un contrato documental de dataset adaptativo, sin datos reales y sin entrenamiento.

## Comandos seguros usados

```bash
git log --oneline main..eco-operationalize-adaptive-dataset
git diff --name-only main..eco-operationalize-adaptive-dataset
git diff --stat main..eco-operationalize-adaptive-dataset
```

## Commits inspeccionados

```text
28e4d98 Add test for adaptive dataset make target
6c7fd85 Add make target for adaptive state dataset
```

## Archivos inspeccionados

```text
.github/workflows/ci.yml
.github/workflows/eco-check.yml
CHANGELOG.md
Makefile
README.md
data/governance/sne_eco_sensitive_intake_candidates.jsonl
data/governance/sne_eco_sensitive_source_registry.jsonl
data/training/sne_eco_empirical_challenge_eval.jsonl
data/training/sne_eco_empirical_seed_dataset.jsonl
docs/architecture/README.md
docs/architecture/eco-adaptive-state-foundation.md
docs/architecture/eco-minimal-simulation-demo.md
docs/architecture/eco-operational-block-bitacora-131-136.md
docs/architecture/eco-operational-state-example-dashboard.json
docs/architecture/eco-operational-state-example.md
docs/architecture/eco-operational-state-schema.json
docs/architecture/eco-operational-state-schema.md
docs/architecture/eco-operational-state-validator.md
docs/architecture/eco-real-data-activation-rollback-policy.md
docs/architecture/eco-real-data-candidate-decision-record.md
docs/architecture/eco-real-data-candidate-example-decision-record.md
docs/architecture/eco-real-data-candidate-lifecycle.md
docs/architecture/eco-real-data-candidate-manifest-example.md
docs/architecture/eco-real-data-candidate-manifest-template.md
docs/architecture/eco-real-data-candidate-review-checklist.md
docs/architecture/eco-real-data-first-safe-candidate-policy.md
docs/architecture/eco-real-data-interpretation-boundary.md
docs/architecture/eco-real-data-manifest-activation-gate.md
docs/architecture/eco-real-data-reactivation-policy.md
docs/architecture/eco-real-data-readiness-gate.md
docs/architecture/eco-real-data-source-manifest-schema.json
docs/architecture/eco-real-data-source-manifest-validator.md
docs/architecture/eco-real-data-source-manifest.md
docs/architecture/eco-simulation-scope.md
docs/architecture/eco-synthetic-data-contract.md
docs/architecture/eco-synthetic-demo-comparison.md
docs/architecture/eco-synthetic-demo-registry.json
docs/architecture/eco-synthetic-demo-registry.md
docs/architecture/eco-synthetic-demos-index.md
docs/architecture/eco-synthetic-operational-dashboard.md
docs/architecture/eco-synthetic-signal-matrix.json
docs/architecture/eco-synthetic-state-timeline.md
docs/case-study-sne-eco-neurogastro-pipeline.md
docs/eco-agent-operational-context.md
docs/guia-baseline-adaptativo-eco.md
docs/guia-diagnostico-cobertura-eco.md
docs/guia-escenarios-sinteticos-extendidos-eco.md
docs/guia-evaluacion-holdout-eco.md
docs/guia-rutas-confundidas-eco.md
docs/operations/eco-adaptive-state-baseline-v0-review.md
docs/operations/eco-adaptive-state-foundation-review.md
docs/operations/eco-add-synthetic-demo-guide.md
docs/operations/eco-admission-review-template.md
docs/operations/eco-baseline-change-review-checklist.md
docs/operations/eco-branch-decision-matrix.md
docs/operations/eco-branch-rescue-index.md
docs/operations/eco-external-evidence-checklist.md
docs/operations/eco-external-evidence-governance-index.md
docs/operations/eco-external-evidence-policy-review.md
docs/operations/eco-external-evidence-policy.md
docs/operations/eco-external-evidence-register-example.md
docs/operations/eco-external-evidence-register.md
docs/operations/eco-external-evidence-review-branch.md
docs/operations/eco-external-evidence-review-guide.md
docs/operations/eco-external-scenario-expansion-review.md
docs/operations/eco-external-scenario-matrix.md
docs/operations/eco-governance-evidence-review.md
docs/operations/eco-operational-panel-index.md
docs/operations/eco-stable-admission-dry-run-review.md
docs/operations/eco-stable-admission-plan-review.md
docs/operations/eco-stable-admission-plan.md
docs/operations/eco-synthetic-demo-decision-guide.md
docs/operations/eco-synthetic-demos-suite-report-guide.md
docs/operations/eco-synthetic-signal-matrix.md
docs/operations/onboarding-tecnico-30min.md
docs/operations/project-map.md
docs/operations/terminal-stop-guide.md
docs/research/eco-research-index.md
docs/research/eco-vacio-cuantico-patrones-minimos.md
docs/research/eco-vacuum-state-demo-traceability.md
docs/sne-eco-admission-governance-index.md
docs/sne-eco-architecture-map.md
docs/sne-eco-claims-and-limits.md
docs/sne-eco-demo-walkthrough.md
docs/sne-eco-empirical-data-contract.md
docs/sne-eco-empirical-narrative.md
docs/sne-eco-evidence-matrix.md
docs/sne-eco-glossary.md
docs/sne-eco-portfolio-index.md
docs/sne-eco-post-merge-governance-snapshot.md
docs/sne-eco-pr-checklist.md
docs/sne-eco-pr-package.md
docs/sne-eco-public-summary.md
docs/sne-eco-quick-evaluation.md
docs/sne-eco-sensitive-data-governance.md
docs/sne-eco-stable-scenario-admission-plan.md
docs/sne-eco-v1-next-steps.md
docs/sne-eco-v1-portfolio-summary.md
docs/sne-eco-v1-public-summaries.md
docs/sne-eco-v1-release-candidate.md
results/smoke-eco-real-data-activation-rollback-policy-20260508T203852Z.log
results/smoke-eco-real-data-activation-rollback-policy-20260508T203907Z.log
results/smoke-eco-real-data-first-safe-candidate-policy-20260508T203852Z.log
results/smoke-eco-real-data-first-safe-candidate-policy-20260508T203911Z.log
results/smoke-eco-real-data-reactivation-policy-20260508T203907Z.log
scripts/run_eco_absorption_threshold_demo.py
scripts/run_eco_minimal_simulation.py
scripts/run_eco_operational_state_examples_report.py
scripts/run_eco_signal_balance_demo.py
scripts/run_eco_status.py
scripts/run_eco_synthetic_demo_comparison_report.py
scripts/run_eco_synthetic_demos_suite_report.py
scripts/run_eco_synthetic_operational_dashboard.py
scripts/run_eco_synthetic_signal_matrix_report.py
scripts/run_eco_vacuum_state_demo.py
scripts/run_eco_waste_pressure_demo.py
scripts/run_smoke_eco_real_data_activation_rollback_policy.sh
scripts/run_smoke_eco_real_data_first_safe_candidate_policy.sh
scripts/run_smoke_eco_real_data_reactivation_policy.sh
scripts/run_sne_eco_admission_governance_command.py
scripts/run_sne_eco_compare_against_rc1.py
scripts/run_sne_eco_empirical_seed_report.py
scripts/run_sne_eco_empirical_train_eval_split.py
scripts/run_sne_eco_external_evidence_policy.py
scripts/run_sne_eco_external_evidence_review.py
scripts/run_sne_eco_external_scenario_probe.py
scripts/run_sne_eco_governed_ml_evaluation_gate.py
scripts/run_sne_eco_integration_readiness_report.py
scripts/run_sne_eco_ml_baseline.py
scripts/run_sne_eco_ml_challenge_eval.py
scripts/run_sne_eco_neurogastro_context_report.py
scripts/run_sne_eco_neurogastro_pipeline_summary.py
scripts/run_sne_eco_observability_dashboard.py
scripts/run_sne_eco_portfolio_check.py
scripts/run_sne_eco_pr_package_check.py
scripts/run_sne_eco_recurrence_audit.py
scripts/run_sne_eco_responsible_experiment_manifest.py
scripts/run_sne_eco_sensitive_governance_summary.py
scripts/run_sne_eco_sensitive_intake_gate.py
scripts/run_sne_eco_sensitive_source_registry.py
scripts/run_sne_eco_stable_admission_dry_run.py
scripts/run_sne_eco_stable_admission_plan.py
scripts/run_sne_eco_state_baseline.py
scripts/run_sne_eco_state_confusion.py
scripts/run_sne_eco_state_coverage.py
scripts/run_sne_eco_state_dataset.py
scripts/run_sne_eco_state_holdout.py
scripts/run_sne_eco_training_readiness.py
scripts/validate_eco_operational_state_examples.py
scripts/validate_eco_real_data_source_manifest.py
scripts/validate_eco_synthetic_contract.py
scripts/validate_eco_synthetic_demos.py
src/eco_core/__init__.py
src/eco_core/adaptive_state_baseline.py
src/eco_core/adaptive_state_confusion.py
src/eco_core/adaptive_state_coverage.py
src/eco_core/adaptive_state_dataset.py
src/eco_core/adaptive_state_evaluation.py
tests/test_adaptive_state_baseline.py
tests/test_adaptive_state_confusion.py
tests/test_adaptive_state_coverage.py
tests/test_adaptive_state_evaluation.py
tests/test_adaptive_state_extended_scenarios.py
tests/test_eco_absorption_threshold_demo.py
tests/test_eco_adaptive_state_baseline_v0_review.py
tests/test_eco_adaptive_state_foundation.py
tests/test_eco_adaptive_state_foundation_review.py
tests/test_eco_add_synthetic_demo_guide.py
tests/test_eco_admission_review_template.py
tests/test_eco_architecture_index.py
tests/test_eco_baseline_change_review_checklist.py
tests/test_eco_branch_decision_matrix.py
tests/test_eco_branch_rescue_index.py
tests/test_eco_check_clean_command.py
tests/test_eco_check_command.py
tests/test_eco_check_command_links.py
tests/test_eco_check_workflow.py
tests/test_eco_clean_results_command.py
tests/test_eco_external_evidence_checklist.py
tests/test_eco_external_evidence_governance_index.py
tests/test_eco_external_evidence_policy.py
tests/test_eco_external_evidence_policy_review.py
tests/test_eco_external_evidence_register.py
tests/test_eco_external_evidence_register_example.py
tests/test_eco_external_evidence_review_branch.py
tests/test_eco_external_evidence_review_guide.py
tests/test_eco_external_scenario_expansion_review.py
tests/test_eco_external_scenario_matrix.py
tests/test_eco_governance_evidence_review.py
tests/test_eco_makefile_operational_report.py
tests/test_eco_makefile_operational_validator.py
tests/test_eco_makefile_real_data_source_manifest_validator.py
tests/test_eco_minimal_simulation_demo.py
tests/test_eco_operational_block_bitacora.py
tests/test_eco_operational_panel_index.py
tests/test_eco_operational_state_example.py
tests/test_eco_operational_state_examples_report.py
tests/test_eco_operational_state_schema.py
tests/test_eco_operational_state_validator.py
tests/test_eco_real_data_activation_rollback_policy.py
tests/test_eco_real_data_candidate_decision_record.py
tests/test_eco_real_data_candidate_example_decision_record.py
tests/test_eco_real_data_candidate_lifecycle.py
tests/test_eco_real_data_candidate_manifest_example.py
tests/test_eco_real_data_candidate_manifest_template.py
tests/test_eco_real_data_candidate_review_checklist.py
tests/test_eco_real_data_first_safe_candidate_policy.py
tests/test_eco_real_data_interpretation_boundary.py
tests/test_eco_real_data_manifest_activation_gate.py
tests/test_eco_real_data_reactivation_policy.py
tests/test_eco_real_data_readiness_gate.py
tests/test_eco_real_data_source_manifest.py
tests/test_eco_real_data_source_manifest_validator.py
tests/test_eco_registry_driven_validator.py
tests/test_eco_research_index.py
tests/test_eco_signal_balance_demo.py
tests/test_eco_simulation_scope.py
tests/test_eco_stable_admission_dry_run_review.py
tests/test_eco_stable_admission_plan.py
tests/test_eco_stable_admission_plan_review.py
tests/test_eco_status_command.py
tests/test_eco_synthetic_contract_validator.py
tests/test_eco_synthetic_data_contract.py
tests/test_eco_synthetic_demo_comparison.py
tests/test_eco_synthetic_demo_comparison_registry_sync.py
tests/test_eco_synthetic_demo_comparison_report.py
tests/test_eco_synthetic_demo_decision_guide.py
tests/test_eco_synthetic_demo_registry.py
tests/test_eco_synthetic_demos_index.py
tests/test_eco_synthetic_demos_suite_report.py
tests/test_eco_synthetic_demos_suite_report_guide.py
tests/test_eco_synthetic_demos_suite_report_links.py
tests/test_eco_synthetic_demos_validator.py
tests/test_eco_synthetic_operational_dashboard.py
tests/test_eco_synthetic_signal_matrix.py
tests/test_eco_synthetic_signal_matrix_report.py
tests/test_eco_vacio_cuantico_patrones_minimos.py
tests/test_eco_vacuum_state_demo.py
tests/test_eco_vacuum_state_make_target.py
tests/test_eco_vacuum_state_traceability.py
tests/test_eco_waste_pressure_demo.py
tests/test_makefile_adaptive_baseline_target.py
tests/test_makefile_confusion_target.py
tests/test_makefile_coverage_target.py
tests/test_makefile_holdout_target.py
tests/test_project_map.py
tests/test_readme_operations_link.py
tests/test_readme_project_map_link.py
tests/test_readme_synthetic_contract_link.py
tests/test_run_sne_eco_extended_scenarios.py
tests/test_run_sne_eco_state_baseline.py
tests/test_run_sne_eco_state_confusion.py
tests/test_run_sne_eco_state_coverage.py
tests/test_run_sne_eco_state_holdout.py
tests/test_sne_eco_admission_governance_command.py
tests/test_sne_eco_admission_governance_index.py
tests/test_sne_eco_admission_governance_make_target.py
tests/test_sne_eco_architecture_map.py
tests/test_sne_eco_claims_and_limits.py
tests/test_sne_eco_compare_against_rc1.py
tests/test_sne_eco_demo_walkthrough.py
tests/test_sne_eco_empirical_seed_dataset.py
tests/test_sne_eco_empirical_seed_report.py
tests/test_sne_eco_empirical_train_eval_split.py
tests/test_sne_eco_evidence_matrix.py
tests/test_sne_eco_external_evidence_policy.py
tests/test_sne_eco_external_evidence_review.py
tests/test_sne_eco_external_scenario_probe.py
tests/test_sne_eco_glossary.py
tests/test_sne_eco_governed_ml_evaluation_gate.py
tests/test_sne_eco_integration_readiness_report.py
tests/test_sne_eco_ml_baseline.py
tests/test_sne_eco_ml_challenge_eval.py
tests/test_sne_eco_ml_challenge_eval_cli.py
tests/test_sne_eco_neurogastro_context_report.py
tests/test_sne_eco_neurogastro_pipeline_summary.py
tests/test_sne_eco_observability_dashboard.py
tests/test_sne_eco_portfolio_check.py
tests/test_sne_eco_post_merge_governance_snapshot.py
tests/test_sne_eco_pr_package_check.py
tests/test_sne_eco_public_summary_portfolio_check.py
tests/test_sne_eco_quick_evaluation.py
tests/test_sne_eco_readme_admission_governance.py
tests/test_sne_eco_responsible_experiment_manifest.py
tests/test_sne_eco_sensitive_data_governance.py
tests/test_sne_eco_sensitive_governance_summary.py
tests/test_sne_eco_sensitive_intake_gate.py
tests/test_sne_eco_sensitive_source_registry.py
tests/test_sne_eco_stability_suite.py
tests/test_sne_eco_stable_admission_dry_run.py
tests/test_sne_eco_stable_admission_plan.py
tests/test_sne_eco_training_readiness.py
tests/test_synthetic_demo_registry_links.py
tests/test_synthetic_demos_index_links.py
tests/test_synthetic_demos_validator_documentation.py
tests/test_terminal_stop_guide.py
tests/test_terminal_stop_guide_status_link.py
```

## Diff stat

```text
.github/workflows/ci.yml                           |  31 -
 .github/workflows/eco-check.yml                    |  29 -
 CHANGELOG.md                                       |  49 --
 Makefile                                           | 373 +---------
 README.md                                          | 758 ++++++++++-----------
 .../sne_eco_sensitive_intake_candidates.jsonl      |  10 -
 .../sne_eco_sensitive_source_registry.jsonl        |  12 -
 .../sne_eco_empirical_challenge_eval.jsonl         |   8 -
 data/training/sne_eco_empirical_seed_dataset.jsonl |  24 -
 docs/architecture/README.md                        |  37 -
 docs/architecture/eco-adaptive-state-foundation.md |  93 ---
 docs/architecture/eco-minimal-simulation-demo.md   |  28 -
 .../eco-operational-block-bitacora-131-136.md      |  53 --
 .../eco-operational-state-example-dashboard.json   |  28 -
 docs/architecture/eco-operational-state-example.md |  23 -
 .../architecture/eco-operational-state-schema.json |  58 --
 docs/architecture/eco-operational-state-schema.md  |  22 -
 .../eco-operational-state-validator.md             |  21 -
 .../eco-real-data-activation-rollback-policy.md    |  74 --
 .../eco-real-data-candidate-decision-record.md     |  75 --
 ...-real-data-candidate-example-decision-record.md |  55 --
 .../eco-real-data-candidate-lifecycle.md           |  99 ---
 .../eco-real-data-candidate-manifest-example.md    |  60 --
 .../eco-real-data-candidate-manifest-template.md   |  94 ---
 .../eco-real-data-candidate-review-checklist.md    |  80 ---
 .../eco-real-data-first-safe-candidate-policy.md   |  77 ---
 .../eco-real-data-interpretation-boundary.md       |  53 --
 .../eco-real-data-manifest-activation-gate.md      |  68 --
 .../eco-real-data-reactivation-policy.md           |  74 --
 docs/architecture/eco-real-data-readiness-gate.md  |  43 --
 .../eco-real-data-source-manifest-schema.json      |  47 --
 .../eco-real-data-source-manifest-validator.md     |  25 -
 docs/architecture/eco-real-data-source-manifest.md |  35 -
 docs/architecture/eco-simulation-scope.md          |  40 --
 docs/architecture/eco-synthetic-data-contract.md   |  75 --
 docs/architecture/eco-synthetic-demo-comparison.md |  52 --
 docs/architecture/eco-synthetic-demo-registry.json |  39 --
 docs/architecture/eco-synthetic-demo-registry.md   |  67 --
 docs/architecture/eco-synthetic-demos-index.md     |  80 ---
 .../eco-synthetic-operational-dashboard.md         |  30 -
 docs/architecture/eco-synthetic-signal-matrix.json |  44 --
 docs/architecture/eco-synthetic-state-timeline.md  |  27 -
 docs/case-study-sne-eco-neurogastro-pipeline.md    | 118 ----
 docs/eco-agent-operational-context.md              | 172 -----
 docs/guia-baseline-adaptativo-eco.md               |  38 --
 docs/guia-diagnostico-cobertura-eco.md             |  42 --
 docs/guia-escenarios-sinteticos-extendidos-eco.md  |  48 --
 docs/guia-evaluacion-holdout-eco.md                |  50 --
 docs/guia-rutas-confundidas-eco.md                 |  44 --
 .../eco-adaptive-state-baseline-v0-review.md       | 471 -------------
 .../eco-adaptive-state-foundation-review.md        | 170 -----
 docs/operations/eco-add-synthetic-demo-guide.md    |  49 --
 docs/operations/eco-admission-review-template.md   |  62 --
 .../eco-baseline-change-review-checklist.md        |  97 ---
 docs/operations/eco-branch-decision-matrix.md      | 194 ------
 docs/operations/eco-branch-rescue-index.md         | 113 ---
 docs/operations/eco-external-evidence-checklist.md |  87 ---
 .../eco-external-evidence-governance-index.md      |  88 ---
 .../eco-external-evidence-policy-review.md         | 174 -----
 docs/operations/eco-external-evidence-policy.md    | 102 ---
 .../eco-external-evidence-register-example.md      |  83 ---
 docs/operations/eco-external-evidence-register.md  | 107 ---
 .../eco-external-evidence-review-branch.md         | 426 ------------
 .../eco-external-evidence-review-guide.md          | 133 ----
 .../eco-external-scenario-expansion-review.md      | 356 ----------
 docs/operations/eco-external-scenario-matrix.md    | 119 ----
 docs/operations/eco-governance-evidence-review.md  |  61 --
 docs/operations/eco-operational-panel-index.md     | 107 ---
 .../eco-stable-admission-dry-run-review.md         | 174 -----
 .../operations/eco-stable-admission-plan-review.md |  85 ---
 docs/operations/eco-stable-admission-plan.md       | 110 ---
 .../eco-synthetic-demo-decision-guide.md           |  31 -
 .../eco-synthetic-demos-suite-report-guide.md      |  75 --
 docs/operations/eco-synthetic-signal-matrix.md     |  19 -
 docs/operations/onboarding-tecnico-30min.md        |  80 ---
 docs/operations/project-map.md                     |  91 ---
 docs/operations/terminal-stop-guide.md             |  66 --
 docs/research/eco-research-index.md                |  30 -
 .../eco-vacio-cuantico-patrones-minimos.md         |  56 --
 .../research/eco-vacuum-state-demo-traceability.md |  54 --
 docs/sne-eco-admission-governance-index.md         |  99 ---
 docs/sne-eco-architecture-map.md                   |  36 -
 docs/sne-eco-claims-and-limits.md                  |  39 --
 docs/sne-eco-demo-walkthrough.md                   |  66 --
 docs/sne-eco-empirical-data-contract.md            |  41 --
 docs/sne-eco-empirical-narrative.md                | 221 ------
 docs/sne-eco-evidence-matrix.md                    |  36 -
 docs/sne-eco-glossary.md                           |  39 --
 docs/sne-eco-portfolio-index.md                    | 130 ----
 docs/sne-eco-post-merge-governance-snapshot.md     |  45 --
 docs/sne-eco-pr-checklist.md                       |  65 --
 docs/sne-eco-pr-package.md                         |  64 --
 docs/sne-eco-public-summary.md                     |  46 --
 docs/sne-eco-quick-evaluation.md                   |  38 --
 docs/sne-eco-sensitive-data-governance.md          |  47 --
 docs/sne-eco-stable-scenario-admission-plan.md     |  93 ---
 docs/sne-eco-v1-next-steps.md                      | 122 ----
 docs/sne-eco-v1-portfolio-summary.md               |  97 ---
 docs/sne-eco-v1-public-summaries.md                |  40 --
 docs/sne-eco-v1-release-candidate.md               |  92 ---
 ...activation-rollback-policy-20260508T203852Z.log |   7 -
 ...activation-rollback-policy-20260508T203907Z.log |   7 -
 ...irst-safe-candidate-policy-20260508T203852Z.log |   7 -
 ...irst-safe-candidate-policy-20260508T203911Z.log |   7 -
 ...l-data-reactivation-policy-20260508T203907Z.log |   7 -
 scripts/run_eco_absorption_threshold_demo.py       |  78 ---
 scripts/run_eco_minimal_simulation.py              |  90 ---
 .../run_eco_operational_state_examples_report.py   |  68 --
 scripts/run_eco_signal_balance_demo.py             |  93 ---
 scripts/run_eco_status.py                          |  60 --
 .../run_eco_synthetic_demo_comparison_report.py    |  82 ---
 scripts/run_eco_synthetic_demos_suite_report.py    |  97 ---
 scripts/run_eco_synthetic_operational_dashboard.py | 100 ---
 scripts/run_eco_synthetic_signal_matrix_report.py  |  56 --
 scripts/run_eco_vacuum_state_demo.py               | 137 ----
 scripts/run_eco_waste_pressure_demo.py             |  75 --
 ...oke_eco_real_data_activation_rollback_policy.sh |  39 --
 ...ke_eco_real_data_first_safe_candidate_policy.sh |  39 --
 .../run_smoke_eco_real_data_reactivation_policy.sh |  39 --
 .../run_sne_eco_admission_governance_command.py    | 246 -------
 scripts/run_sne_eco_compare_against_rc1.py         | 197 ------
 scripts/run_sne_eco_empirical_seed_report.py       | 224 ------
 scripts/run_sne_eco_empirical_train_eval_split.py  | 307 ---------
 scripts/run_sne_eco_external_evidence_policy.py    | 236 -------
 scripts/run_sne_eco_external_evidence_review.py    | 216 ------
 scripts/run_sne_eco_external_scenario_probe.py     | 190 ------
 scripts/run_sne_eco_governed_ml_evaluation_gate.py | 199 ------
 .../run_sne_eco_integration_readiness_report.py    | 253 -------
 scripts/run_sne_eco_ml_baseline.py                 | 271 --------
 scripts/run_sne_eco_ml_challenge_eval.py           | 232 -------
 scripts/run_sne_eco_neurogastro_context_report.py  | 324 ---------
 .../run_sne_eco_neurogastro_pipeline_summary.py    | 177 -----
 scripts/run_sne_eco_observability_dashboard.py     | 161 -----
 scripts/run_sne_eco_portfolio_check.py             | 198 ------
 scripts/run_sne_eco_pr_package_check.py            | 121 ----
 scripts/run_sne_eco_recurrence_audit.py            | 130 ----
 .../run_sne_eco_responsible_experiment_manifest.py | 196 ------
 .../run_sne_eco_sensitive_governance_summary.py    | 181 -----
 scripts/run_sne_eco_sensitive_intake_gate.py       | 239 -------
 scripts/run_sne_eco_sensitive_source_registry.py   | 255 -------
 scripts/run_sne_eco_stable_admission_dry_run.py    | 226 ------
 scripts/run_sne_eco_stable_admission_plan.py       | 244 -------
 scripts/run_sne_eco_state_baseline.py              |  70 --
 scripts/run_sne_eco_state_confusion.py             |  71 --
 scripts/run_sne_eco_state_coverage.py              |  75 --
 scripts/run_sne_eco_state_dataset.py               |  13 +-
 scripts/run_sne_eco_state_holdout.py               |  71 --
 scripts/run_sne_eco_training_readiness.py          | 232 -------
 scripts/validate_eco_operational_state_examples.py |  65 --
 scripts/validate_eco_real_data_source_manifest.py  | 118 ----
 scripts/validate_eco_synthetic_contract.py         | 107 ---
 scripts/validate_eco_synthetic_demos.py            |  89 ---
 src/eco_core/__init__.py                           |  60 --
 src/eco_core/adaptive_state_baseline.py            | 313 ---------
 src/eco_core/adaptive_state_confusion.py           | 178 -----
 src/eco_core/adaptive_state_coverage.py            | 157 -----
 src/eco_core/adaptive_state_dataset.py             |  47 --
 src/eco_core/adaptive_state_evaluation.py          | 159 -----
 tests/test_adaptive_state_baseline.py              |  58 --
 tests/test_adaptive_state_confusion.py             |  43 --
 tests/test_adaptive_state_coverage.py              |  46 --
 tests/test_adaptive_state_evaluation.py            |  59 --
 tests/test_adaptive_state_extended_scenarios.py    |  38 --
 tests/test_eco_absorption_threshold_demo.py        |  42 --
 .../test_eco_adaptive_state_baseline_v0_review.py  |  41 --
 tests/test_eco_adaptive_state_foundation.py        |  39 --
 tests/test_eco_adaptive_state_foundation_review.py |  44 --
 tests/test_eco_add_synthetic_demo_guide.py         |  43 --
 tests/test_eco_admission_review_template.py        |  40 --
 tests/test_eco_architecture_index.py               |  18 -
 tests/test_eco_baseline_change_review_checklist.py |  43 --
 tests/test_eco_branch_decision_matrix.py           |  32 -
 tests/test_eco_branch_rescue_index.py              |  38 --
 tests/test_eco_check_clean_command.py              |  26 -
 tests/test_eco_check_command.py                    |  15 -
 tests/test_eco_check_command_links.py              |  22 -
 tests/test_eco_check_workflow.py                   |  21 -
 tests/test_eco_clean_results_command.py            |  50 --
 tests/test_eco_external_evidence_checklist.py      |  43 --
 .../test_eco_external_evidence_governance_index.py |  44 --
 tests/test_eco_external_evidence_policy.py         |  42 --
 tests/test_eco_external_evidence_policy_review.py  |  40 --
 tests/test_eco_external_evidence_register.py       |  49 --
 .../test_eco_external_evidence_register_example.py |  42 --
 tests/test_eco_external_evidence_review_branch.py  |  41 --
 tests/test_eco_external_evidence_review_guide.py   |  41 --
 .../test_eco_external_scenario_expansion_review.py |  42 --
 tests/test_eco_external_scenario_matrix.py         |  44 --
 tests/test_eco_governance_evidence_review.py       |  48 --
 tests/test_eco_makefile_operational_report.py      |  31 -
 tests/test_eco_makefile_operational_validator.py   |  28 -
 ...makefile_real_data_source_manifest_validator.py |  26 -
 tests/test_eco_minimal_simulation_demo.py          |  41 --
 tests/test_eco_operational_block_bitacora.py       |  17 -
 tests/test_eco_operational_panel_index.py          |  42 --
 tests/test_eco_operational_state_example.py        |  32 -
 .../test_eco_operational_state_examples_report.py  |  28 -
 tests/test_eco_operational_state_schema.py         |  34 -
 tests/test_eco_operational_state_validator.py      |  14 -
 ...est_eco_real_data_activation_rollback_policy.py |  22 -
 ...test_eco_real_data_candidate_decision_record.py |  23 -
 ..._real_data_candidate_example_decision_record.py |  23 -
 tests/test_eco_real_data_candidate_lifecycle.py    |  24 -
 ...est_eco_real_data_candidate_manifest_example.py |  21 -
 ...st_eco_real_data_candidate_manifest_template.py |  25 -
 ...est_eco_real_data_candidate_review_checklist.py |  23 -
 ...st_eco_real_data_first_safe_candidate_policy.py |  21 -
 .../test_eco_real_data_interpretation_boundary.py  |  20 -
 .../test_eco_real_data_manifest_activation_gate.py |  20 -
 tests/test_eco_real_data_reactivation_policy.py    |  22 -
 tests/test_eco_real_data_readiness_gate.py         |  19 -
 tests/test_eco_real_data_source_manifest.py        |  30 -
 ...test_eco_real_data_source_manifest_validator.py |  26 -
 tests/test_eco_registry_driven_validator.py        |  54 --
 tests/test_eco_research_index.py                   |  30 -
 tests/test_eco_signal_balance_demo.py              |  51 --
 tests/test_eco_simulation_scope.py                 |  31 -
 tests/test_eco_stable_admission_dry_run_review.py  |  40 --
 tests/test_eco_stable_admission_plan.py            |  42 --
 tests/test_eco_stable_admission_plan_review.py     |  35 -
 tests/test_eco_status_command.py                   |  27 -
 tests/test_eco_synthetic_contract_validator.py     | 100 ---
 tests/test_eco_synthetic_data_contract.py          |  62 --
 tests/test_eco_synthetic_demo_comparison.py        |  33 -
 ..._eco_synthetic_demo_comparison_registry_sync.py |  33 -
 tests/test_eco_synthetic_demo_comparison_report.py |  57 --
 tests/test_eco_synthetic_demo_decision_guide.py    |  19 -
 tests/test_eco_synthetic_demo_registry.py          |  40 --
 tests/test_eco_synthetic_demos_index.py            |  32 -
 tests/test_eco_synthetic_demos_suite_report.py     |  42 --
 .../test_eco_synthetic_demos_suite_report_guide.py |  33 -
 .../test_eco_synthetic_demos_suite_report_links.py |  30 -
 tests/test_eco_synthetic_demos_validator.py        |  32 -
 tests/test_eco_synthetic_operational_dashboard.py  |  29 -
 tests/test_eco_synthetic_signal_matrix.py          |  32 -
 tests/test_eco_synthetic_signal_matrix_report.py   |  24 -
 tests/test_eco_vacio_cuantico_patrones_minimos.py  |  28 -
 tests/test_eco_vacuum_state_demo.py                |  54 --
 tests/test_eco_vacuum_state_make_target.py         |  44 --
 tests/test_eco_vacuum_state_traceability.py        |  38 --
 tests/test_eco_waste_pressure_demo.py              |  44 --
 tests/test_makefile_adaptive_baseline_target.py    |  15 -
 tests/test_makefile_confusion_target.py            |  15 -
 tests/test_makefile_coverage_target.py             |  15 -
 tests/test_makefile_holdout_target.py              |  15 -
 tests/test_project_map.py                          |  40 --
 tests/test_readme_operations_link.py               |  21 -
 tests/test_readme_project_map_link.py              |  18 -
 tests/test_readme_synthetic_contract_link.py       |  25 -
 tests/test_run_sne_eco_extended_scenarios.py       |  56 --
 tests/test_run_sne_eco_state_baseline.py           |  41 --
 tests/test_run_sne_eco_state_confusion.py          |  38 --
 tests/test_run_sne_eco_state_coverage.py           |  39 --
 tests/test_run_sne_eco_state_holdout.py            |  38 --
 tests/test_sne_eco_admission_governance_command.py |  41 --
 tests/test_sne_eco_admission_governance_index.py   |  23 -
 ...est_sne_eco_admission_governance_make_target.py |   9 -
 tests/test_sne_eco_architecture_map.py             |  21 -
 tests/test_sne_eco_claims_and_limits.py            |  22 -
 tests/test_sne_eco_compare_against_rc1.py          |  55 --
 tests/test_sne_eco_demo_walkthrough.py             |  20 -
 tests/test_sne_eco_empirical_seed_dataset.py       |  45 --
 tests/test_sne_eco_empirical_seed_report.py        |  35 -
 tests/test_sne_eco_empirical_train_eval_split.py   |  52 --
 tests/test_sne_eco_evidence_matrix.py              |  23 -
 tests/test_sne_eco_external_evidence_policy.py     |  83 ---
 tests/test_sne_eco_external_evidence_review.py     | 137 ----
 tests/test_sne_eco_external_scenario_probe.py      |  29 -
 tests/test_sne_eco_glossary.py                     |  24 -
 tests/test_sne_eco_governed_ml_evaluation_gate.py  |  54 --
 tests/test_sne_eco_integration_readiness_report.py |  59 --
 tests/test_sne_eco_ml_baseline.py                  |  53 --
 tests/test_sne_eco_ml_challenge_eval.py            |  53 --
 tests/test_sne_eco_ml_challenge_eval_cli.py        |  23 -
 tests/test_sne_eco_neurogastro_context_report.py   | 120 ----
 tests/test_sne_eco_neurogastro_pipeline_summary.py |  82 ---
 tests/test_sne_eco_observability_dashboard.py      |  80 ---
 tests/test_sne_eco_portfolio_check.py              |  46 --
 .../test_sne_eco_post_merge_governance_snapshot.py |  25 -
 tests/test_sne_eco_pr_package_check.py             |  50 --
 .../test_sne_eco_public_summary_portfolio_check.py |  21 -
 tests/test_sne_eco_quick_evaluation.py             |  21 -
 tests/test_sne_eco_readme_admission_governance.py  |  17 -
 ...test_sne_eco_responsible_experiment_manifest.py |  65 --
 tests/test_sne_eco_sensitive_data_governance.py    |  35 -
 tests/test_sne_eco_sensitive_governance_summary.py |  51 --
 tests/test_sne_eco_sensitive_intake_gate.py        |  50 --
 tests/test_sne_eco_sensitive_source_registry.py    |  68 --
 tests/test_sne_eco_stability_suite.py              |  49 --
 tests/test_sne_eco_stable_admission_dry_run.py     |  57 --
 tests/test_sne_eco_stable_admission_plan.py        |  89 ---
 tests/test_sne_eco_training_readiness.py           |  45 --
 tests/test_synthetic_demo_registry_links.py        |  26 -
 tests/test_synthetic_demos_index_links.py          |  24 -
 ...test_synthetic_demos_validator_documentation.py |  30 -
 tests/test_terminal_stop_guide.py                  |  26 -
 tests/test_terminal_stop_guide_status_link.py      |  24 -
 297 files changed, 349 insertions(+), 21795 deletions(-)
```

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin incorporación de datasets reales;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin integración masiva de ramas antiguas.
