# Ficha técnica del clasificador E.C.O.

## Propósito

Esta ficha documenta el módulo de clasificación baseline de **E.C.O. — Entérico Codificador Orgánico**. Su función es mantener una línea base explicable, medible y repetible antes de incorporar modelos más complejos como embeddings o DNABERT.

## Modelo

```text
centroid_baseline_explicable
centroid_baseline_motif_kmer_minmax
```

El clasificador calcula centroides por clase y predice según distancia euclidiana al centroide más cercano.

## Dataset actual

```text
Archivo: examples/eco_labeled_sequences.tsv
Total: 60 secuencias
Train: 36
Test: 24
Clases: regulatory y non_regulatory
```

El dataset demostrativo actual está balanceado y contiene casos fáciles, ambiguos y difíciles. Sigue siendo pequeño para conclusiones científicas generales, pero ya permite comparar configuraciones internas con más criterio que la muestra inicial.

## Baseline v1 — control explicable

```text
feature_mode = motif
feature_scaling = none
Test accuracy = 0.8333
Test macro F1 = 0.8333
```

v1 usa longitud, GC, N, conteo/densidad de motivos y señales simples. Queda como **control mínimo explicable**.

## Baseline v2 — variante exploratoria

```text
feature_mode = motif_kmer
kmer_k = 2
feature_scaling = minmax_train
Test accuracy = 0.7500
Test macro F1 = 0.7333
```

v2 agrega k-mers de tamaño 2. En el dataset ampliado actual queda bajo v1 y no se mantiene como baseline principal.

## Baseline v3 — candidato principal pre-embeddings

```text
feature_mode = motif_kmer
kmer_k = 3
feature_scaling = minmax_train
Test accuracy = 0.9167
Test macro F1 = 0.9161
```

v3 agrega k-mers de tamaño 3. En el split fijo actual es la mejor configuración y el reporte de sensibilidad también identifica `kmer3_minmax` como mejor promedio.

## Comparación de split fijo

```text
baseline_v1 | motif      | none       | Test macro F1 0.8333
baseline_v2 | motif_kmer | k=2 minmax | Test macro F1 0.7333
baseline_v3 | motif_kmer | k=3 minmax | Test macro F1 0.9161
```

## Evaluación repetida v1/v2/v3

```text
Repeticiones: 10
v1 macro F1 promedio: 0.7126
v2 macro F1 promedio: 0.6872
v3 macro F1 promedio: 0.7880
Mejor promedio: v3
Delta v3 vs v1: +0.0755
```

Lectura prudente:

> v3 aparece como el candidato pre-embeddings más fuerte en la evaluación repetida. Conviene mantener v1 como control explicable y dejar v2 como variante exploratoria.

## Decisión operativa

- `baseline_v1`: control mínimo explicable.
- `baseline_v2`: variante exploratoria no principal.
- `baseline_v3`: candidato principal pre-embeddings.
- `classifier-sensitivity`: control para revisar si k=3 sigue siendo razonable.
- `classifier-repeated-eval`: control para revisar estabilidad entre splits.

## Comandos principales

```bash
make dataset-audit
make classifier-baseline
make classifier-baseline-v2
make classifier-baseline-v3
make classifier-compare
make classifier-repeated-eval
make classifier-sensitivity
make check
```

## Próximo avance técnico

```text
1. Mantener v3 como baseline candidato oficial pre-embeddings.
2. Actualizar README y roadmap con la decisión v1/v2/v3.
3. Preparar una ruta experimental de embeddings solo como comparación futura.
4. Mantener límites explícitos: educativo, bioinformático, no diagnóstico.
```
