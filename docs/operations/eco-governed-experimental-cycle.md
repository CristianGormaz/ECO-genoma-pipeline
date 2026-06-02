# E.C.O. Governed Experimental Cycle v1

## Propósito

El ciclo experimental gobernado conecta madurez por fase, admisión gobernada, gates, riesgos, rollback visible, límites responsables y decisión final auditable.

## Comando

```bash
.venv/bin/python scripts/run_eco_governed_experimental_cycle.py
```

## Salidas

```text
results/eco_governed_experimental_cycle.json
results/eco_governed_experimental_cycle.md
```

## Dimensiones evaluadas

- `phase_maturity`: evalúa `draft`, `synthetic`, `governed_experimental`, `stable_candidate` y `blocked`.
- `governed_admission`: verifica intake gate, source guard, maturity score, rollback evidence, responsible limits y decisión final.
- `gates`: revisa admisión de fuentes, intake sensible y evaluación ML gobernada.
- `rollback_visibility`: conserva evidencia de dry-run y candados de estabilidad.
- `final_decision`: deriva `advance | pause | review | reject` desde gates, riesgos y estados.

## Estados permitidos

```text
passed
attention
missing
future
blocked
```

## Decisiones permitidas

```text
advance
pause
review
reject
```

## Límite responsable

Este ciclo es sintético/documental y operacional. No usa datos reales, no entrena modelos, no usa datos sensibles, no diagnostica, no realiza interpretación clínica, no cambia baseline, no recalibra umbrales, no afirma conciencia y no representa libre albedrío real.
