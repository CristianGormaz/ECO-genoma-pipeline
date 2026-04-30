# Roadmap técnico del Proyecto E.C.O.

## 1. Propósito

Este roadmap ordena la evolución de **E.C.O. — Entérico Codificador Orgánico**. El objetivo es avanzar por capas: primero funcional, luego medible, luego comparable, luego repetible, luego escalable y finalmente publicable.

## 2. Estado actual

E.C.O. ya cuenta con tres rutas funcionales:

| Ruta | Estado | Evidencia |
|---|---|---|
| Regiones y motivos | Funcional | BED/FASTA → motivos → JSON/Markdown. |
| Variantes públicas | Funcional | Registros públicos → categorías E.C.O. → Markdown/HTML/SVG. |
| Clasificación baseline | Funcional + comparativa + evaluación repetida | Dataset auditado → baseline v1/v2/v3 → comparación fija → sensibilidad → evaluación repetida Markdown/HTML. |

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
Total: 60
Train: 36
Test: 24
Clases: non_regulatory 30 | regulatory 30
```

Incluye casos fáciles, ambiguos y difíciles para que la evaluación no dependa de una muestra demasiado perfecta.

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

- Añadir más secuencias etiquetadas cuando exista una fuente o criterio más fuerte.
- Incluir negativos duros y regulatorios difíciles adicionales.
- Mantener separación train/test.
- Evitar duplicados exactos o casi idénticos entre train y test.
- Evitar vender `accuracy` o `macro F1` como resultado general.

## 6. Fase 3: Baseline robusto y comparación interna

### Estado

Implementado en versión funcional con tres configuraciones.

### Implementado

- Baseline v1 con `feature_mode=motif` y `feature_scaling=none`.
- Baseline v2 con `feature_mode=motif_kmer`, `k=2` y `feature_scaling=minmax_train`.
- Baseline v3 con `feature_mode=motif_kmer`, `k=3` y `feature_scaling=minmax_train`.
- Normalización min-max ajustada solo con train para evitar fuga de información desde test.
- Auditoría de dataset etiquetado.
- Reportes JSON/Markdown/HTML para v1, v2 y v3.
- Comparación Markdown/HTML v1/v2/v3.
- Evaluación repetida v1/v2/v3 con splits estratificados.
- Sensibilidad de configuraciones para revisar k-mers, normalización y tamaño de k.
- Integración en `make check` y `make portfolio-demo`.

### Comandos

```bash
make dataset-audit
make classifier-baseline
make classifier-baseline-v2
make classifier-baseline-v3
make classifier-compare
make classifier-repeated-eval
make classifier-sensitivity
make open-classifier-repeated-eval
make open-classifier-sensitivity
make open-classifier-comparison
```

### Lectura con split fijo

```text
baseline_v1 | motif      | none       | Test macro F1 0.8333
baseline_v2 | motif_kmer | k=2 minmax | Test macro F1 0.7333
baseline_v3 | motif_kmer | k=3 minmax | Test macro F1 0.9161
```

### Lectura con evaluación repetida

```text
Repeticiones: 10
v1 macro F1 promedio: 0.7126
v2 macro F1 promedio: 0.6872
v3 macro F1 promedio: 0.7880
Delta v3 vs v1 promedio: +0.0755
Mejor promedio: v3
```

Interpretación prudente:

> v3 aparece como el candidato pre-embeddings más fuerte en la evaluación repetida. v1 debe mantenerse como control explicable y v2 como variante exploratoria no principal.

## 7. Decisión técnica actual

| Modelo | Rol operativo | Motivo |
|---|---|---|
| v1 | Control explicable | Simple, transparente y útil como referencia mínima. |
| v2 | Variante exploratoria | k=2 no mejora de forma consistente en el dataset actual. |
| v3 | Candidato principal pre-embeddings | k=3 + minmax_train mejora el split fijo y lidera el promedio repetido. |

## 8. Fase 4: Embeddings / DNABERT

### Estado

Pendiente.

### Objetivo

Agregar una ruta experimental con embeddings solo después de mantener v1/v3 como línea base comparativa.

### Tareas

- Definir dataset estable y congelar una versión demostrativa.
- Generar embeddings o features vectoriales externas.
- Entrenar clasificador simple sobre embeddings.
- Comparar contra v1 y v3.
- Mantener evaluación repetida como control previo.
- Documentar costo, límites y reproducibilidad.

## 9. Fase 5: Comparación formal ampliada

### Estado

Parcialmente implementada.

Ya existe:

```text
results/eco_classifier_comparison_report.md
results/eco_classifier_comparison_report.html
results/eco_classifier_repeated_eval_report.md
results/eco_classifier_repeated_eval_report.html
results/eco_classifier_sensitivity_report.md
results/eco_classifier_sensitivity_report.html
```

La versión completa debería comparar:

| Modelo | Features | Scaling | Evaluación | Macro F1 | Comentario |
|---|---|---|---|---:|---|
| Baseline v1 | motivos + GC | none | split fijo + repetida | x | Control explicable. |
| Baseline v3 | motivos + k-mers k=3 | minmax_train | split fijo + repetida | x | Candidato principal pre-embeddings. |
| Embeddings | DNABERT/otro | por definir | split fijo + repetida | x | Más complejo, solo si aporta valor medible. |

## 10. Fase 6: Presentación pública controlada

### Estado

Apta para portafolio y conversaciones laborales. Todavía conviene esperar antes de presentarla como evaluación técnica fuerte en comunidades exigentes.

Antes de publicar en espacios más técnicos, E.C.O. debería tener:

- dataset más amplio o fuente externa reducida y documentada;
- comparación v1/v3 repetida con más datos;
- limitaciones explícitas;
- reproducibilidad con comandos simples;
- validación externa o benchmark pequeño controlado.

## 11. Próximo sprint recomendado

```text
Sprint: preparación pre-embeddings controlada

1. Congelar v3 como candidato principal pre-embeddings.
2. Actualizar README para que refleje v1/v2/v3 y no solo v1/v2.
3. Crear una nota técnica breve: por qué v3 supera a v2 en esta muestra.
4. Preparar un esqueleto de ruta embeddings sin descargar modelos pesados todavía.
5. Mantener make check estable antes de sumar dependencias nuevas.
```

## 12. Frase guía

> E.C.O. debe avanzar como un sistema medible: cada nueva capa debe demostrar qué mejora, qué limita y contra qué baseline se compara.
