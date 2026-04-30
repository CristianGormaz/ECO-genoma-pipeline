# R8-G.3 - Router sin oráculo por confianza E.C.O.

## Propósito

R8-G.2 demostró que un router híbrido por dificultad mejora el rendimiento general.

El límite es que usa dificultad conocida: easy, ambiguous y hard.

R8-G.3 define el siguiente paso: crear un router sin oráculo, capaz de decidir entre baseline_v3 y embedding_semireal usando señales internas de confianza.

## Hipótesis

Si baseline_v3 está muy seguro, se usa baseline_v3.

Si baseline_v3 tiene baja confianza, se deriva a embedding_semireal.

Esto imita una digestión adaptativa:

```text
dato claro      -> ruta explicable rápida
dato incierto   -> ruta vectorial más profunda
dato difícil    -> ruta semireal robustecida
```

## Estado previo

- baseline_v1: control explicable.
- baseline_v3: referencia oficial pre-embeddings.
- embedding_placeholder: contrato vectorial validado.
- embedding_semireal: candidato experimental robustecido.
- hybrid_router: router oracular prometedor.

## Resultado R8-G.2

| Modelo | Macro F1 promedio | Std |
| --- | ---: | ---: |
| baseline_v3 | 0.8065 | 0.1160 |
| embedding_semireal | 0.8204 | 0.0738 |
| hybrid_router | 0.8791 | 0.0677 |

## Regla R8-G.3

El nuevo router no debe mirar la dificultad real del dataset.

Debe decidir usando una regla tipo:

```text
si confianza_baseline_v3 >= umbral:
    usar baseline_v3
si no:
    usar embedding_semireal
```

## Criterio de éxito

El router sin oráculo será prometedor si:

1. supera a baseline_v3 en macro F1 promedio;
2. se acerca al router híbrido oracular;
3. mantiene o reduce variabilidad;
4. no depende de etiquetas easy/ambiguous/hard para decidir;
5. conserva trazabilidad.

## Límite responsable

Esta evaluación sigue siendo demostrativa. No es diagnóstico clínico, no es benchmark científico general y no representa desempeño externo.
