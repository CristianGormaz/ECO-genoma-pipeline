# Matriz de decisión de ramas no mergeadas E.C.O.

## Estado

- Tipo: no destructivo
- No borra ramas
- No modifica archivos del repositorio
- Fuente: `/tmp/eco-branch-audit-review/branches_audit.tsv`

## Resumen

- Ramas clasificadas: 72
- Categorías de decisión: 8

## Conteo por decisión

- REVISAR PRIMERO - gobernanza/evidencia: 10
- REVISAR PRIMERO - sensible por baseline/datos: 18
- REVISAR - rama grande con muchos commits: 1
- REVISAR PRIMERO - validación/release/estabilidad: 12
- RESCATAR - documentación/portfolio: 10
- CONSERVAR - arquitectura bioinspirada: 9
- REVISAR DESPUÉS - baja prioridad: 11
- NO TOCAR - respaldo local: 1

## Detalle priorizado

### REVISAR PRIMERO - gobernanza/evidencia

- `eco-sne-stable-admission-plan` — commits únicos: 21; archivos: 32; familia: E.C.O.-S.N.E. gobernanza / evidencia externa; último: `7f5f14a`
  - último commit: Document SNE ECO stable scenario admission plan
- `eco-sne-stable-admission-dry-run` — commits únicos: 20; archivos: 34; familia: E.C.O.-S.N.E. gobernanza / evidencia externa; último: `ed09886`
  - último commit: Add SNE ECO stable admission dry run
- `eco-sne-external-evidence-policy` — commits únicos: 19; archivos: 29; familia: E.C.O.-S.N.E. gobernanza / evidencia externa; último: `fb7750d`
  - último commit: Add SNE ECO external evidence policy tests
- `eco-sne-external-evidence-review` — commits únicos: 18; archivos: 27; familia: E.C.O.-S.N.E. gobernanza / evidencia externa; último: `bb17397`
  - último commit: Add SNE ECO external evidence review tests
- `eco-sne-external-scenario-expansion` — commits únicos: 17; archivos: 25; familia: E.C.O.-S.N.E. gobernanza / evidencia externa; último: `bfddf51`
  - último commit: Add SNE ECO external scenario probe tests
- `eco-sne-admission-governance-command` — commits únicos: 3; archivos: 2; familia: E.C.O.-S.N.E. gobernanza / evidencia externa; último: `a1e9205`
  - último commit: Align admission governance command test with yellow status
- `eco-sne-readme-admission-governance` — commits únicos: 2; archivos: 2; familia: E.C.O.-S.N.E. gobernanza / evidencia externa; último: `6ba7ba7`
  - último commit: Fix README admission governance wording
- `sne-30-public-demo-governance` — commits únicos: 2; archivos: 2; familia: S.N.E. serie histórica; último: `e31cb97`
  - último commit: Add SNE ECO PR checklist
- `eco-sne-admission-governance-make-target` — commits únicos: 1; archivos: 2; familia: E.C.O.-S.N.E. gobernanza / evidencia externa; último: `391e6dc`
  - último commit: Add SNE ECO admission governance make target
- `sne-36-evidence-matrix` — commits únicos: 1; archivos: 5; familia: S.N.E. serie histórica; último: `c18f779`
  - último commit: Add SNE ECO evidence matrix

### REVISAR PRIMERO - sensible por baseline/datos

- `eco-sne-release-tag-changelog` — commits únicos: 12; archivos: 16; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `1b5ae70`
  - último commit: Add changelog for SNE ECO v1.0 RC1
- `eco-sne-readme-integration` — commits únicos: 11; archivos: 14; familia: E.C.O.-S.N.E. experimento técnico; último: `5ebfe4c`
  - último commit: Restore SNE ECO v1.0 visibility in README
- `eco-sne-recurrence-guard` — commits únicos: 11; archivos: 11; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `8caa0ac`
  - último commit: Accept empty suggested focus in zero-confusion report
- `eco-sne-release-candidate-v1` — commits únicos: 11; archivos: 15; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `b2808ac`
  - último commit: Add SNE ECO v1 release candidate note
- `eco-sne-empirical-narrative` — commits únicos: 9; archivos: 13; familia: E.C.O.-S.N.E. experimento técnico; último: `e8a8100`
  - último commit: Add SNE ECO empirical narrative documentation
- `eco-sne-extended-scenarios-v0` — commits únicos: 8; archivos: 8; familia: E.C.O.-S.N.E. experimento técnico; último: `ecea4f6`
  - último commit: Add guide for extended adaptive scenarios
- `eco-sne-stability-suite` — commits únicos: 8; archivos: 12; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `8ab178e`
  - último commit: Add SNE ECO stability regression suite
- `eco-sne-hierarchical-baseline` — commits únicos: 7; archivos: 8; familia: E.C.O.-S.N.E. experimento técnico; último: `c892e6a`
  - último commit: Update baseline export test for hierarchical model name
- `eco-adaptive-state-baseline-v0` — commits únicos: 6; archivos: 6; familia: E.C.O. estado adaptativo / baseline; último: `3b223ec`
  - último commit: Add adaptive baseline guide
- `eco-sne-confidence-resolution` — commits únicos: 6; archivos: 9; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `8e25fc9`
  - último commit: Update holdout test for hierarchical confidence fallback
- `eco-sne-recurrence-resolution` — commits únicos: 6; archivos: 10; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `b0a615e`
  - último commit: Add SNE ECO recurrence audit script
- `sne-40-portfolio-check-v1-1-report` — commits únicos: 5; archivos: 9; familia: S.N.E. portfolio / documentación pública; último: `19f8bee`
  - último commit: Add v1.1 comparison report to SNE ECO portfolio check
- `sne-39-portfolio-demo-v1-1-gate` — commits únicos: 4; archivos: 7; familia: S.N.E. portfolio / documentación pública; último: `f431b8f`
  - último commit: Add v1.1 comparison gate to SNE ECO portfolio demo
- `sne-38-make-compare-v1-1` — commits únicos: 3; archivos: 6; familia: S.N.E. serie histórica; último: `e5f84e7`
  - último commit: Add Makefile target for SNE ECO v1.1 comparison
- `eco-adaptive-state-foundation` — commits únicos: 2; archivos: 2; familia: E.C.O. estado adaptativo / baseline; último: `40a5d20`
  - último commit: Add test for adaptive state foundation doc
- `eco-operationalize-adaptive-dataset` — commits únicos: 2; archivos: 2; familia: E.C.O. estado adaptativo / baseline; último: `28e4d98`
  - último commit: Add test for adaptive dataset make target
- `eco-sprint-v1-1-command` — commits únicos: 2; archivos: 2; familia: E.C.O. general / experimental; último: `2bbc3d2`
  - último commit: Add test for adaptive baseline make target
- `sne-37-compare-v1-1` — commits únicos: 2; archivos: 4; familia: S.N.E. serie histórica; último: `c4d216a`
  - último commit: Add SNE ECO v1.1 baseline comparison

### REVISAR - rama grande con muchos commits

- `eco-sne-confusion-command` — commits únicos: 31; archivos: 7; familia: E.C.O.-S.N.E. experimento técnico; último: `fe36e8d`
  - último commit: Merge main into neurogastro pipeline branch

### REVISAR PRIMERO - validación/release/estabilidad

- `eco-sne-compare-against-rc1` — commits únicos: 16; archivos: 23; familia: E.C.O.-S.N.E. experimento técnico; último: `8da8ca0`
  - último commit: Add SNE ECO comparison against RC1 tests
- `eco-sne-observability-dashboard` — commits únicos: 15; archivos: 21; familia: E.C.O.-S.N.E. experimento técnico; último: `a6f4a5a`
  - último commit: Add SNE ECO observability dashboard tests
- `eco-sne-portfolio-packaging` — commits únicos: 15; archivos: 19; familia: E.C.O.-S.N.E. experimento técnico; último: `cb3df6b`
  - último commit: Add SNE ECO next steps after RC1
- `eco-sne-coverage-diagnostics-v0` — commits únicos: 6; archivos: 6; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `3b033b6`
  - último commit: Add adaptive coverage diagnostics guide
- `eco-sne-holdout-eval-v0` — commits únicos: 6; archivos: 6; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `f9c683d`
  - último commit: Add holdout evaluation guide
- `eco-sne-validation-script` — commits únicos: 4; archivos: 2; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `5071a64`
  - último commit: Fix SNE validation script import path
- `eco-sne-directed-variants` — commits únicos: 3; archivos: 4; familia: E.C.O.-S.N.E. experimento técnico; último: `9a5733a`
  - último commit: Add directed SNE ECO variants and align coverage expectation
- `eco-sne-validation-artifacts` — commits únicos: 3; archivos: 3; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `600a76b`
  - último commit: Add Makefile target for SNE-ECO validation artifacts
- `eco-sne-coverage-command` — commits únicos: 2; archivos: 2; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `3f795ed`
  - último commit: Add test for adaptive coverage make target
- `eco-sne-holdout-command` — commits únicos: 2; archivos: 2; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `ebf8d69`
  - último commit: Add test for adaptive holdout make target
- `eco-sne-roadmap-v1-1-clean` — commits únicos: 2; archivos: 2; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `4de2c50`
  - último commit: Add test for SNE-ECO v1.1 roadmap
- `eco-sne-validation-ux` — commits únicos: 1; archivos: 1; familia: E.C.O.-S.N.E. validación / release / estabilidad; último: `019ef68`
  - último commit: Add SNE-ECO validation UX guide

### RESCATAR - documentación/portfolio

- `eco-defense-layer` — commits únicos: 4; archivos: 4; familia: E.C.O. arquitectura entérica / bioinspirada; último: `2344779`
  - último commit: Add public API test for defense helpers
- `eco-gut-brain-report` — commits únicos: 4; archivos: 4; familia: E.C.O. arquitectura entérica / bioinspirada; último: `3afed22`
  - último commit: Add public API test for gut-brain report
- `eco-microbiota-memory` — commits únicos: 4; archivos: 4; familia: E.C.O. arquitectura entérica / bioinspirada; último: `34c4927`
  - último commit: Add public API test for microbiota helpers
- `sne-23-portfolio-case-study` — commits únicos: 1; archivos: 1; familia: S.N.E. portfolio / documentación pública; último: `7bdad9c`
  - último commit: Add SNE ECO neurogastro pipeline case study
- `sne-24-portfolio-index` — commits únicos: 1; archivos: 1; familia: S.N.E. portfolio / documentación pública; último: `844d5a5`
  - último commit: Add SNE ECO portfolio index
- `sne-25-readme-portfolio-entry` — commits únicos: 1; archivos: 1; familia: S.N.E. portfolio / documentación pública; último: `72cb57e`
  - último commit: Add portfolio entry to README
- `sne-27-portfolio-check-target` — commits únicos: 1; archivos: 1; familia: S.N.E. portfolio / documentación pública; último: `b22241d`
  - último commit: Add portfolio check Makefile target
- `sne-28-portfolio-demo-target` — commits únicos: 1; archivos: 1; familia: S.N.E. portfolio / documentación pública; último: `90ddefe`
  - último commit: Add portfolio demo Makefile target
- `sne-31-public-summary` — commits únicos: 1; archivos: 4; familia: S.N.E. serie histórica; último: `1a95611`
  - último commit: Add SNE ECO public summary
- `sne-32-public-summary-portfolio-check` — commits únicos: 1; archivos: 5; familia: S.N.E. portfolio / documentación pública; último: `c7ac687`
  - último commit: Add public summary to portfolio check

### CONSERVAR - arquitectura bioinspirada

- `sne-eco-enteric-module` — commits únicos: 5; archivos: 4; familia: E.C.O. arquitectura entérica / bioinspirada; último: `9c122f4`
  - último commit: Merge remote-tracking branch 'origin/main' into sne-eco-enteric-module
- `eco-submucosal-sensing` — commits únicos: 4; archivos: 3; familia: E.C.O. arquitectura entérica / bioinspirada; último: `1a98e89`
  - último commit: Make invalid character sensor test case-insensitive
- `eco-homeostasis-layer` — commits únicos: 3; archivos: 3; familia: E.C.O. arquitectura entérica / bioinspirada; último: `d8c2b95`
  - último commit: Export enteric homeostasis helpers
- `eco-integrate-enteric-organs` — commits únicos: 3; archivos: 3; familia: E.C.O. integración bioinspirada; último: `58cdb79`
  - último commit: Add tests for integrated enteric orchestrator
- `eco-myenteric-motility` — commits únicos: 3; archivos: 3; familia: E.C.O. arquitectura entérica / bioinspirada; último: `760fea9`
  - último commit: Export myenteric motility helpers
- `eco-integrate-defense-signal` — commits únicos: 2; archivos: 2; familia: E.C.O. integración bioinspirada; último: `f568731`
  - último commit: Add tests for defense signal integration
- `eco-integrate-gut-brain-report` — commits únicos: 2; archivos: 2; familia: E.C.O. integración bioinspirada; último: `b98fc9f`
  - último commit: Add tests for gut-brain report integration
- `eco-integrate-myenteric-motility` — commits únicos: 2; archivos: 2; familia: E.C.O. integración bioinspirada; último: `776e593`
  - último commit: Add tests for myenteric motility integration
- `eco-enteric-modularization` — commits únicos: 1; archivos: 2; familia: E.C.O. arquitectura entérica / bioinspirada; último: `18225f5`
  - último commit: Add enteric barrier module

### REVISAR DESPUÉS - baja prioridad

- `eco-sprint-v1-1-data-rows` — commits únicos: 7; archivos: 6; familia: E.C.O. general / experimental; último: `cf94cb0`
  - último commit: Relax defense severity expectation in adaptive dataset test
- `eco-sne-confused-routes-v0` — commits únicos: 6; archivos: 6; familia: E.C.O.-S.N.E. experimento técnico; último: `3cc6723`
  - último commit: Add confused routes guide
- `eco-sne-v1-1-packet-trace` — commits únicos: 6; archivos: 6; familia: E.C.O.-S.N.E. experimento técnico; último: `f8ac54b`
  - último commit: Add SNE-ECO packet trace guide
- `eco-sne-v1-index-demo` — commits únicos: 4; archivos: 3; familia: E.C.O.-S.N.E. experimento técnico; último: `f18eac5`
  - último commit: Align SNE v1 index ethical wording with tests
- `eco-readme-sne-v1-visibility` — commits únicos: 2; archivos: 2; familia: E.C.O. general / experimental; último: `c4105c5`
  - último commit: Add README visibility test for SNE-ECO v1
- `sne-26-final-check` — commits únicos: 2; archivos: 2; familia: S.N.E. serie histórica; último: `f45825a`
  - último commit: Add tests for SNE ECO portfolio check
- `sne-29-demo-walkthrough` — commits únicos: 1; archivos: 3; familia: S.N.E. serie histórica; último: `27d17b3`
  - último commit: Add SNE ECO demo walkthrough
- `sne-33-quick-evaluation-guide` — commits únicos: 1; archivos: 5; familia: S.N.E. serie histórica; último: `4efd34a`
  - último commit: Add quick evaluation guide
- `sne-34-architecture-map` — commits únicos: 1; archivos: 5; familia: S.N.E. serie histórica; último: `fddec26`
  - último commit: Add SNE ECO architecture map
- `sne-35-glossary` — commits únicos: 1; archivos: 5; familia: S.N.E. serie histórica; último: `175f717`
  - último commit: Add SNE ECO glossary
- `sne-37-claims-and-limits` — commits únicos: 1; archivos: 5; familia: S.N.E. serie histórica; último: `7c23fc5`
  - último commit: Add SNE ECO claims and limits matrix

### NO TOCAR - respaldo local

- `backup-main-10d3141-20260506-204140` — commits únicos: 1; archivos: 1; familia: backup / respaldo local; último: `10d3141`
  - último commit: feat: add ECO synthetic signal matrix report
