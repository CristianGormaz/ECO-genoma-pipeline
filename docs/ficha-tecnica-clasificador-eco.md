# Ficha tecnica del clasificador E.C.O.

## Proposito

Esta ficha documenta el modulo de clasificacion baseline de E.C.O. Su funcion es mantener una linea base explicable antes de incorporar modelos mas complejos.

## Modelo

```text
centroid_baseline_explicable
centroid_baseline_motif_kmer_minmax
```

El clasificador calcula centroides por clase y predice segun distancia euclidiana al centroide mas cercano.

## Dataset actual

```text
Archivo: examples/eco_labeled_sequences.tsv
Total: 60 secuencias
Train: 36
Test: 24
Clases: regulatory y non_regulatory
```

## Baseline v1

```text
feature_mode = motif
feature_scaling = none
Test accuracy = 0.8333
Test macro F1 = 0.8333
```

v1 usa longitud, GC, N, conteo/densidad de motivos y senales simples.

## Baseline v2

```text
feature_mode = motif_kmer
kmer_k = 2
feature_scaling = minmax_train
Test accuracy = 0.7500
Test macro F1 = 0.7333
```

v2 agrega k-mers de tamano 2. En el dataset ampliado actual queda bajo v1.

## Baseline v3

```text
feature_mode = motif_kmer
kmer_k = 3
feature_scaling = minmax_train
Test accuracy = 0.9167
Test macro F1 = 0.9161
```

v3 agrega k-mers de tamano 3. En el split fijo actual es la mejor configuracion y coincide con el reporte de sensibilidad, donde `kmer3_minmax` aparece como mejor promedio.

## Comparacion resumida

```text
baseline_v1 | motif      | none       | Test macro F1 0.8333
baseline_v2 | motif_kmer | k=2 minmax | Test macro F1 0.7333
baseline_v3 | motif_kmer | k=3 minmax | Test macro F1 0.9161
```

## Decision operativa

- v1 queda como control minimo explicable.
- v2 queda como variante exploratoria no principal.
- v3 queda como candidato principal pre-embeddings.

## Proximo avance tecnico

```text
1. actualizar README y roadmap con v3
2. repetir evaluacion v1/v2/v3
3. mantener sensibilidad como control
4. preparar comparacion futura contra embeddings
```
