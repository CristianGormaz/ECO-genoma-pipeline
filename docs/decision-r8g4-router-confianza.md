# E.C.O. - Router sin oráculo por confianza

## Propósito

Este informe evalúa un router que decide entre `baseline_v3` y `embedding_semireal` sin usar la etiqueta real de dificultad.

La regla evaluada es:

```text
si confianza_baseline_v3 >= umbral:
    usar baseline_v3
si no:
    usar embedding_semireal
```

## Configuración

| Campo | Valor |
| --- | --- |
| Dataset | examples/eco_labeled_sequences.tsv |
| Repeticiones | 50 |
| Test ratio | 0.4 |
| Seed base | 42 |
| Embedding k | 4 |
| Dimensiones | 128 |
| Mejor umbral | 0.3 |
| Decisión | router_confianza_prometedor |

## Mejor resultado

| Modelo | Accuracy prom. | Accuracy std | Macro F1 prom. | Macro F1 std |
| --- | ---: | ---: | ---: | ---: |
| baseline_v3 | 0.7325 | 0.0741 | 0.7063 | 0.0929 |
| embedding_semireal | 0.795 | 0.0745 | 0.7901 | 0.0803 |
| confidence_router | 0.9567 | 0.0382 | 0.9563 | 0.0392 |

## Rutas usadas por el router

| Ruta | Veces usada |
| --- | ---: |
| baseline_v3 | 790 |
| embedding_semireal | 410 |

## Barrido de umbrales

| Umbral | Router F1 prom. | Router std | V3 F1 prom. | Semi-real F1 prom. | Usa V3 | Usa Semi-real |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0 | 0.7063 | 0.0929 | 0.7063 | 0.7901 | 1200 | 0 |
| 0.05 | 0.7389 | 0.112 | 0.7063 | 0.7901 | 1140 | 60 |
| 0.1 | 0.7831 | 0.1289 | 0.7063 | 0.7901 | 1074 | 126 |
| 0.15 | 0.841 | 0.1295 | 0.7063 | 0.7901 | 968 | 232 |
| 0.2 | 0.8838 | 0.1058 | 0.7063 | 0.7901 | 891 | 309 |
| 0.25 | 0.9339 | 0.0747 | 0.7063 | 0.7901 | 816 | 384 |
| 0.3 | 0.9563 | 0.0392 | 0.7063 | 0.7901 | 790 | 410 |
| 0.35 | 0.9563 | 0.0392 | 0.7063 | 0.7901 | 790 | 410 |
| 0.4 | 0.9546 | 0.0391 | 0.7063 | 0.7901 | 778 | 422 |
| 0.45 | 0.9496 | 0.041 | 0.7063 | 0.7901 | 741 | 459 |
| 0.5 | 0.9404 | 0.0418 | 0.7063 | 0.7901 | 643 | 557 |
| 0.55 | 0.9279 | 0.0472 | 0.7063 | 0.7901 | 564 | 636 |
| 0.6 | 0.9088 | 0.0563 | 0.7063 | 0.7901 | 500 | 700 |
| 0.65 | 0.8903 | 0.0608 | 0.7063 | 0.7901 | 397 | 803 |
| 0.7 | 0.8648 | 0.062 | 0.7063 | 0.7901 | 318 | 882 |
| 0.75 | 0.8315 | 0.0801 | 0.7063 | 0.7901 | 260 | 940 |
| 0.8 | 0.7938 | 0.0785 | 0.7063 | 0.7901 | 189 | 1011 |

## Decisión E.C.O.

**Decisión:** `router_confianza_prometedor`

Lectura prudente:

- Este router ya no usa `easy`, `ambiguous` ni `hard` para decidir.
- Si mejora frente a `baseline_v3`, demuestra una ruta más realista que el router oracular.
- Si no supera al router oracular, es normal: el oracular usa información privilegiada.
- El siguiente paso sería calibrar el umbral con un conjunto de validación separado.

## Límite responsable

Este resultado sigue siendo demostrativo. No es diagnóstico clínico, no es benchmark científico general y no reemplaza validación externa.
