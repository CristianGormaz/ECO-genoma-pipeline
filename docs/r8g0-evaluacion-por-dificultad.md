# R8-G.0 - Evaluación por dificultad de casos E.C.O.

## Propósito

Este documento define el siguiente paso antes de integrar embeddings reales como DNABERT.

La pregunta central es:

> ¿embedding_semireal mejora porque resuelve mejor casos difíciles/ambiguos, o solo porque aprovecha señales fáciles del dataset?

## Estado previo

- baseline_v1: control explicable.
- baseline_v3: referencia oficial pre-embeddings.
- embedding_placeholder: contrato vectorial validado.
- embedding_semireal: candidato experimental robustecido.

## Evidencia R8-F

Con 50 repeticiones:

- baseline_v3 macro F1 promedio: 0.8001
- embedding_semireal macro F1 promedio: 0.8273
- delta: +0.0273
- embedding_semireal gana/empata/pierde vs baseline_v3: 28/3/19
- embedding_semireal std: 0.0909
- baseline_v3 std: 0.1542

## Decisión prudente

embedding_semireal queda como candidato experimental robustecido, pero no reemplaza oficialmente a baseline_v3.

## Siguiente criterio

Para avanzar hacia candidato pre-oficial, debe evaluarse rendimiento por dificultad:

1. easy
2. ambiguous
3. hard

## Regla E.C.O.

Si embedding_semireal mejora principalmente en casos easy, no se promueve.

Si mejora en ambiguous/hard y mantiene menor variabilidad, puede pasar a candidato pre-oficial.

## Límite responsable

Esta evaluación sigue usando dataset demostrativo. No es benchmark científico, no es diagnóstico clínico y no representa desempeño externo.
