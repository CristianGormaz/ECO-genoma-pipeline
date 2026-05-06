# Guía de interpretación del reporte de suite sintética E.C.O.

## Estado

Estado: operativo.

Clasificación: permitido.

## Propósito

Esta guía explica cómo leer el reporte general de demos sintéticas E.C.O. generado por el comando `make eco-synthetic-demos-suite-report`.

## Comando principal

```bash
make eco-synthetic-demos-suite-report
```

## Archivos generados

- `results/eco_synthetic_demos_suite_report.json`: salida estructurada para inspección técnica.
- `results/eco_synthetic_demos_suite_report.md`: salida legible para revisión humana.

## Qué significa Estado: passed

Significa que el reporte pudo leer el registro operativo de demos sintéticas y resumir las demos oficiales registradas.

No significa que E.C.O. haga afirmaciones biomédicas aplicadas, ni que use datos reales, ni que entrene modelos.

## Qué revisar después de ejecutar el reporte

1. Que el estado sea `passed`.
2. Que el número de demos registradas coincida con el registro JSON.
3. Que las salidas JSON y Markdown se generen en `results/`.
4. Que luego se limpien los archivos temporales antes del commit.

## Validación recomendada

```bash
make eco-status
make eco-validate-synthetic-demos
make eco-synthetic-demos-suite-report
python3 -m pytest -q
git status --short
```

## Límite responsable

Este reporte usa solo datos sintéticos. No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no convierte metáforas simbólicas en conclusiones científicas.

## Check operativo completo

- Comando recomendado: `make eco-check`
- Ejecuta estado operativo, validación global de demos sintéticas, reporte suite y pytest global.
- Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin recalibración.
