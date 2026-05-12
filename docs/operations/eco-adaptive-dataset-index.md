# Índice operativo del dataset adaptativo E.C.O.

Este índice reúne las piezas actuales del dataset adaptativo sintético E.C.O. en una sola entrada operativa.

## Estado

- Clasificación: permitido.
- Uso: documental, sintético y trazable.
- No habilita entrenamiento.
- No habilita uso de datos reales.
- No modifica baseline.
- No recalibra umbrales.
- No produce afirmaciones biomédicas aplicadas.

## Piezas principales

- Contrato del dataset adaptativo: `docs/architecture/eco-adaptive-dataset-contract.md`
- Ejemplo sintético JSON: `docs/architecture/eco-adaptive-dataset-example.json`
- Ejemplo sintético Markdown: `docs/architecture/eco-adaptive-dataset-example.md`
- Validador del ejemplo: `scripts/validate_eco_adaptive_dataset_example.py`
- Reporte operativo: `scripts/run_eco_adaptive_dataset_report.py`
- Guía del reporte: `docs/operations/eco-adaptive-dataset-report-guide.md`
- Dashboard sintético: `scripts/run_eco_synthetic_operational_dashboard.py`

## Comandos útiles

- Validar ejemplo sintético: `make eco-validate-adaptive-dataset-example`
- Generar reporte operativo: `make eco-adaptive-dataset-report`
- Generar dashboard sintético: `make eco-synthetic-operational-dashboard`
- Validación completa limpia: `make eco-check-clean`

## Límites responsables

- sin datos reales
- sin datos sensibles
- sin datos genéticos privados
- sin entrenamiento
- sin modificación de baseline
- sin recalibración de umbrales
- sin afirmaciones biomédicas aplicadas

## Lectura simple

El dataset adaptativo actual no es un dataset real. Es una maqueta sintética y verificable que sirve para probar estructura, trazabilidad, límites responsables y operación del pipeline E.C.O. antes de considerar cualquier fuente externa.
