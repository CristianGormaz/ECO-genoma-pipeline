# Revisión de rama: eco-adaptive-state-foundation

Este documento resume la inspección segura de la rama antigua `eco-adaptive-state-foundation`.

## Objetivo

Determinar si la rama contiene piezas rescatables relacionadas con estado adaptativo, baseline o fundamentos operativos, sin integrar cambios antiguos en bloque.

## Estado de la revisión

- Tipo de sprint: documental / auditoría.
- Clasificación: permitido.
- Acción realizada: inspección de commits, archivos y diferencia contra `main`.
- Rama inspeccionada: `eco-adaptive-state-foundation`.
- Commits únicos contra `main`: 2.
- Archivos cambiados contra `main`: 297.
- Último commit observado: Add test for adaptive state foundation doc.
- No se hizo merge.
- No se hizo cherry-pick.
- No se modificó baseline.
- No se recalibraron umbrales.
- No se entrenaron modelos.
- No se incorporaron datos sensibles.

## Muestra de commits

```text
40a5d20 Add test for adaptive state foundation doc
4f546b7 Document adaptive state foundation for E.C.O.
```

## Muestra de archivos cambiados

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
docs/guia-dataset-adaptativo-eco.md
docs/guia-diagnostico-cobertura-eco.md
docs/guia-escenarios-sinteticos-extendidos-eco.md
docs/guia-evaluacion-holdout-eco.md
docs/guia-rutas-confundidas-eco.md
docs/operations/eco-adaptive-state-baseline-v0-review.md
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
```

## Lectura operativa

Esta rama pertenece al bloque sensible de baseline, datos y evaluación. Debe tratarse como fuente de ideas, no como paquete listo para integrar.

## Riesgo detectado

No conviene integrar la rama completa. Cualquier contenido relacionado con baseline, datos, evaluación, métricas o umbrales debe pasar por revisión separada y comparación explícita.

## Piezas potencialmente rescatables

Rescatar solo en PRs pequeños y separados:

1. Fundamento documental de estado adaptativo.
2. Glosario operativo de estado, señal, balance o transición.
3. Checklist conceptual si no modifica baseline.
4. Ejemplo sintético si no usa datos reales.
5. Test documental si solo valida límites responsables.

## Piezas bloqueadas sin auditoría

No rescatar directamente:

- datasets;
- cambios de baseline;
- scripts de entrenamiento;
- scripts de evaluación aplicada;
- cambios de umbral;
- resultados generados;
- cambios amplios de CI o Makefile;
- cualquier afirmación biomédica aplicada.

## Decisión recomendada

No integrar `eco-adaptive-state-foundation` como bloque.

El siguiente sprint lógico, si esta revisión queda green, sería rescatar una sola pieza documental: una guía de fundamentos de estado adaptativo E.C.O., alineada con los límites actuales de `main`.

## Comandos seguros de inspección usados

```bash
git log --oneline main..eco-adaptive-state-foundation
git diff --name-only main..eco-adaptive-state-foundation
git diff --stat main..eco-adaptive-state-foundation
```

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin integración masiva de ramas antiguas.
