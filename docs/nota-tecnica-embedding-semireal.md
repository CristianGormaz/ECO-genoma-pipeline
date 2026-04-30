# Nota técnica: embedding semi-real E.C.O.

## Propósito

Esta ruta prepara una transición controlada entre el embedding placeholder y un embedding real futuro.

No pretende ser DNABERT ni un modelo profundo. Su función es probar una representación vectorial más exigente manteniendo bajo costo, trazabilidad y reproducibilidad local.

## Configuración actual

- Entrada: examples/eco_labeled_sequences.tsv
- Representación: frecuencias k-mer/proyección vectorial controlada.
- k: 4
- Dimensiones objetivo: 128
- Clasificador: centroid baseline sobre vectores normalizados.
- Comparación obligatoria: baseline_v1 y baseline_v3.

## Lectura prudente

Si el split fijo mejora, no se declara superioridad todavía. Primero debe repetirse la evaluación con distintos splits y compararse contra baseline_v3.

## Regla E.C.O.

Un modelo nuevo solo reemplaza a baseline_v3 si mejora de forma repetida, reduce variabilidad o aporta mejor desempeño en casos ambiguos/difíciles.

## Límites

- No es DNABERT.
- No es diagnóstico clínico.
- No representa benchmark científico.
- Es una ruta experimental para preparar embeddings reales.

## Decisión actual

embedding_semireal = transición controlada hacia embedding real, no reemplazo oficial de baseline_v3.
