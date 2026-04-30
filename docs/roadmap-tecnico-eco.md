# Roadmap técnico del Proyecto E.C.O.

## 1. Propósito

Este roadmap ordena la evolución de **E.C.O. — Entérico Codificador Orgánico**. El objetivo es avanzar por capas: primero funcional, luego medible, luego comparable, luego escalable y finalmente publicable.

## 2. Estado actual

E.C.O. ya cuenta con tres rutas funcionales:

| Ruta | Estado | Evidencia |
|---|---|---|
| Regiones y motivos | Funcional | BED/FASTA → motivos → JSON/Markdown. |
| Variantes públicas | Funcional | Registros públicos → categorías E.C.O. → Markdown/HTML/SVG. |
| Clasificación baseline | Funcional + comparativa + evaluación repetida | Dataset auditado → baseline v1/v2 → comparación fija → evaluación repetida Markdown/HTML. |

Estado operativo actual:

```text
make check
→ 34 passed

make portfolio-demo
→ genera reportes Markdown, JSON, HTML y SVG
```

## 3. Principio guía

```text
primero funcional
→ luego medible
→ luego comparable
→ luego repetible
→ luego escalable
→ luego publicable
```

E.C.O. no debería saltar a modelos complejos sin mantener una línea base simple, explicable, comparable y repetible.

## 4. Fase 1: MVP funcional

### Estado

Completado.

### Incluye

- `eco_core` con ingesta, filtrado, absorción, descarte y feedback.
- Conversión BED/FASTA.
- Análisis de motivos simples.
- Interpretación segura de registros públicos.
- Reportes JSON/Markdown/HTML.
- Visualizaciones SVG.
- Demo de portafolio.

### Comandos de validación

```bash
make check
make portfolio-demo
```

## 5. Fase 2: Dataset más amplio

### Estado

Primera ampliación implementada y auditada.

### Avance actual

El dataset etiquetado pasó a una muestra demostrativa más exigente:

```text
Total: 26
Train: 16
Test: 10
Clases: non_regulatory 12 | regulatory 14
```

Incluye casos fáciles y casos ambiguos para que la evaluación no dependa de una muestra demasiado perfecta.

### Auditoría implementada

```bash
make dataset-audit
```

Salidas:

```text
results/eco_dataset_audit_report.json
results/eco_dataset_audit_report.md
```

Resultado actual:

```text
Sin alertas críticas de composición.
```

### Tareas pendientes

- Añadir más secuencias etiquetadas.
- Incluir ejemplos ambiguos adicionales.
- Mantener separación train/test.
- Documentar criterios de selección.
- Evitar vender `accuracy: 1.0` como resultado general.

### Criterio de salida

```text
más ejemplos etiquetados
métricas por clase actualizadas
evaluación repetida más estable
comparación v1/v2 más informativa
```

## 6. Fase 3: Baseline robusto y comparación interna

### Estado

Implementado en primera versión funcional.

### Implementado

- Baseline v1 con `feature_mode=motif`.
- Baseline v2 con `feature_mode=motif_kmer`, `k=2` y `feature_scaling=minmax_train`.
- Normalización min-max ajustada solo con train para evitar fuga de información desde test.
- Auditoría de dataset etiquetado.
- Reportes JSON/Markdown/HTML para v1.
- Reportes JSON/Markdown/HTML para v2.
- Comparación Markdown/HTML v1 vs v2.
- Evaluación repetida v1/v2 con splits estratificados.
- Tests para k-mers, modo v2, normalización y comparación.
- Integración en `make check` y `make portfolio-demo`.

### Comandos

```bash
make dataset-audit
make classifier-baseline
make classifier-baseline-v2
make classifier-compare
make classifier-repeated-eval
make open-classifier-repeated-eval
```

### Lectura con split fijo

```text
baseline_v1 | motif | scaling none | Test macro F1 0.7917
baseline_v2 | motif_kmer | scaling minmax_train | Test macro F1 1.0
```

### Lectura con evaluación repetida

```text
Repeticiones: 10
v1 macro F1 promedio: 0.8134
v2 macro F1 promedio: 0.9087
Delta macro F1 promedio: +0.0952
v2 gana: 7/10
v2 empata: 3/10
v2 pierde: 0/10
```

Interpretación prudente:

> v2 muestra una ventaja promedio y no pierde en la evaluación repetida actual. Esto fortalece la señal inicial, pero todavía corresponde a un dataset demostrativo pequeño.

## 7. Fase 4: Embeddings / DNABERT

### Estado

Pendiente.

### Objetivo

Agregar una ruta experimental con embeddings solo después de tener una línea base más robusta.

### Tareas

- Definir dataset estable.
- Generar embeddings.
- Entrenar clasificador simple sobre embeddings.
- Comparar contra baseline v1/v2.
- Mantener la evaluación repetida como control previo.

## 8. Fase 5: Comparación formal ampliada

### Estado

Parcialmente implementada.

Ya existe:

```text
results/eco_classifier_comparison_report.md
results/eco_classifier_comparison_report.html
results/eco_classifier_repeated_eval_report.md
results/eco_classifier_repeated_eval_report.html
```

La versión completa debería comparar:

| Modelo | Features | Scaling | Evaluación | Accuracy | Macro F1 | Comentario |
|---|---|---|---|---:|---:|---|
| Baseline v1 | motivos + GC | none | split fijo + repetida | x | x | Explicable. |
| Baseline v2 | motivos + k-mers | minmax_train | split fijo + repetida | x | x | Más granular. |
| Embeddings | DNABERT/otro | por definir | split fijo + repetida | x | x | Más complejo. |

## 9. Fase 6: Presentación pública controlada

### Estado

Apta para portafolio y conversaciones laborales. Todavía conviene esperar antes de presentarla como evaluación técnica fuerte en comunidades exigentes.

Antes de publicar en espacios más técnicos, E.C.O. debería tener:

- dataset más amplio;
- comparación v1/v2 repetida con más datos;
- limitaciones explícitas;
- reproducibilidad con comandos simples;
- idealmente una fuente externa o dataset reducido documentado.

## 10. Prioridad recomendada

| Prioridad | Acción | Motivo |
|---|---|---|
| Alta | Ampliar dataset etiquetado a 50-80 secuencias | Verifica si la mejora de v2 se mantiene. |
| Alta | Agregar casos ambiguos controlados | Evita una evaluación demasiado fácil. |
| Alta | Documentar criterios de construcción del dataset | Mejora defendibilidad técnica. |
| Media | Mejorar visualización comparativa repetida | Mejora la lectura UX. |
| Media | Preparar embeddings | Abre camino a DNABERT. |
| Baja por ahora | Publicación técnica exigente | Falta dataset más fuerte. |

## 11. Próximo sprint recomendado

```text
Sprint: dataset v3 + criterios de selección

1. Ampliar examples/eco_labeled_sequences.tsv a 50-80 secuencias.
2. Separar casos fáciles, ambiguos y negativos duros.
3. Crear docs/criterios-dataset-clasificador-eco.md.
4. Repetir dataset-audit, classifier-compare y classifier-repeated-eval.
5. Actualizar resultados de portafolio solo si la señal se mantiene.
```

## 12. Frase guía

> E.C.O. debe avanzar como un sistema medible: cada nueva capa debe demostrar qué mejora, qué limita y contra qué baseline se compara.
