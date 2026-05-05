# E.C.O. — Trazabilidad de demo Vacuum State

## Estado

Estado: experimental.

Clasificación: permitido.

## Propósito

Este documento conecta la pieza conceptual del vacío informacional con la demo computacional mínima de E.C.O.

## Documento base

- `docs/research/eco-vacio-cuantico-patrones-minimos.md`

Ese documento define el vocabulario controlado:

- estado_base
- ausencia
- fluctuacion
- frontera
- medicion

## Demo asociada

- `scripts/run_eco_vacuum_state_demo.py`

La demo genera una representación educativa de un estado informacional mínimo inspirado en patrones del vacío cuántico.

## Salidas esperadas

Al ejecutar la demo, se generan:

- `results/eco_vacuum_state_demo.json`
- `results/eco_vacuum_state_demo.md`

## Lectura operativa

La demo no mide el vacío cuántico real. Representa una analogía computacional segura:

campo minimo -> estado base -> fluctuacion -> frontera -> medicion -> evento

## Límite responsable

Trabajo educativo/experimental. No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no afirma aplicaciones físicas reales.

## Criterio de aceptación

- El documento de trazabilidad existe.
- El documento referencia el documento base.
- El documento referencia el script de demo.
- El documento declara límites responsables.
- La demo sigue pasando sus pruebas.
