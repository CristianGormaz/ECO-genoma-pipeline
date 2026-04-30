# R8-G.5 - Router por confianza calibrado E.C.O.

## Propósito

R8-G.4 mostró una señal muy fuerte del router por confianza, pero el umbral fue seleccionado mediante barrido sobre la misma evaluación.

R8-G.5 define una evaluación más honesta: elegir el umbral en una partición de calibración y medir el rendimiento final en test separado.

## Problema detectado

El router sin oráculo no usa easy/ambiguous/hard para decidir, lo cual es correcto.

Pero si el mejor umbral se elige mirando todos los resultados de test, aparece un riesgo de optimismo metodológico.

## Regla R8-G.5

```text
train       -> entrenar baseline_v3 y embedding_semireal
calibration -> elegir mejor umbral de confianza
test        -> evaluar el router con ese umbral ya fijado
```

## Criterio de éxito

El router calibrado será prometedor si:

1. supera a baseline_v3 en macro F1 promedio;
2. mantiene menor o similar variabilidad;
3. no usa etiquetas de dificultad para decidir;
4. no selecciona el umbral mirando el test final;
5. conserva trazabilidad de decisión.

## Estado operativo

```text
baseline_v3 = referencia oficial pre-embeddings
embedding_semireal = candidato experimental robustecido
confidence_router = candidato prometedor, pendiente de calibración honesta
confidence_router_calibrado = próximo filtro metodológico
```

## Límite responsable

Este paso sigue usando dataset demostrativo. No es diagnóstico clínico, no es benchmark científico general y no representa desempeño externo.
