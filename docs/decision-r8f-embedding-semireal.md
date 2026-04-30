# R8-F - Decisión extendida embedding semi-real E.C.O.

## Propósito

Este documento registra la evaluación extendida de embedding_semireal frente a baseline_v3.

No reemplaza automáticamente a baseline_v3. Su función es decidir si embedding_semireal queda habilitado como candidato experimental robustecido antes de avanzar hacia embeddings reales.

## Resultado con 30 repeticiones

| Modelo | Macro F1 promedio | Observación |
| --- | ---: | --- |
| baseline_v3 | 0.8040 | Referencia oficial pre-embeddings |
| embedding_semireal | 0.8327 | Señal superior en promedio |

- Delta embedding_semireal vs baseline_v3: +0.0287
- Gana/empata/pierde vs baseline_v3: 17/2/11

## Resultado con 50 repeticiones

| Modelo | Macro F1 promedio | Std | Mejor en repeticiones |
| --- | ---: | ---: | ---: |
| baseline_v3 | 0.8001 | 0.1542 | 18 |
| embedding_semireal | 0.8273 | 0.0909 | 21 |

- Delta embedding_semireal vs baseline_v3: +0.0273
- Gana/empata/pierde vs baseline_v3: 28/3/19
- Señal importante: embedding_semireal mejora el promedio y reduce la variabilidad.

## Decisión E.C.O.

embedding_semireal se mantiene como candidato experimental robustecido para evaluación pre-oficial.

No reemplaza todavía a baseline_v3 porque:

- El dataset sigue siendo demostrativo y pequeño.
- Aunque gana más veces de las que pierde, todavía pierde en 19 de 50 repeticiones.
- La mejora promedio es positiva, pero debe validarse por tipo de caso: fácil, ambiguo y difícil.
- No es DNABERT ni embedding profundo real.

## Estado operativo recomendado

```text
baseline_v1 = control explicable
baseline_v3 = referencia oficial pre-embeddings
embedding_placeholder = contrato vectorial validado
embedding_semireal = candidato experimental robustecido
```

## Próximo paso R8-G

Antes de integrar DNABERT o un backend externo, E.C.O. debe agregar una evaluación por dificultad de casos:

1. easy
2. ambiguous
3. hard

La regla prudente es simple: si embedding_semireal mejora principalmente por casos fáciles, no debe promoverse. Si mejora en ambiguos o difíciles y mantiene menor variabilidad, puede pasar a candidato pre-oficial.

## Límite responsable

Este resultado no es diagnóstico clínico, no es benchmark científico general y no representa desempeño sobre datos reales externos.
