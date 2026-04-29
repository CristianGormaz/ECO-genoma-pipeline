# Ejemplo local: coordenadas BED 0-based

Este documento registra una prueba local útil para entender cómo E.C.O. interpreta coordenadas BED.

El objetivo fue procesar una secuencia local con motivos conocidos:

```text
ACGTACGTCCAATTTTTTTTATAAAGGGCGGAATAAA
```

## Secuencia de referencia local

Archivo usado:

```text
data/mi_referencia.fa
```

Contenido:

```fasta
>chrLocal
ACGTACGTCCAATTTTTTTTATAAAGGGCGGAATAAA
```

## Índice base por base

BED usa coordenadas **0-based y semiabiertas**:

```text
start incluido
end excluido
```

Índice de la secuencia:

```text
0  A
1  C
2  G
3  T
4  A
5  C
6  G
7  T
8  C
9  C
10 A
11 A
12 T
13 T
14 T
15 T
16 T
17 T
18 T
19 T
20 A
21 T
22 A
23 A
24 A
25 G
26 G
27 G
28 C
29 G
30 G
31 A
32 A
33 T
34 A
35 A
36 A
```

## BED incorrecto durante la prueba

Una primera versión usó:

```text
chrLocal        8       13      mi_caat 0       +
chrLocal        21      27      mi_tata 0       +
chrLocal        27      33      mi_gc   0       +
```

E.C.O. extrajo:

```fasta
>mi_caat|chrLocal:8-13(+)
CCAAT
>mi_tata|chrLocal:21-27(+)
TAAAGG
>mi_gc|chrLocal:27-33(+)
GCGGAA
```

Resultado:

```text
Motivos encontrados: 1
```

Esto no era un error de E.C.O. El problema estaba en las coordenadas: `mi_tata` y `mi_gc` quedaron desplazados.

## BED corregido

Las coordenadas correctas son:

```text
chrLocal        8       13      mi_caat  0      +
chrLocal        19      25      mi_tata  0      +
chrLocal        25      31      mi_gc    0      +
chrLocal        31      37      mi_polya 0      +
```

Esto extrae:

```fasta
>mi_caat|chrLocal:8-13(+)
CCAAT
>mi_tata|chrLocal:19-25(+)
TATAAA
>mi_gc|chrLocal:25-31(+)
GGGCGG
>mi_polya|chrLocal:31-37(+)
AATAAA
```

## Comando ejecutado

```bash
python3 scripts/run_eco_pipeline.py \
  --bed data/mis_regiones.bed \
  --reference data/mi_referencia.fa \
  --output-dir results \
  --prefix prueba_local_03
```

## Resultado esperado

```text
Regiones procesadas: 4
Motivos encontrados: 5
Aceptados: 4
Rechazados: 0
Absorbidos: 4
Tasa de rechazo: 0.0%
Estado: OK, pipeline parametrizable E.C.O. funcionando.
```

## Por qué aparecen 5 motivos y no 4

Aunque se extrajeron 4 regiones, el total de motivos encontrados fue 5 porque la secuencia:

```text
TATAAA
```

activa dos patrones del analizador:

```text
TATA_box_canonica
TATA_box_degenerada
```

Conteo final:

| Región | Secuencia | Motivos detectados |
| --- | --- | --- |
| `mi_caat` | `CCAAT` | `CAAT_box` |
| `mi_tata` | `TATAAA` | `TATA_box_canonica`, `TATA_box_degenerada` |
| `mi_gc` | `GGGCGG` | `GC_box` |
| `mi_polya` | `AATAAA` | `polyA_signal` |

Total:

```text
1 + 2 + 1 + 1 = 5 motivos
```

## Aprendizaje clave

Cuando una región BED no devuelve el motivo esperado, conviene revisar primero la secuencia extraída:

```bash
cat results/prueba_local_03.fa
```

Si la secuencia extraída no coincide con lo esperado, el problema suele estar en:

- coordenadas desplazadas;
- confusión entre 0-based y 1-based;
- `end` interpretado como incluido cuando en BED es excluido;
- referencia FASTA distinta a la usada para generar el BED.

## Lectura final

Este caso confirma que E.C.O. procesa correctamente archivos propios y que la interpretación precisa de coordenadas BED es una parte crítica del flujo bioinformático.
