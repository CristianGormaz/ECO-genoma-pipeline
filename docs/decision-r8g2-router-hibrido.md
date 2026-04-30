# E.C.O. - Evaluación de router híbrido por dificultad

## Propósito

Este informe prueba una regla híbrida:

```text
easy      -> baseline_v3
ambiguous -> embedding_semireal
hard      -> embedding_semireal
```

La hipótesis es que `baseline_v3` conserva mejor los casos fáciles, mientras `embedding_semireal` aporta más valor en casos ambiguos y difíciles.

## Configuración

| Campo | Valor |
| --- | --- |
| Dataset | examples/eco_labeled_sequences.tsv |
| Repeticiones | 50 |
| Test ratio | 0.4 |
| Seed base | 42 |
| Embedding k | 4 |
| Dimensiones | 128 |
| Decisión | router_hibrido_prometedor |

## Resumen general

| Modelo | Accuracy prom. | Accuracy std | Macro F1 prom. | Macro F1 std |
| --- | ---: | ---: | ---: | ---: |
| baseline_v3 | 0.8133 | 0.1068 | 0.8065 | 0.116 |
| embedding_semireal | 0.8242 | 0.0694 | 0.8204 | 0.0738 |
| hybrid_router | 0.88 | 0.067 | 0.8791 | 0.0677 |

## Resumen por dificultad

### ambiguous

| Modelo | Accuracy prom. | Macro F1 prom. | Macro F1 std |
| --- | ---: | ---: | ---: |
| baseline_v3 | 0.7851 | 0.7621 | 0.2055 |
| embedding_semireal | 0.7971 | 0.7862 | 0.1332 |
| hybrid_router | 0.7971 | 0.7862 | 0.1332 |

### easy

| Modelo | Accuracy prom. | Macro F1 prom. | Macro F1 std |
| --- | ---: | ---: | ---: |
| baseline_v3 | 0.9387 | 0.9356 | 0.081 |
| embedding_semireal | 0.7744 | 0.7456 | 0.1981 |
| hybrid_router | 0.9387 | 0.9356 | 0.081 |

### hard

| Modelo | Accuracy prom. | Macro F1 prom. | Macro F1 std |
| --- | ---: | ---: | ---: |
| baseline_v3 | 0.771 | 0.742 | 0.2336 |
| embedding_semireal | 0.9303 | 0.9256 | 0.0973 |
| hybrid_router | 0.9303 | 0.9256 | 0.0973 |

## Decisión E.C.O.

**Decisión:** `router_hibrido_prometedor`

Lectura prudente:

- Si el router mejora el promedio sin aumentar la variabilidad, puede pasar a candidato pre-oficial condicional.
- Si solo empata, se mantiene como experimento arquitectónico.
- Este router todavía usa etiquetas de dificultad conocidas; en datos reales habría que inferir dificultad automáticamente.

## Límite responsable

Este resultado sigue siendo demostrativo. No es diagnóstico clínico, no es benchmark científico general y no reemplaza validación externa.
