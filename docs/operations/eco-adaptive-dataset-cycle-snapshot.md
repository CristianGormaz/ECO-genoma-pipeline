# Snapshot operativo del ciclo adaptativo E.C.O.

Este documento cierra el ciclo operativo actual del dataset adaptativo sintético E.C.O.

## Estado del ciclo

- Estado: green.
- Clasificación: permitido.
- Uso: documental, sintético, trazable y operativo.
- No habilita entrenamiento.
- No habilita ingestión de datos reales.
- No modifica baseline.
- No recalibra umbrales.
- No produce afirmaciones biomédicas aplicadas.

## Avances integrados

| PR | Avance | Resultado |
|---|---|---|
| #186 | Endurecimiento del reporte adaptativo | El reporte detecta límites responsables desde JSON y Markdown. |
| #187 | Índice operativo del dataset adaptativo | Las piezas principales quedaron reunidas en una entrada operativa. |
| #188 | Readiness gate adaptativo | El sistema valida si el paquete documental mínimo está completo. |
| #189 | Integración con eco-check | El readiness gate quedó dentro de la validación operativa general. |
| #190 | Integración con dashboard | El dashboard sintético operativo ahora muestra 5 componentes. |

## Piezas actuales

- Contrato: `docs/architecture/eco-adaptive-dataset-contract.md`
- Ejemplo JSON: `docs/architecture/eco-adaptive-dataset-example.json`
- Ejemplo Markdown: `docs/architecture/eco-adaptive-dataset-example.md`
- Guía del reporte: `docs/operations/eco-adaptive-dataset-report-guide.md`
- Índice operativo: `docs/operations/eco-adaptive-dataset-index.md`
- Reporte operativo: `scripts/run_eco_adaptive_dataset_report.py`
- Readiness gate: `scripts/run_eco_adaptive_dataset_readiness_gate.py`
- Dashboard sintético: `scripts/run_eco_synthetic_operational_dashboard.py`

## Validaciones principales

- `make eco-validate-adaptive-dataset-example`
- `make eco-adaptive-dataset-report`
- `make eco-adaptive-dataset-readiness-gate`
- `make eco-synthetic-operational-dashboard`
- `make eco-check-clean`
- `python3 -m pytest -q`

## Lectura simple

El ciclo adaptativo actual no convierte E.C.O. en un sistema de datos reales. Deja preparada una base sintética, documental y verificable para revisar estructura, trazabilidad, límites responsables y operación del pipeline antes de considerar cualquier fuente externa.

## Siguiente límite operativo

Antes de agregar fuentes externas, debe existir una decisión explícita sobre:

- origen de datos;
- licencia o permiso de uso;
- ausencia de datos sensibles;
- propósito no clínico;
- criterios de exclusión;
- validación documental;
- separación entre simulación, evaluación e interpretación.
