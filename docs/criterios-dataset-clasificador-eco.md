# Criterios para ampliar el dataset del clasificador E.C.O.

## 1. Propósito

Este documento define criterios para ampliar `examples/eco_labeled_sequences.tsv` sin perder trazabilidad, prudencia ni valor técnico.

El objetivo no es fabricar un dataset perfecto. El objetivo es construir una muestra demostrativa más exigente para probar si el baseline v2 mantiene ventaja frente a v1.

## 2. Estado actual

Dataset v3 implementado:

```text
Total: 60 secuencias
regulatory: 30
non_regulatory: 30
train: 36
test: 24
```

Distribución conceptual aplicada:

```text
regulatory easy
regulatory ambiguous
regulatory hard
non_regulatory easy
non_regulatory ambiguous
non_regulatory hard
```

Lectura prudente:

> Dataset v3 amplía la dificultad y mejora la trazabilidad del clasificador. El siguiente control real es ejecutar auditoría, comparación v1/v2 y evaluación repetida para revisar si la ventaja de v2 se mantiene.

## 3. Principios de construcción

### 3.1. Trazabilidad

Cada secuencia debe tener un identificador claro.

Formato usado:

```text
reg_train_easy_01
reg_train_amb_01
reg_train_hard_01
reg_test_easy_01
reg_test_amb_01
reg_test_hard_01
nonreg_train_easy_01
nonreg_train_amb_01
nonreg_train_hard_01
nonreg_test_easy_01
nonreg_test_amb_01
nonreg_test_hard_01
```

### 3.2. Separación explícita train/test

El campo `split` debe ser definido manualmente como:

```text
train
test
```

No mezclar versiones casi idénticas de una misma secuencia entre train y test.

### 3.3. Balance razonable

Mantener proporciones cercanas entre clases:

```text
regulatory: 50% aproximado
non_regulatory: 50% aproximado
```

Dataset v3 usa balance exacto:

```text
regulatory: 30
non_regulatory: 30
```

### 3.4. Dificultad gradual

Cada clase debe contener tres tipos de casos:

| Tipo | Descripción | Uso |
|---|---|---|
| easy | Casos claros y esperables. | Validar funcionamiento básico. |
| ambiguous | Casos con señales parciales o débiles. | Medir sensibilidad del modelo. |
| hard | Casos diseñados para confundir. | Evaluar robustez real. |

## 4. Casos regulatorios sugeridos

### 4.1. Regulatory easy

Secuencias con varios motivos claros:

```text
TATAAA
CCAAT
GGGCGG
AATAAA
```

Uso: confirmar que el modelo detecta regiones con señales regulatorias evidentes.

### 4.2. Regulatory ambiguous

Secuencias con solo uno o dos motivos, o motivos degenerados.

Ejemplos conceptuales:

```text
solo CAAT_box
solo TATA degenerada
GC alto con una señal débil
polyA sin otros motivos
```

Uso: probar si v2 aprovecha composición k-mer además de motivos explícitos.

### 4.3. Regulatory hard

Secuencias regulatorias con señales menos obvias.

Ejemplos conceptuales:

```text
motivos separados por regiones neutras
señales débiles con GC extremo
motivos parcialmente solapados
secuencias cortas con una señal relevante
```

Uso: evitar que el clasificador aprenda solo “más motivos = regulatory”.

## 5. Casos no regulatorios sugeridos

### 5.1. Non-regulatory easy

Secuencias sin motivos detectables y composición balanceada.

Uso: validar que el modelo no marca todo como regulatory.

### 5.2. Non-regulatory ambiguous

Secuencias no regulatorias con composición parecida a regulatory, pero sin motivos funcionales claros.

Ejemplos conceptuales:

```text
GC alto sin GC_box real
AT alto sin TATAAA real
repeticiones simples sin señal regulatoria
```

Uso: probar si el modelo sobrerreacciona a composición.

### 5.3. Non-regulatory hard

Secuencias no regulatorias que contienen señales parecidas a motivos.

Ejemplos conceptuales:

```text
casi TATAAA, pero no exacta
casi CCAAT, pero alterada
segmentos con G/C altos sin patrón GGGCGG
```

Uso: medir falsos positivos.

## 6. Columnas requeridas

El dataset debe mantener columnas compatibles con el código actual:

```text
sequence_id	sequence	label	split
```

Valores permitidos para `label`:

```text
regulatory
non_regulatory
```

Valores permitidos para `split`:

```text
train
test
```

## 7. Tamaño recomendado para dataset v3

Meta inicial definida:

```text
50 a 80 secuencias
```

Dataset v3 actual:

| Grupo | Train | Test | Total |
|---|---:|---:|---:|
| regulatory easy | 6 | 4 | 10 |
| regulatory ambiguous | 6 | 4 | 10 |
| regulatory hard | 6 | 4 | 10 |
| non_regulatory easy | 6 | 4 | 10 |
| non_regulatory ambiguous | 6 | 4 | 10 |
| non_regulatory hard | 6 | 4 | 10 |

Total:

```text
train: 36
test: 24
total: 60
```

## 8. Reglas para evitar métricas infladas

- No duplicar secuencias exactas entre train y test.
- No usar patrones demasiado obvios en todos los casos regulatory.
- No dejar todos los non_regulatory sin motivos; incluir negativos difíciles.
- No cambiar el test para mejorar el resultado después de mirar las métricas.
- No presentar accuracy alta como conclusión general.
- Registrar cuándo un caso fue creado como `easy`, `ambiguous` o `hard` en el ID.

## 9. Comandos de control después de ampliar

Después de modificar `examples/eco_labeled_sequences.tsv`, ejecutar:

```bash
make dataset-audit
make classifier-baseline
make classifier-baseline-v2
make classifier-compare
make classifier-repeated-eval
make check
```

Revisar:

```bash
sed -n '1,180p' results/eco_dataset_audit_report.md
sed -n '1,180p' results/eco_classifier_comparison_report.md
sed -n '1,180p' results/eco_classifier_repeated_eval_report.md
```

## 10. Criterio de avance

Se considera que dataset v3 fortalece E.C.O. si:

```text
1. La auditoría no muestra alertas críticas.
2. v2 mantiene ventaja promedio o al menos no cae frente a v1.
3. Las métricas bajan de forma razonable si el dataset se vuelve más difícil.
4. La lectura del reporte sigue siendo clara y prudente.
```

## 11. Lectura E.C.O.

Ampliar el dataset equivale a darle al sistema alimento más complejo.

Un pipeline bioinspirado no se valida solo con comida fácil. Debe demostrar que puede procesar señales claras, ruido, ambigüedad y casos que obligan a diferenciar entre apariencia y función.
