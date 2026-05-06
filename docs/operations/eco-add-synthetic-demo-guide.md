# Guía para agregar una demo sintética E.C.O.

## Estado
Estado: operativo.

Clasificación: permitido.

## Propósito
Esta guía define el mínimo seguro para agregar una nueva demo sintética al pipeline E.C.O. sin romper el registro, el validador global ni los límites responsables.

## Checklist obligatorio
1. Crear un runner en scripts/run_eco_<nombre>_demo.py.
2. Generar salida JSON en results/eco_<nombre>_demo.json.
3. Generar salida Markdown en results/eco_<nombre>_demo.md.
4. Registrar la demo en docs/architecture/eco-synthetic-demo-registry.json.
5. Documentarla en docs/architecture/eco-synthetic-demo-registry.md.
6. Actualizar docs/architecture/eco-synthetic-demos-index.md si corresponde.
7. Crear o actualizar tests.
8. Validar con make eco-validate-synthetic-demos.

## Validación mínima antes del commit
- make eco-status
- make eco-validate-synthetic-demos
- python3 -m pytest -q
- git status --short

## Límites responsables
- No usar datos sensibles.
- No entrenar modelos.
- No modificar baseline estable.
- No recalibrar umbrales.
- No hacer afirmaciones biomédicas aplicadas.
- No convertir metáforas simbólicas en conclusiones científicas.
