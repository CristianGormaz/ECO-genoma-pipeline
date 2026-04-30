# Ficha técnica del clasificador E.C.O.

## Propósito

Esta ficha documenta el módulo de clasificación baseline del Proyecto **E.C.O. — Entérico Codificador Orgánico**. Su función es establecer una línea base explicable antes de incorporar embeddings o modelos más complejos.

## Tipo de modelo

```text
centroid_baseline_explicable
centroid_baseline_motif_kmer_minmax
```

El clasificador calcula centroides por clase y predice según distancia euclidiana al centroide más cercano.

## Dataset

Archivo base:

```text
examples/eco_labeled_sequences.tsv
```

Campos:

| Campo | Descripción |
|---|---|
| sequence_id | Identificador de la secuencia. |
| sequence | Secuencia ADN. |
| label | Clase esperada. |
| split | División train/test. |

Clases actuales:

```text
regulatory
non_regulatory
```

## Baseline v1

Configuración:

```text
feature_mode = motif
feature_scaling = none
```

Features principales:

- longitud;
- porcentaje GC;
- porcentaje N;
- cantidad de motivos;
- densidad de motivos;
- presencia de TATA box;
- presencia de CAAT box;
- presencia de GC box;
- presencia de señal polyA;
- presencia de homopolímeros.

## Baseline v2

Configuración:

```text
feature_mode = motif_kmer
kmer_k = 2
feature_scaling = minmax_train
```

Agrega frecuencias k-mer:

```text
AA, AC, AG, AT, CA, CC, CG, CT, GA, GC, GG, GT, TA, TC, TG, TT
```

La normalización `minmax_train` se ajusta solo usando datos de entrenamiento. Luego se aplica a train y test. Esto evita fuga de información desde test.

## Métricas reportadas

Cada baseline reporta:

- accuracy de entrenamiento;
- accuracy de prueba;
- precision por clase;
- recall por clase;
- F1 por clase;
- macro F1;
- weighted F1;
- matriz de confusión;
- predicciones por secuencia;
- confianza heurística;
- distancias a centroides.

## Resultado demostrativo actual

Split fijo actual:

```text
baseline_v1 | Test macro F1 0.7917
baseline_v2 | Test macro F1 1.0
```

Lectura prudente:

> v2 mejora a v1 en el dataset demostrativo actual, pero esta diferencia debe repetirse con más datos, splits alternativos y evaluación externa antes de tratarla como generalización.

## Evaluación repetida

Comando:

```bash
make classifier-repeated-eval
```

Salida:

```text
results/eco_classifier_repeated_eval_report.json
results/eco_classifier_repeated_eval_report.md
results/eco_classifier_repeated_eval_report.html
```

Objetivo:

```text
revisar si v2 mejora de forma estable o solo en un split puntual
```

## Uso permitido

- Demostración educativa.
- Portafolio técnico.
- Comparación interna de features.
- Línea base antes de DNABERT/embeddings.
- Ejemplo de pipeline explicable.

## Uso no permitido

- Diagnóstico clínico.
- Interpretación de pacientes.
- Cálculo de riesgo genético personal.
- Benchmark científico general.
- Conclusiones médicas o terapéuticas.

## Próximo avance técnico

El paso natural es aumentar el dataset y repetir la comparación:

```text
más secuencias
más casos ambiguos
más splits
comparación v1/v2 repetida
ruta futura hacia embeddings
```
