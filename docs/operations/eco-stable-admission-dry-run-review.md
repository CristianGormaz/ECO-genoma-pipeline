# Revisión de rama: eco-sne-stable-admission-dry-run

Este documento aplica la plantilla de revisión de admisión estable a la rama antigua `eco-sne-stable-admission-dry-run`.

## Objetivo

Determinar si el concepto de dry-run de admisión estable puede rescatarse como pieza pequeña, sin integrar cambios antiguos en bloque.

## Identificación de la pieza

- Nombre de la pieza: dry-run de admisión estable S.N.E.-E.C.O.
- Rama origen: `eco-sne-stable-admission-dry-run`.
- Tipo de pieza: documentación operativa / posible script de validación futura.
- Estado propuesto: review_needed.
- Acción realizada: inspección documental de commits, archivos y diff contra `main`.

## Clasificación responsable

- Tipo de sprint: documental / auditoría.
- Clasificación: permitido.
- No se hizo merge.
- No se hizo cherry-pick.
- No se ejecutó entrenamiento.
- No se modificó baseline.
- No se recalibraron umbrales.
- No se incorporó evidencia externa automáticamente.

## Lectura de la rama

- Commits únicos contra `main`: 20.
- Último commit revisado: Add SNE ECO stable admission dry run.
- Archivos cambiados detectados: 215.

## Commits observados

- `ed09886 Add SNE ECO stable admission dry run`
- `7d2989c SNE-19 stable scenario admission plan (#56)`
- `1b32858 SNE-18 external evidence policy (#55)`
- `9ace54f SNE-17 external evidence review (#54)`
- `5dfbacd SNE-16 external scenario expansion probe (#53)`
- `f7a71dc SNE-15 compare against RC1 (#52)`
- `823c534 SNE-14 observability dashboard (#51)`
- `3a3e5f4 SNE-13 portfolio packaging after RC1 (#50)`
- `2524b8d Add changelog for SNE ECO v1.0 RC1 (#49)`
- `4bc3bf3 Add SNE ECO v1 release candidate note (#48)`
- `471cc60 SNE-10 README integration and reproducible commands (#47)`
- `25d99ff Add SNE ECO empirical narrative documentation (#46)`
- `c845f8c Add SNE ECO stability regression suite (#45)`
- `00e05f7 Merge SNE-07 recurrence guard`
- `6616238 Add SNE ECO recurrence audit script (#43)`
- `791510d Merge SNE-05 confidence resolution`
- `065d049 Sprint SNE-04: hierarchical baseline fallback (#41)`
- `bbc8d2b Merge Sprint SNE-03 directed variants`
- `dc77907 Add test for confused route make target`
- `48dfd53 Add make target for confused route analysis`

## Muestra de archivos cambiados

- `.github/workflows/ci.yml`
- `.github/workflows/eco-check.yml`
- `Makefile`
- `README.md`
- `data/governance/sne_eco_sensitive_intake_candidates.jsonl`
- `data/governance/sne_eco_sensitive_source_registry.jsonl`
- `data/training/sne_eco_empirical_challenge_eval.jsonl`
- `data/training/sne_eco_empirical_seed_dataset.jsonl`
- `docs/architecture/README.md`
- `docs/architecture/eco-minimal-simulation-demo.md`
- `docs/architecture/eco-operational-block-bitacora-131-136.md`
- `docs/architecture/eco-operational-state-example-dashboard.json`
- `docs/architecture/eco-operational-state-example.md`
- `docs/architecture/eco-operational-state-schema.json`
- `docs/architecture/eco-operational-state-schema.md`
- `docs/architecture/eco-operational-state-validator.md`
- `docs/architecture/eco-real-data-activation-rollback-policy.md`
- `docs/architecture/eco-real-data-candidate-decision-record.md`
- `docs/architecture/eco-real-data-candidate-example-decision-record.md`
- `docs/architecture/eco-real-data-candidate-lifecycle.md`
- `docs/architecture/eco-real-data-candidate-manifest-example.md`
- `docs/architecture/eco-real-data-candidate-manifest-template.md`
- `docs/architecture/eco-real-data-candidate-review-checklist.md`
- `docs/architecture/eco-real-data-first-safe-candidate-policy.md`
- `docs/architecture/eco-real-data-interpretation-boundary.md`
- `docs/architecture/eco-real-data-manifest-activation-gate.md`
- `docs/architecture/eco-real-data-reactivation-policy.md`
- `docs/architecture/eco-real-data-readiness-gate.md`
- `docs/architecture/eco-real-data-source-manifest-schema.json`
- `docs/architecture/eco-real-data-source-manifest-validator.md`
- `docs/architecture/eco-real-data-source-manifest.md`
- `docs/architecture/eco-simulation-scope.md`
- `docs/architecture/eco-synthetic-data-contract.md`
- `docs/architecture/eco-synthetic-demo-comparison.md`
- `docs/architecture/eco-synthetic-demo-registry.json`
- `docs/architecture/eco-synthetic-demo-registry.md`
- `docs/architecture/eco-synthetic-demos-index.md`
- `docs/architecture/eco-synthetic-operational-dashboard.md`
- `docs/architecture/eco-synthetic-signal-matrix.json`
- `docs/architecture/eco-synthetic-state-timeline.md`

## Resumen de diff

```text
.github/workflows/ci.yml                           |  31 --
 .github/workflows/eco-check.yml                    |  29 --
 Makefile                                           | 264 +----------------
 README.md                                          | 189 ------------
 .../sne_eco_sensitive_intake_candidates.jsonl      |  10 -
 .../sne_eco_sensitive_source_registry.jsonl        |  12 -
 .../sne_eco_empirical_challenge_eval.jsonl         |   8 -
 data/training/sne_eco_empirical_seed_dataset.jsonl |  24 --
 docs/architecture/README.md                        |  37 ---
 docs/architecture/eco-minimal-simulation-demo.md   |  28 --
 .../eco-operational-block-bitacora-131-136.md      |  53 ----
 .../eco-operational-state-example-dashboard.json   |  28 --
 docs/architecture/eco-operational-state-example.md |  23 --
 .../architecture/eco-operational-state-schema.json |  58 ----
 docs/architecture/eco-operational-state-schema.md  |  22 --
 .../eco-operational-state-validator.md             |  21 --
 .../eco-real-data-activation-rollback-policy.md    |  74 -----
 .../eco-real-data-candidate-decision-record.md     |  75 -----
 ...-real-data-candidate-example-decision-record.md |  55 ----
 .../eco-real-data-candidate-lifecycle.md           |  99 -------
 .../eco-real-data-candidate-manifest-example.md    |  60 ----
 .../eco-real-data-candidate-manifest-template.md   |  94 ------
 .../eco-real-data-candidate-review-checklist.md    |  80 -----
 .../eco-real-data-first-safe-candidate-policy.md   |  77 -----
 .../eco-real-data-interpretation-boundary.md       |  53 ----
 .../eco-real-data-manifest-activation-gate.md      |  68 -----
 .../eco-real-data-reactivation-policy.md           |  74 -----
 docs/architecture/eco-real-data-readiness-gate.md  |  43 ---
 .../eco-real-data-source-manifest-schema.json      |  47 ---
 .../eco-real-data-source-manifest-validator.md     |  25 --
 docs/architecture/eco-real-data-source-manifest.md |  35 ---
 docs/architecture/eco-simulation-scope.md          |  40 ---
 docs/architecture/eco-synthetic-data-contract.md   |  75 -----
 docs/architecture/eco-synthetic-demo-comparison.md |  52 ----
 docs/architecture/eco-synthetic-demo-registry.json |  39 ---
```

## Riesgo detectado

La rama no debe integrarse completa. El nombre `dry-run` sugiere una pieza útil para simular admisión sin afectar el sistema, pero el diff contra `main` mezcla documentación, scripts, tests, workflows, datos o piezas históricas.

## Preguntas de admisión

1. ¿El dry-run puede expresarse como documentación antes de script?
2. ¿Puede validarse sin ejecutar modelos ni modificar datos?
3. ¿Puede quedar separado de baseline, entrenamiento y evaluación?
4. ¿Puede funcionar solo como verificación operativa?
5. ¿Evita incorporar evidencia externa automáticamente?
6. ¿Puede rescatarse en un PR pequeño?

## Decisión recomendada

No integrar la rama `eco-sne-stable-admission-dry-run` como bloque.

El siguiente rescate, si se decide continuar, debería ser una pieza documental pequeña: una especificación de dry-run de admisión estable. Solo después convendría evaluar si merece script.

## Piezas potencialmente rescatables

1. Especificación del dry-run.
2. Checklist de ejecución segura.
3. Criterios de salida: passed / attention / blocked.
4. Test documental de límites responsables.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
