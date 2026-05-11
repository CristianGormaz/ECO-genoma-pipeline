# Revisión de gobernanza y evidencia externa E.C.O.

Este documento resume la primera familia prioritaria identificada en la matriz de decisión de ramas.

## Objetivo

Revisar ramas asociadas a gobernanza, admisión de escenarios, evidencia externa y límites operativos sin integrar cambios todavía.

## Clasificación

- Tipo de sprint: documental / auditoría.
- Clasificación: permitido.
- Acción: revisar, resumir y priorizar.
- No realiza merge de ramas antiguas.
- No hace cherry-pick.
- No borra ramas.

## Ramas revisadas

| Rama | Ref usada | Estado | Commits únicos | Archivos cambiados | Último commit | Muestra de archivos |
|---|---|---|---:|---:|---|---|
| `eco-sne-stable-admission-plan` | `eco-sne-stable-admission-plan` | `review_needed` | 21 | 209 | Document SNE ECO stable scenario admission plan | .github/workflows/ci.yml,.github/workflows/eco-check.yml Makefile,README.md data/governance/sne_eco_sensitive_intake_candidates.jsonl,data/governance/sne_eco_sensitive_source_registry.jsonl data/training/sne_eco_empirical_challenge_eval.jsonl,data/training/sne_eco_empirical_seed_dataset.jsonl docs/architecture/README.md,docs/architecture/eco-minimal-simulation-demo.md |
| `eco-sne-stable-admission-dry-run` | `eco-sne-stable-admission-dry-run` | `review_needed` | 20 | 207 | Add SNE ECO stable admission dry run | .github/workflows/ci.yml,.github/workflows/eco-check.yml Makefile,README.md data/governance/sne_eco_sensitive_intake_candidates.jsonl,data/governance/sne_eco_sensitive_source_registry.jsonl data/training/sne_eco_empirical_challenge_eval.jsonl,data/training/sne_eco_empirical_seed_dataset.jsonl docs/architecture/README.md,docs/architecture/eco-minimal-simulation-demo.md |
| `eco-sne-external-evidence-policy` | `eco-sne-external-evidence-policy` | `review_needed` | 19 | 212 | Add SNE ECO external evidence policy tests | .github/workflows/ci.yml,.github/workflows/eco-check.yml Makefile,README.md data/governance/sne_eco_sensitive_intake_candidates.jsonl,data/governance/sne_eco_sensitive_source_registry.jsonl data/training/sne_eco_empirical_challenge_eval.jsonl,data/training/sne_eco_empirical_seed_dataset.jsonl docs/architecture/README.md,docs/architecture/eco-minimal-simulation-demo.md |
| `eco-sne-external-evidence-review` | `eco-sne-external-evidence-review` | `review_needed` | 18 | 214 | Add SNE ECO external evidence review tests | .github/workflows/ci.yml,.github/workflows/eco-check.yml Makefile,README.md data/governance/sne_eco_sensitive_intake_candidates.jsonl,data/governance/sne_eco_sensitive_source_registry.jsonl data/training/sne_eco_empirical_challenge_eval.jsonl,data/training/sne_eco_empirical_seed_dataset.jsonl docs/architecture/README.md,docs/architecture/eco-minimal-simulation-demo.md |
| `eco-sne-external-scenario-expansion` | `eco-sne-external-scenario-expansion` | `review_needed` | 17 | 216 | Add SNE ECO external scenario probe tests | .github/workflows/ci.yml,.github/workflows/eco-check.yml Makefile,README.md data/governance/sne_eco_sensitive_intake_candidates.jsonl,data/governance/sne_eco_sensitive_source_registry.jsonl data/training/sne_eco_empirical_challenge_eval.jsonl,data/training/sne_eco_empirical_seed_dataset.jsonl docs/architecture/README.md,docs/architecture/eco-minimal-simulation-demo.md |
| `eco-sne-admission-governance-command` | `eco-sne-admission-governance-command` | `review_needed` | 3 | 203 | Align admission governance command test with yellow status | .github/workflows/ci.yml,.github/workflows/eco-check.yml Makefile,README.md data/governance/sne_eco_sensitive_intake_candidates.jsonl,data/governance/sne_eco_sensitive_source_registry.jsonl data/training/sne_eco_empirical_challenge_eval.jsonl,data/training/sne_eco_empirical_seed_dataset.jsonl docs/architecture/README.md,docs/architecture/eco-minimal-simulation-demo.md |
| `eco-sne-readme-admission-governance` | `eco-sne-readme-admission-governance` | `review_needed` | 2 | 201 | Fix README admission governance wording | .github/workflows/ci.yml,.github/workflows/eco-check.yml Makefile,README.md data/governance/sne_eco_sensitive_intake_candidates.jsonl,data/governance/sne_eco_sensitive_source_registry.jsonl data/training/sne_eco_empirical_challenge_eval.jsonl,data/training/sne_eco_empirical_seed_dataset.jsonl docs/architecture/README.md,docs/architecture/eco-minimal-simulation-demo.md |
| `eco-sne-admission-governance-make-target` | `eco-sne-admission-governance-make-target` | `review_needed` | 1 | 202 | Add SNE ECO admission governance make target | .github/workflows/ci.yml,.github/workflows/eco-check.yml Makefile,README.md data/governance/sne_eco_sensitive_intake_candidates.jsonl,data/governance/sne_eco_sensitive_source_registry.jsonl data/training/sne_eco_empirical_challenge_eval.jsonl,data/training/sne_eco_empirical_seed_dataset.jsonl docs/architecture/README.md,docs/architecture/eco-minimal-simulation-demo.md |
| `sne-30-public-demo-governance` | `sne-30-public-demo-governance` | `review_needed` | 2 | 189 | Add SNE ECO PR checklist | .github/workflows/eco-check.yml,Makefile README.md,data/governance/sne_eco_sensitive_intake_candidates.jsonl data/governance/sne_eco_sensitive_source_registry.jsonl,data/training/sne_eco_empirical_challenge_eval.jsonl data/training/sne_eco_empirical_seed_dataset.jsonl,docs/architecture/README.md docs/architecture/eco-minimal-simulation-demo.md,docs/architecture/eco-operational-block-bitacora-131-136.md |
| `sne-36-evidence-matrix` | `sne-36-evidence-matrix` | `review_needed` | 1 | 179 | Add SNE ECO evidence matrix | .github/workflows/eco-check.yml,Makefile README.md,data/governance/sne_eco_sensitive_intake_candidates.jsonl data/governance/sne_eco_sensitive_source_registry.jsonl,data/training/sne_eco_empirical_challenge_eval.jsonl data/training/sne_eco_empirical_seed_dataset.jsonl,docs/architecture/README.md docs/architecture/eco-minimal-simulation-demo.md,docs/architecture/eco-operational-block-bitacora-131-136.md |

## Lectura operativa

Estas ramas deben revisarse antes que ramas de baseline, datos, evaluación o arquitectura bioinspirada, porque definen reglas de admisión, límites de uso, evidencia externa y criterios de seguridad del proyecto.

## Decisión recomendada

1. No integrar todo en bloque.
2. Revisar primero documentos de política y gobernanza.
3. Rescatar solo piezas vigentes y coherentes con main.
4. Convertir cualquier rescate futuro en PR pequeño.
5. Mantener separada cualquier modificación de baseline, datos o evaluación.

## Comandos seguros de inspección

```bash
git rev-list --count main..NOMBRE_RAMA
git diff --stat main..NOMBRE_RAMA
git diff --name-only main..NOMBRE_RAMA
git log --oneline main..NOMBRE_RAMA
```

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa.
