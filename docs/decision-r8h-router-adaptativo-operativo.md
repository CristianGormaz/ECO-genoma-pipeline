# R8-H - Router adaptativo operativo E.C.O.

## Propósito

Este documento registra el cierre operativo del router adaptativo E.C.O.

El sistema ya puede decidir entre baseline_v3 y embedding_semireal usando una señal interna de confianza.

## Estado previo

- baseline_v1: control explicable.
- baseline_v3: referencia oficial pre-embeddings.
- embedding_semireal: candidato experimental robustecido.
- confidence_router_calibrado: router sin oráculo evaluado con calibración.
- adaptive_router_predict: CLI operativo para predicción individual.

## Resultado del router calibrado

| Modelo | Macro F1 promedio | Std | Lectura |
| --- | ---: | ---: | --- |
| baseline_v3 | 0.6589 | 0.1012 | Ruta explicable base |
| embedding_semireal | 0.8311 | 0.0817 | Ruta vectorial semi-real |
| confidence_router_calibrated | 0.9114 | 0.1008 | Válvula adaptativa prometedora |

## Regla operativa actual

```text
si confianza_baseline_v3 >= umbral:
    usar baseline_v3
si no:
    usar embedding_semireal
```

## Demo operativa

El comando adaptive-router-predict-demo ejecutó una predicción individual:

- Secuencia: demo_adaptive_router
- baseline_v3: regulatory, confianza 0.2615
- embedding_semireal: non_regulatory, confianza 0.2461
- Ruta seleccionada: baseline_v3
- Predicción final: regulatory

## Decisión E.C.O.

El router adaptativo queda como componente operativo experimental.

No reemplaza aún validación externa, pero ya demuestra una arquitectura útil:

```text
dato claro      -> ruta explicable rápida
dato incierto   -> ruta semi-real
dato difícil    -> decisión adaptativa por confianza
```

## Próximo paso recomendado

Preparar Pull Request de la rama feature/r8-embedding-real-contract hacia main.

Después del merge, el siguiente sprint debería enfocarse en predicción batch o integración con datos externos reales.

## Límite responsable

Este resultado sigue usando dataset demostrativo. No es diagnóstico clínico, no es benchmark científico general y no reemplaza validación externa.
