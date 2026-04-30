# E.C.O. - Router por confianza calibrado

## Propósito

Este informe evalúa un router sin oráculo que decide entre `baseline_v3` y `embedding_semireal` usando confianza interna.

A diferencia de R8-G.4, el umbral se selecciona en una partición de calibración y luego se evalúa en test separado.

```text
train       -> entrena modelos
calibration -> selecciona umbral
test        -> evalúa router con umbral fijo
```

## Configuración

| Campo | Valor |
| --- | --- |
| Dataset | examples/eco_labeled_sequences.tsv |
| Repeticiones | 50 |
| Test ratio | 0.3 |
| Calibration ratio sobre train_cal | 0.25 |
| Seed base | 42 |
| Embedding k | 4 |
| Dimensiones | 128 |
| Decisión | router_calibrado_prometedor |

## Resumen general

| Modelo | Accuracy prom. | Macro F1 prom. | Macro F1 std |
| --- | ---: | ---: | ---: |
| baseline_v3 | 0.6967 | 0.6589 | 0.1012 |
| embedding_semireal | 0.8344 | 0.8311 | 0.0817 |
| confidence_router_calibrated | 0.9156 | 0.9114 | 0.1008 |

## Umbrales seleccionados

- Umbral promedio: `0.207`
- Umbral mínimo: `0.0`
- Umbral máximo: `0.35`

## Rutas usadas

| Ruta | Veces usada |
| --- | ---: |
| baseline_v3 | 606 |
| embedding_semireal | 294 |

## Detalle por repetición

| Seed | Train | Calibration | Test | Umbral | V3 F1 | Semi-real F1 | Router F1 | Usa V3 | Usa Semi-real |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 42 | 32 | 10 | 18 | 0.0 | 0.9443 | 0.9443 | 0.9443 | 18 | 0 |
| 43 | 32 | 10 | 18 | 0.25 | 0.7662 | 0.8889 | 0.9443 | 9 | 9 |
| 44 | 32 | 10 | 18 | 0.2 | 0.7662 | 0.775 | 0.9443 | 13 | 5 |
| 45 | 32 | 10 | 18 | 0.15 | 0.7662 | 0.7662 | 1.0 | 13 | 5 |
| 46 | 32 | 10 | 18 | 0.3 | 0.625 | 0.9443 | 1.0 | 9 | 9 |
| 47 | 32 | 10 | 18 | 0.3 | 0.5418 | 0.7214 | 0.8286 | 10 | 8 |
| 48 | 32 | 10 | 18 | 0.25 | 0.625 | 0.775 | 0.9443 | 9 | 9 |
| 49 | 32 | 10 | 18 | 0.15 | 0.625 | 0.7214 | 0.8286 | 14 | 4 |
| 50 | 32 | 10 | 18 | 0.2 | 0.5418 | 0.8889 | 0.9443 | 11 | 7 |
| 51 | 32 | 10 | 18 | 0.25 | 0.625 | 0.9443 | 1.0 | 11 | 7 |
| 52 | 32 | 10 | 18 | 0.2 | 0.625 | 0.7662 | 1.0 | 12 | 6 |
| 53 | 32 | 10 | 18 | 0.2 | 0.4462 | 1.0 | 0.8875 | 12 | 6 |
| 54 | 32 | 10 | 18 | 0.25 | 0.625 | 0.8889 | 0.9443 | 9 | 9 |
| 55 | 32 | 10 | 18 | 0.2 | 0.7662 | 0.8875 | 1.0 | 14 | 4 |
| 56 | 32 | 10 | 18 | 0.0 | 0.5418 | 0.8875 | 0.5418 | 18 | 0 |
| 57 | 32 | 10 | 18 | 0.25 | 0.625 | 0.8328 | 0.8875 | 13 | 5 |
| 58 | 32 | 10 | 18 | 0.1 | 0.625 | 0.7662 | 0.8875 | 13 | 5 |
| 59 | 32 | 10 | 18 | 0.2 | 0.7662 | 0.8286 | 1.0 | 9 | 9 |
| 60 | 32 | 10 | 18 | 0.2 | 0.699 | 0.775 | 0.9443 | 13 | 5 |
| 61 | 32 | 10 | 18 | 0.2 | 0.699 | 0.7778 | 0.8875 | 13 | 5 |
| 62 | 32 | 10 | 18 | 0.1 | 0.7662 | 0.8875 | 1.0 | 13 | 5 |
| 63 | 32 | 10 | 18 | 0.25 | 0.699 | 0.8286 | 1.0 | 12 | 6 |
| 64 | 32 | 10 | 18 | 0.05 | 0.8286 | 0.699 | 0.9443 | 14 | 4 |
| 65 | 32 | 10 | 18 | 0.3 | 0.5418 | 1.0 | 1.0 | 9 | 9 |
| 66 | 32 | 10 | 18 | 0.25 | 0.699 | 0.8328 | 0.8286 | 15 | 3 |
| 67 | 32 | 10 | 18 | 0.1 | 0.625 | 0.9443 | 0.699 | 17 | 1 |
| 68 | 32 | 10 | 18 | 0.0 | 0.625 | 0.8328 | 0.625 | 18 | 0 |
| 69 | 32 | 10 | 18 | 0.25 | 0.7662 | 0.9443 | 1.0 | 9 | 9 |
| 70 | 32 | 10 | 18 | 0.2 | 0.625 | 0.699 | 0.9443 | 13 | 5 |
| 71 | 32 | 10 | 18 | 0.2 | 0.699 | 0.8875 | 1.0 | 12 | 6 |
| 72 | 32 | 10 | 18 | 0.2 | 0.5418 | 0.6667 | 0.8286 | 12 | 6 |
| 73 | 32 | 10 | 18 | 0.25 | 0.699 | 0.8286 | 1.0 | 13 | 5 |
| 74 | 32 | 10 | 18 | 0.15 | 0.699 | 0.8328 | 0.9443 | 13 | 5 |
| 75 | 32 | 10 | 18 | 0.25 | 0.5418 | 0.8875 | 0.8286 | 13 | 5 |
| 76 | 32 | 10 | 18 | 0.25 | 0.699 | 0.8875 | 1.0 | 9 | 9 |
| 77 | 32 | 10 | 18 | 0.1 | 0.7662 | 0.775 | 0.8875 | 16 | 2 |
| 78 | 32 | 10 | 18 | 0.3 | 0.8286 | 0.7662 | 1.0 | 9 | 9 |
| 79 | 32 | 10 | 18 | 0.35 | 0.625 | 0.8875 | 0.9443 | 10 | 8 |
| 80 | 32 | 10 | 18 | 0.35 | 0.4462 | 0.6625 | 0.7662 | 9 | 9 |
| 81 | 32 | 10 | 18 | 0.25 | 0.4462 | 0.7778 | 0.7662 | 13 | 5 |
| 82 | 32 | 10 | 18 | 0.25 | 0.7662 | 0.8889 | 0.9443 | 13 | 5 |
| 83 | 32 | 10 | 18 | 0.3 | 0.625 | 0.8889 | 0.8875 | 11 | 7 |
| 84 | 32 | 10 | 18 | 0.25 | 0.699 | 0.7662 | 1.0 | 12 | 6 |
| 85 | 32 | 10 | 18 | 0.25 | 0.625 | 0.8875 | 1.0 | 9 | 9 |
| 86 | 32 | 10 | 18 | 0.15 | 0.5418 | 0.775 | 0.7662 | 15 | 3 |
| 87 | 32 | 10 | 18 | 0.3 | 0.699 | 0.8328 | 0.8875 | 9 | 9 |
| 88 | 32 | 10 | 18 | 0.2 | 0.625 | 0.7778 | 0.8875 | 12 | 6 |
| 89 | 32 | 10 | 18 | 0.15 | 0.625 | 0.7662 | 0.9443 | 13 | 5 |
| 90 | 32 | 10 | 18 | 0.35 | 0.699 | 0.775 | 0.9443 | 9 | 9 |
| 91 | 32 | 10 | 18 | 0.15 | 0.625 | 0.8889 | 0.9443 | 11 | 7 |

## Decisión E.C.O.

**Decisión:** `router_calibrado_prometedor`

Lectura prudente:

- Si el router calibrado supera a `baseline_v3`, ya existe una señal más honesta que R8-G.4.
- Si además se acerca al router oracular, E.C.O. gana una válvula adaptativa realista.
- Si baja frente al router no calibrado, es esperable: se eliminó optimismo por selección de umbral.

## Límite responsable

Este resultado sigue usando dataset demostrativo. No es diagnóstico clínico, no es benchmark científico general y no reemplaza validación externa.
