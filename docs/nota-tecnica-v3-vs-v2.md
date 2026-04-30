# Nota técnica: por qué v3 supera a v2 en la muestra actual

## Propósito

Esta nota explica la decisión de mantener `baseline_v3` como candidato principal pre-embeddings dentro del clasificador E.C.O.

No busca declarar un benchmark científico general. Su función es documentar una decisión interna de arquitectura: qué configuración simple conviene usar como referencia antes de comparar contra embeddings o modelos más complejos.

## Contexto

El dataset demostrativo actual tiene:

```text
Total: 60 secuencias
Train: 36
Test: 24
Clases: regulatory y non_regulatory
```

El flujo actual compara tres configuraciones:

| Modelo | Feature mode | k | Scaling | Rol |
|---|---|---:|---|---|
| v1 | motif | no aplica | none | Control explicable. |
| v2 | motif_kmer | 2 | minmax_train | Variante exploratoria. |
| v3 | motif_kmer | 3 | minmax_train | Candidato principal pre-embeddings. |

## Resultado de split fijo

```text
baseline_v1 | Test macro F1 0.8333
baseline_v2 | Test macro F1 0.7333
baseline_v3 | Test macro F1 0.9161
```

En el split fijo actual, v3 obtiene el mejor macro F1 de prueba.

## Resultado de evaluación repetida

```text
Repeticiones: 10
v1 macro F1 promedio: 0.7126
v2 macro F1 promedio: 0.6872
v3 macro F1 promedio: 0.7880
Delta v3 vs v1: +0.0755
Mejor promedio: v3
```

La evaluación repetida reduce la dependencia de un solo split. En este control, v3 también aparece como la configuración más fuerte.

## Resultado de sensibilidad

```text
Mejor configuración: kmer3_minmax
Delta mejor vs v1: +0.0754
Delta v2 actual vs v1: -0.0254
```

La sensibilidad confirma que `k=3` con `minmax_train` funciona mejor que `k=2` en la muestra actual.

## Interpretación técnica

La hipótesis operativa es:

```text
k=2 captura composición muy corta.
k=3 captura patrones locales un poco más informativos.
```

En este dataset, k=3 parece representar mejor diferencias de composición entre secuencias regulatorias y no regulatorias difíciles, sin saltar todavía a embeddings profundos.

## Decisión E.C.O.

```text
v1 = control mínimo explicable
v2 = variante exploratoria no principal
v3 = candidato principal pre-embeddings
```

## Límites

- Dataset demostrativo, no benchmark científico.
- Métricas internas, no validación externa.
- v3 no es modelo final.
- k-mers simples no reemplazan embeddings ni modelos profundos.
- No hay interpretación clínica ni diagnóstico.

## Próximo paso lógico

Preparar una ruta experimental de embeddings que se compare contra:

```text
baseline_v1: control explicable
baseline_v3: mejor candidato pre-embeddings
```

Cualquier modelo avanzado debe demostrar qué mejora frente a esas dos referencias.
