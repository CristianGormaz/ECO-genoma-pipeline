# Guía de evaluación holdout E.C.O.

Esta guía explica cómo leer la primera evaluación honesta del baseline adaptativo S.N.E.-E.C.O.

## Por qué existe

El baseline v0 puede alcanzar `accuracy_demo = 1.0` cuando se evalúa sobre las mismas filas usadas para aprender. Eso confirma funcionamiento, pero no generalización.

La evaluación holdout separa filas:

```text
filas pares → entrenamiento
filas impares → prueba
```

Así se observa qué ocurre cuando el baseline encuentra combinaciones no vistas.

## Comando directo

```bash
python scripts/run_sne_eco_state_holdout.py --output-json results/sne_eco_state_holdout_report.json --output-md results/sne_eco_state_holdout_report.md
```

## Artefactos generados

```text
results/sne_eco_state_holdout_report.json
results/sne_eco_state_holdout_report.md
```

## Métricas

```text
accuracy_holdout
macro_f1_holdout
confusion_matrix
predictions
```

## Cómo interpretar resultados bajos

Una métrica baja no significa que E.C.O. falló. Significa que el dataset mínimo todavía no cubre suficientes rutas digestivas para que el baseline generalice.

## Límite responsable

Esta evaluación no representa desempeño general, no modela conciencia humana, no diagnostica y no debe usarse como herramienta clínica o forense. Su función es medir honestamente el comportamiento del baseline sobre transiciones no usadas para entrenamiento.

## Próximo paso recomendado

Si el holdout muestra baja generalización, el siguiente sprint debe ampliar escenarios sintéticos controlados antes de incorporar modelos más complejos.
