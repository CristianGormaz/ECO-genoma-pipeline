# Revisión de rama: eco-sne-external-scenario-expansion

Este documento resume la inspección segura de la rama antigua `eco-sne-external-scenario-expansion`.

## Objetivo

Identificar si existe una pieza rescatable relacionada con expansión de escenarios externos sin integrar cambios antiguos en bloque.

## Estado de la revisión

- Tipo de sprint: documental / auditoría.
- Clasificación: permitido.
- Acción realizada: inspección de commits, archivos y diff contra `main`.
- Ref usada: `eco-sne-external-scenario-expansion`.
- No se hizo merge.
- No se hizo cherry-pick.
- No se borraron ramas.
- No se modificó baseline.
- No se recalibraron umbrales.
- No se incorporó evidencia externa automáticamente.

## Lectura operativa

La rama parece asociada a una expansión de escenarios externos. Debe tratarse como fuente de ideas y trazabilidad, no como paquete listo para integrar.

Una expansión de escenarios externos puede ser útil si ayuda a describir casos de revisión, límites o clasificación de evidencia, pero no debe convertir fuentes externas en datos entrenables ni en conclusiones aplicadas.

## Riesgo detectado

La rama no debe integrarse completa. Las ramas antiguas de esta familia suelen mezclar documentación, scripts, tests, Makefile, CI, datos o resultados generados.

El riesgo principal es retroceder el estado actual de `main` o introducir piezas que no respeten la política de evidencia externa ya estabilizada.

## Áreas sensibles

No rescatar sin revisión separada:

- cambios de CI;
- cambios grandes en Makefile;
- scripts de evaluación o entrenamiento;
- datos en `data/`;
- resultados generados en `results/`;
- modificaciones de baseline;
- cambios de umbrales;
- evidencia externa sin registro, checklist y límites explícitos.

## Piezas potencialmente rescatables

Rescatar solo en PRs pequeños:

1. Matriz o listado de escenarios externos sintéticos.
2. Checklist para clasificar escenarios externos.
3. Glosario de tipos de escenario externo.
4. Ejemplo documental sin datos reales.
5. Test documental que valide límites responsables.

## Decisión recomendada

No integrar la rama `eco-sne-external-scenario-expansion` como bloque.

El siguiente sprint lógico, si esta revisión queda integrada, sería rescatar una sola pieza documental: una guía o matriz de escenarios externos sintéticos, alineada con la política, checklist, registro y guía de evidencia externa ya existentes.

## Commits inspeccionados

```text
bfddf51 Add SNE ECO external scenario probe tests
e821d72 Add SNE ECO external scenario probe
f7a71dc SNE-15 compare against RC1 (#52)
823c534 SNE-14 observability dashboard (#51)
3a3e5f4 SNE-13 portfolio packaging after RC1 (#50)
2524b8d Add changelog for SNE ECO v1.0 RC1 (#49)
4bc3bf3 Add SNE ECO v1 release candidate note (#48)
471cc60 SNE-10 README integration and reproducible commands (#47)
25d99ff Add SNE ECO empirical narrative documentation (#46)
c845f8c Add SNE ECO stability regression suite (#45)
00e05f7 Merge SNE-07 recurrence guard
6616238 Add SNE ECO recurrence audit script (#43)
791510d Merge SNE-05 confidence resolution
065d049 Sprint SNE-04: hierarchical baseline fallback (#41)
bbc8d2b Merge Sprint SNE-03 directed variants
dc77907 Add test for confused route make target
48dfd53 Add make target for confused route analysis
```

## Archivos inspeccionados

```text
.github/workflows/ci.yml
.github/workflows/eco-check.yml
Makefile
README.md
data/governance/sne_eco_sensitive_intake_candidates.jsonl
data/governance/sne_eco_sensitive_source_registry.jsonl
data/training/sne_eco_empirical_challenge_eval.jsonl
data/training/sne_eco_empirical_seed_dataset.jsonl
docs/architecture/README.md
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
docs/operations/eco-add-synthetic-demo-guide.md
docs/operations/eco-admission-review-template.md
docs/operations/eco-branch-decision-matrix.md
docs/operations/eco-branch-rescue-index.md
docs/operations/eco-external-evidence-checklist.md
docs/operations/eco-external-evidence-policy-review.md
docs/operations/eco-external-evidence-policy.md
docs/operations/eco-external-evidence-register-example.md
docs/operations/eco-external-evidence-register.md
docs/operations/eco-external-evidence-review-branch.md
docs/operations/eco-external-evidence-review-guide.md
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
scripts/run_sne_eco_governed_ml_evaluation_gate.py
scripts/run_sne_eco_integration_readiness_report.py
scripts/run_sne_eco_ml_baseline.py
scripts/run_sne_eco_ml_challenge_eval.py
scripts/run_sne_eco_neurogastro_context_report.py
scripts/run_sne_eco_neurogastro_pipeline_summary.py
scripts/run_sne_eco_portfolio_check.py
scripts/run_sne_eco_pr_package_check.py
scripts/run_sne_eco_responsible_experiment_manifest.py
scripts/run_sne_eco_sensitive_governance_summary.py
scripts/run_sne_eco_sensitive_intake_gate.py
scripts/run_sne_eco_sensitive_source_registry.py
scripts/run_sne_eco_stable_admission_dry_run.py

... salida truncada: 120 líneas adicionales ...
```

## Diff stat inspeccionado

```text
.github/workflows/ci.yml                           |  31 --
 .github/workflows/eco-check.yml                    |  29 --
 Makefile                                           | 304 +--------------
 README.md                                          | 197 ----------
 .../sne_eco_sensitive_intake_candidates.jsonl      |  10 -
 .../sne_eco_sensitive_source_registry.jsonl        |  12 -
 .../sne_eco_empirical_challenge_eval.jsonl         |   8 -
 data/training/sne_eco_empirical_seed_dataset.jsonl |  24 --
 docs/architecture/README.md                        |  37 --
 docs/architecture/eco-minimal-simulation-demo.md   |  28 --
 .../eco-operational-block-bitacora-131-136.md      |  53 ---
 .../eco-operational-state-example-dashboard.json   |  28 --
 docs/architecture/eco-operational-state-example.md |  23 --
 .../architecture/eco-operational-state-schema.json |  58 ---
 docs/architecture/eco-operational-state-schema.md  |  22 --
 .../eco-operational-state-validator.md             |  21 -
 .../eco-real-data-activation-rollback-policy.md    |  74 ----
 .../eco-real-data-candidate-decision-record.md     |  75 ----
 ...-real-data-candidate-example-decision-record.md |  55 ---
 .../eco-real-data-candidate-lifecycle.md           |  99 -----
 .../eco-real-data-candidate-manifest-example.md    |  60 ---
 .../eco-real-data-candidate-manifest-template.md   |  94 -----
 .../eco-real-data-candidate-review-checklist.md    |  80 ----
 .../eco-real-data-first-safe-candidate-policy.md   |  77 ----
 .../eco-real-data-interpretation-boundary.md       |  53 ---
 .../eco-real-data-manifest-activation-gate.md      |  68 ----
 .../eco-real-data-reactivation-policy.md           |  74 ----
 docs/architecture/eco-real-data-readiness-gate.md  |  43 ---
 .../eco-real-data-source-manifest-schema.json      |  47 ---
 .../eco-real-data-source-manifest-validator.md     |  25 --
 docs/architecture/eco-real-data-source-manifest.md |  35 --
 docs/architecture/eco-simulation-scope.md          |  40 --
 docs/architecture/eco-synthetic-data-contract.md   |  75 ----
 docs/architecture/eco-synthetic-demo-comparison.md |  52 ---
 docs/architecture/eco-synthetic-demo-registry.json |  39 --
 docs/architecture/eco-synthetic-demo-registry.md   |  67 ----
 docs/architecture/eco-synthetic-demos-index.md     |  80 ----
 .../eco-synthetic-operational-dashboard.md         |  30 --
 docs/architecture/eco-synthetic-signal-matrix.json |  44 ---
 docs/architecture/eco-synthetic-state-timeline.md  |  27 --
 docs/case-study-sne-eco-neurogastro-pipeline.md    | 118 ------
 docs/eco-agent-operational-context.md              | 172 ---------
 docs/operations/eco-add-synthetic-demo-guide.md    |  49 ---
 docs/operations/eco-admission-review-template.md   |  62 ---
 docs/operations/eco-branch-decision-matrix.md      | 194 ----------
 docs/operations/eco-branch-rescue-index.md         | 113 ------
 docs/operations/eco-external-evidence-checklist.md |  87 -----
 .../eco-external-evidence-policy-review.md         | 174 ---------
 docs/operations/eco-external-evidence-policy.md    | 102 -----
 .../eco-external-evidence-register-example.md      |  83 ----
 docs/operations/eco-external-evidence-register.md  | 107 ------
 .../eco-external-evidence-review-branch.md         | 426 ---------------------
 .../eco-external-evidence-review-guide.md          | 133 -------
 docs/operations/eco-governance-evidence-review.md  |  61 ---
 docs/operations/eco-operational-panel-index.md     | 107 ------
 .../eco-stable-admission-dry-run-review.md         | 174 ---------
 .../operations/eco-stable-admission-plan-review.md |  85 ----
 docs/operations/eco-stable-admission-plan.md       | 110 ------
 .../eco-synthetic-demo-decision-guide.md           |  31 --
 .../eco-synthetic-demos-suite-report-guide.md      |  75 ----
 docs/operations/eco-synthetic-signal-matrix.md     |  19 -
 docs/operations/onboarding-tecnico-30min.md        |  80 ----
 docs/operations/project-map.md                     |  91 -----
 docs/operations/terminal-stop-guide.md             |  66 ----
 docs/research/eco-research-index.md                |  30 --
 .../eco-vacio-cuantico-patrones-minimos.md         |  56 ---
 .../research/eco-vacuum-state-demo-traceability.md |  54 ---
 docs/sne-eco-admission-governance-index.md         |  99 -----
 docs/sne-eco-architecture-map.md                   |  36 --
 docs/sne-eco-claims-and-limits.md                  |  39 --
 docs/sne-eco-demo-walkthrough.md                   |  66 ----
 docs/sne-eco-empirical-data-contract.md            |  41 --
 docs/sne-eco-evidence-matrix.md                    |  36 --
 docs/sne-eco-glossary.md                           |  39 --
 docs/sne-eco-portfolio-index.md                    | 130 -------
 docs/sne-eco-post-merge-governance-snapshot.md     |  45 ---
 docs/sne-eco-pr-checklist.md                       |  65 ----
 docs/sne-eco-pr-package.md                         |  64 ----
 docs/sne-eco-public-summary.md                     |  46 ---
 docs/sne-eco-quick-evaluation.md                   |  38 --
 docs/sne-eco-sensitive-data-governance.md          |  47 ---
 docs/sne-eco-stable-scenario-admission-plan.md     |  93 -----
 ...activation-rollback-policy-20260508T203852Z.log |   7 -
 ...activation-rollback-policy-20260508T203907Z.log |   7 -
 ...irst-safe-candidate-policy-20260508T203852Z.log |   7 -
 ...irst-safe-candidate-policy-20260508T203911Z.log |   7 -
 ...l-data-reactivation-policy-20260508T203907Z.log |   7 -
 scripts/run_eco_absorption_threshold_demo.py       |  78 ----
 scripts/run_eco_minimal_simulation.py              |  90 -----
 .../run_eco_operational_state_examples_report.py   |  68 ----
 scripts/run_eco_signal_balance_demo.py             |  93 -----
 scripts/run_eco_status.py                          |  60 ---
 .../run_eco_synthetic_demo_comparison_report.py    |  82 ----
 scripts/run_eco_synthetic_demos_suite_report.py    |  97 -----
 scripts/run_eco_synthetic_operational_dashboard.py | 100 -----
 scripts/run_eco_synthetic_signal_matrix_report.py  |  56 ---
 scripts/run_eco_vacuum_state_demo.py               | 137 -------
 scripts/run_eco_waste_pressure_demo.py             |  75 ----
 ...oke_eco_real_data_activation_rollback_policy.sh |  39 --
 ...ke_eco_real_data_first_safe_candidate_policy.sh |  39 --
 .../run_smoke_eco_real_data_reactivation_policy.sh |  39 --
 .../run_sne_eco_admission_governance_command.py    | 246 ------------
 scripts/run_sne_eco_compare_against_rc1.py         |  38 +-
 scripts/run_sne_eco_empirical_seed_report.py       | 224 -----------
 scripts/run_sne_eco_empirical_train_eval_split.py  | 307 ---------------
 scripts/run_sne_eco_external_evidence_policy.py    | 236 ------------
 scripts/run_sne_eco_external_evidence_review.py    | 216 -----------
 scripts/run_sne_eco_governed_ml_evaluation_gate.py | 199 ----------
 .../run_sne_eco_integration_readiness_report.py    | 253 ------------
 scripts/run_sne_eco_ml_baseline.py                 | 271 -------------
 scripts/run_sne_eco_ml_challenge_eval.py           | 232 -----------
 scripts/run_sne_eco_neurogastro_context_report.py  | 324 ----------------
 .../run_sne_eco_neurogastro_pipeline_summary.py    | 177 ---------
 scripts/run_sne_eco_portfolio_check.py             | 198 ----------
 scripts/run_sne_eco_pr_package_check.py            | 121 ------
 .../run_sne_eco_responsible_experiment_manifest.py | 196 ----------
 .../run_sne_eco_sensitive_governance_summary.py    | 181 ---------
 scripts/run_sne_eco_sensitive_intake_gate.py       | 239 ------------
 scripts/run_sne_eco_sensitive_source_registry.py   | 255 ------------
 scripts/run_sne_eco_stable_admission_dry_run.py    | 226 -----------

... salida truncada: 121 líneas adicionales ...
```

## Comandos seguros usados

```bash
git log --oneline main..eco-sne-external-scenario-expansion
git diff --name-only main..eco-sne-external-scenario-expansion
git diff --stat main..eco-sne-external-scenario-expansion
```

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
