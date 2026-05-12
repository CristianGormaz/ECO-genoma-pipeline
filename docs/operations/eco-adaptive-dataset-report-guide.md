# Guía de reporte operativo del dataset adaptativo E.C.O.

Esta guía explica cómo generar una lectura operativa del ejemplo sintético de dataset adaptativo.

## Objetivo

Convertir el ejemplo sintético del dataset adaptativo en un reporte JSON/Markdown trazable, legible y verificable.

## Comando

```bash
make eco-adaptive-dataset-report
```

## Salidas

- `results/eco_adaptive_dataset_report.json`
- `results/eco_adaptive_dataset_report.md`

## Límites responsables

- sin datos reales;
- sin datos sensibles;
- sin datos genéticos privados;
- sin entrenamiento;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas.

## Uso recomendado

Usar este reporte para revisar el estado documental del dataset adaptativo sintético antes de cualquier paso posterior.

No usarlo como dataset real ni como habilitación de entrenamiento.
