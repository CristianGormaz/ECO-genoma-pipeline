# Nota técnica: decisión de modelos E.C.O.

## Propósito

Esta nota documenta la decisión operativa actual del pipeline **E.C.O. — Entérico Codificador Orgánico** antes de avanzar hacia embeddings reales o modelos más pesados.

El objetivo es evitar una falsa mejora por complejidad: un modelo futuro solo debería reemplazar al baseline actual si demuestra una ventaja medible frente a las referencias existentes.

## Estado actual

El pipeline compara cuatro roles principales:

| Modelo | Rol operativo | Decisión |
|---|---|---|
| `baseline_v1` | Control explicable | Se mantiene como referencia mínima por transparencia. |
| `baseline_v2` | Variante exploratoria | No queda como candidato principal. |
| `baseline_v3` | Candidato principal pre-embeddings | Se mantiene como baseline fuerte antes de modelos más complejos. |
| `embedding_placeholder` | Contrato vectorial experimental | Valida arquitectura, pero no reemplaza a v3 por empate técnico. |

## Lectura resumida

```text
baseline_v1 = control explicable
baseline_v3 = candidato principal pre-embeddings
embedding_placeholder = contrato vectorial validado
```

## Resultado clave

El `embedding_placeholder` supera marginalmente a `baseline_v3` en evaluación repetida, pero el delta promedio es demasiado pequeño para declararlo superior.

```text
Delta embedding vs v3 = 0.0014
Decisión operativa = empate_tecnico_con_v3
```

Por eso, la lectura prudente es:

> El placeholder valida la arquitectura vectorial, pero no reemplaza a `baseline_v3`.

## Flujo validado

E.C.O. ya puede ejecutar el contrato técnico:

```text
secuencia -> embedding -> clasificador -> comparación -> reporte
```

Esto prepara el terreno para DNABERT u otro modelo real sin romper la trazabilidad del sistema.

## Regla para reemplazar el baseline

Un embedding real o modelo más complejo debería demostrar al menos una de estas mejoras:

1. Mejor macro F1 promedio frente a `baseline_v3`.
2. Menor variabilidad entre splits.
3. Mejor desempeño en casos ambiguos o difíciles.
4. Mejor explicación complementaria sin romper trazabilidad.
5. Reproducibilidad razonable en el equipo o entorno elegido.

## Comandos asociados

```bash
make classifier-compare
make classifier-repeated-eval
make embedding-repeated-eval
make model-decision
make open-model-decision
```

## Límites responsables

- Dataset demostrativo pequeño.
- No es benchmark científico general.
- No hay diagnóstico clínico.
- Las métricas son internas del MVP.
- El embedding placeholder no es DNABERT.
- Cualquier mejora futura debe compararse contra `baseline_v1` y `baseline_v3`.

## Próximo paso lógico

Preparar una ruta experimental de embedding real o semi-real, manteniendo:

```text
baseline_v1 = control explicable
baseline_v3 = candidato principal pre-embeddings
embedding_placeholder = contrato vectorial validado
model_decision = filtro de reemplazo responsable
```
