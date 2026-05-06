# Mapa operativo del proyecto E.C.O.

## Estado

Estado: operativo.

Clasificación: permitido.

Este mapa ayuda a ubicar las piezas principales del repositorio sin cambiar código ni resultados del pipeline.

## Entrada principal

- README.md: punto de entrada general del proyecto.
- Makefile: comandos operativos reutilizables.

## Comandos útiles

- make eco-status: revisa rama, HEAD, origin/main y limpieza del árbol.
- make eco-vacuum-state-demo: genera la demo educativa de Vacuum State.

## Carpetas principales

- docs/operations/: guías para operar el repositorio con seguridad.
- docs/research/: documentos de investigación y trazabilidad conceptual.
- scripts/: comandos ejecutables del pipeline.
- tests/: validaciones automáticas con pytest.
- results/: salidas generadas por demos o reportes cuando corresponde.

## Archivos operativos actuales

- docs/operations/terminal-stop-guide.md: guía para saber cuándo detenerse.
- docs/operations/project-map.md: este mapa operativo.
- docs/research/eco-research-index.md: índice de investigación E.C.O.
- docs/architecture/eco-synthetic-demos-index.md: índice de demos sintéticas y sus validaciones.
- docs/architecture/eco-synthetic-data-contract.md: contrato mínimo para datos sintéticos y trazas de simulación.
- scripts/run_eco_status.py: inspección rápida del estado del repositorio.

## Límite responsable

Este documento es operativo y documental. No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no hace afirmaciones biomédicas aplicadas.

## Validación sintética global

- make eco-validate-synthetic-demos: ejecuta y valida todas las demos sintéticas permitidas.

## Registro sintético

- docs/architecture/eco-synthetic-demo-registry.md: registro de demos sintéticas oficiales, comandos, salidas y validadores.
- make eco-validate-synthetic-demos: validación global recomendada antes de cerrar cambios relacionados con demos sintéticas.
## Guía para nuevas demos sintéticas

- [Guía para agregar una demo sintética E.C.O.](eco-add-synthetic-demo-guide.md)

## Reporte suite sintética

- `make eco-synthetic-demos-suite-report`: genera un resumen operativo de las demos sintéticas registradas.
- `scripts/run_eco_synthetic_demos_suite_report.py`: runner del reporte.
- `results/eco_synthetic_demos_suite_report.json`: salida JSON temporal.
- `results/eco_synthetic_demos_suite_report.md`: salida Markdown temporal.

## Guía de interpretación del reporte suite sintético

- [Guía de interpretación del reporte de suite sintética E.C.O.](docs/operations/eco-synthetic-demos-suite-report-guide.md)
- Comando asociado: `make eco-synthetic-demos-suite-report`
- Uso: entender el estado `passed`, las salidas generadas y los límites responsables del reporte.

## Check operativo completo

- Comando recomendado: `make eco-check`
- Ejecuta estado operativo, validación global de demos sintéticas, reporte suite y pytest global.
- Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin recalibración.

## Limpieza de resultados sintéticos

- Comando: `make eco-clean-results`
- Uso: eliminar artefactos generados en `results/` por demos sintéticas y reporte suite.
- Límite: no elimina código, documentación, tests, baseline ni umbrales.

## Chequeo operativo con limpieza

- Comando recomendado: `make eco-check-clean`
- Ejecuta `make eco-check` y luego `make eco-clean-results`.
- Uso: validar el pipeline completo y limpiar salidas sintéticas generadas en `results/`.
- Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin baseline; sin recalibración.
