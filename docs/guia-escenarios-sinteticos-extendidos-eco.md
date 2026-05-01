# Guía de escenarios sintéticos extendidos E.C.O.

Esta guía explica el catálogo extendido de transiciones para S.N.E.-E.C.O.

## Por qué existe

El dataset mínimo tiene 4 rutas. Sirve para validar el funcionamiento, pero es demasiado pequeño para evaluar generalización.

El holdout inicial puede dar métricas bajas porque el baseline encuentra rutas no vistas y cae al estado por defecto.

## Qué agrega el catálogo extendido

El catálogo `EXTENDED_TRANSITION_PACKETS` agrega rutas sintéticas controladas:

```text
válidas variadas
válidas ricas en GC
válidas ricas en AT
secuencias cortas
caracteres inválidos
alto contenido N
duplicados
recurrencias
secuencias largas
colas inválidas
```

## Cómo usarlo

Dataset extendido:

```bash
python scripts/run_sne_eco_state_dataset.py --extended --output-json results/sne_eco_state_dataset_extended.json --output-tsv results/sne_eco_state_dataset_extended.tsv
```

Holdout extendido:

```bash
python scripts/run_sne_eco_state_holdout.py --extended --output-json results/sne_eco_state_holdout_extended_report.json --output-md results/sne_eco_state_holdout_extended_report.md
```

## Límite responsable

Estos escenarios son sintéticos y educativos. No son muestras reales, no son datos clínicos, no son evidencia forense y no modelan conciencia humana.

## Objetivo técnico

Aumentar la cobertura de rutas digestivas para que el baseline pueda distinguir mejor entre memorización, reglas aprendidas y falta de datos.
