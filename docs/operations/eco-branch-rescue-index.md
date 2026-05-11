# Índice de rescate de ramas prioritarias E.C.O.

Este documento transforma la matriz de decisión de ramas en una guía práctica para continuar el trabajo sin perder contexto.

## Objetivo

Ayudar a responder:

1. Qué rama conviene revisar primero.
2. Qué ramas deben conservarse.
3. Qué ramas pueden rescatarse como documentación.
4. Qué ramas no deben tocarse sin revisión.

## Estado base recomendado

Antes de revisar cualquier rama, confirmar:

- rama main;
- árbol limpio;
- HEAD igual a origin/main;
- eco-status green;
- pruebas pasando con .venv/bin/python.

## Comandos base

```bash
git switch main
git pull --ff-only origin main
make eco-status
.venv/bin/python -m pytest -q
git status --short
git rev-list --left-right --count HEAD...origin/main
```

Resultado esperado: main, green, árbol limpio, tests pasando y relación 0 0.

## Orden recomendado de revisión

| Prioridad | Grupo | Acción recomendada |
|---|---|---|
| 1 | Gobernanza y evidencia externa | Revisar primero, porque define reglas de admisión y límites. |
| 2 | Baseline, datos y evaluación | Revisar con cuidado; no modificar umbrales ni baseline sin auditoría. |
| 3 | Validación, release y estabilidad | Revisar después de gobernanza y baseline. |
| 4 | Arquitectura bioinspirada | Conservar como línea conceptual; migrar solo si encaja con el sistema actual. |
| 5 | Portfolio y documentación pública | Rescatar piezas útiles para explicar el proyecto. |
| 6 | Baja prioridad histórica | Revisar después; no borrar sin respaldo. |
| 7 | Respaldos locales | No tocar salvo que exista respaldo equivalente claro. |

## Ramas prioritarias sugeridas

### Gobernanza y evidencia

- eco-sne-stable-admission-plan
- eco-sne-stable-admission-dry-run
- eco-sne-external-evidence-policy
- eco-sne-external-evidence-review
- eco-sne-external-scenario-expansion
- eco-sne-admission-governance-command
- eco-sne-readme-admission-governance
- eco-sne-admission-governance-make-target

### Baseline, datos y evaluación

- eco-adaptive-state-baseline-v0
- eco-adaptive-state-foundation
- eco-operationalize-adaptive-dataset
- eco-sne-hierarchical-baseline
- eco-sne-confidence-resolution
- eco-sne-recurrence-resolution
- eco-sne-stability-suite
- sne-37-compare-v1-1
- sne-38-make-compare-v1-1
- sne-39-portfolio-demo-v1-1-gate
- sne-40-portfolio-check-v1-1-report

### Arquitectura bioinspirada

- sne-eco-enteric-module
- eco-submucosal-sensing
- eco-homeostasis-layer
- eco-myenteric-motility
- eco-defense-layer
- eco-gut-brain-report
- eco-microbiota-memory
- eco-enteric-modularization
- eco-integrate-enteric-organs

## Regla de seguridad

No borrar ramas no mergeadas sin revisar:

```bash
git rev-list --count main..NOMBRE_RAMA
git diff --stat main..NOMBRE_RAMA
```

Si el conteo es mayor que cero, esa rama tiene trabajo que main no contiene.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas.

## Relación con la matriz

Documento base:

```bash
make eco-branch-decision-matrix
```
