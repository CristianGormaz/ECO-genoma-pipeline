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

