# Roadmap técnico del Proyecto E.C.O.

## 1. Propósito

Este roadmap ordena la evolución de **E.C.O. — Entérico Codificador Orgánico**. El objetivo es avanzar por capas: primero funcional, luego medible, luego comparable, luego escalable y finalmente publicable.

## 2. Estado actual

E.C.O. ya cuenta con tres rutas funcionales:

| Ruta | Estado | Evidencia |
|---|---|---|
| Regiones y motivos | Funcional | BED/FASTA → motivos → JSON/Markdown. |
| Variantes públicas | Funcional | Registros públicos → categorías E.C.O. → Markdown/HTML/SVG. |
| Clasificación baseline | Funcional + comparativa | Baseline v1 y v2 → comparación Markdown/HTML. |

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
→ luego escalable
→ luego publicable
```

E.C.O. no debería saltar a modelos complejos sin mantener una línea base simple, explicable y comparable.

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

Siguiente foco técnico.

### Objetivo

Ampliar el dataset etiquetado para que la evaluación no dependa de una muestra demasiado pequeña o fácil.

### Tareas

- Añadir más secuencias etiquetadas.
- Incluir ejemplos ambiguos o difíciles.
- Mantener separación train/test.
- Documentar criterios de selección.
- Evitar vender `accuracy: 1.0` como resultado general.

### Criterio de salida

```text
más ejemplos etiquetados
métricas por clase actualizadas
comparación v1/v2 más informativa
```

## 6. Fase 3: Baseline robusto y comparación interna

### Estado

Primera versión implementada.

### Implementado

- Baseline v1 con `feature_mode=motif`.
- Baseline v2 con `feature_mode=motif_kmer` y `k=2`.
- Reportes JSON/Markdown/HTML para v1.
- Reportes JSON/Markdown/HTML para v2.
- Comparación Markdown/HTML v1 vs v2.
- Tests para k-mers, modo v2 y comparación.
- Integración en `make check` y `make portfolio-demo`.

### Comandos

```bash
make classifier-baseline
make classifier-baseline-v2
make classifier-compare
make open-classifier-comparison
```

### Lectura actual

```text
v1 Test macro F1: 1.0
v2 Test macro F1: 1.0
```

Ambos modelos empatan en la muestra actual. Eso valida el flujo, pero todavía no demuestra superioridad de v2.

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

## 8. Fase 5: Comparación formal ampliada

### Estado

Parcialmente implementada.

Ya existe:

```text
results/eco_classifier_comparison_report.md
results/eco_classifier_comparison_report.html
```

La versión completa debería comparar:

| Modelo | Features | Train | Test | Accuracy | Macro F1 | Comentario |
|---|---|---:|---:|---:|---:|---|
| Baseline v1 | motivos + GC | n | n | x | x | Explicable. |
| Baseline v2 | motivos + k-mers | n | n | x | x | Más granular. |
| Embeddings | DNABERT/otro | n | n | x | x | Más complejo. |

## 9. Fase 6: Presentación pública controlada

### Estado

Apta para portafolio y conversaciones laborales. Todavía conviene esperar antes de presentarla como evaluación técnica fuerte en comunidades exigentes.

Antes de publicar en espacios más técnicos, E.C.O. debería tener:

- dataset más amplio;
- comparación v1/v2 con resultados no triviales;
- limitaciones explícitas;
- reproducibilidad con comandos simples.

## 10. Prioridad recomendada

| Prioridad | Acción | Motivo |
|---|---|---|
| Alta | Ampliar dataset etiquetado | Hace más honesta la evaluación. |
| Alta | Agregar casos ambiguos | Permite ver si v2 aporta. |
| Media | Mejorar visualización comparativa | Mejora la lectura UX. |
| Media | Preparar embeddings | Abre camino a DNABERT. |
| Baja por ahora | Publicación técnica exigente | Falta dataset más fuerte. |

## 11. Próximo paso inmediato

```text
ampliar examples/eco_labeled_sequences.tsv con más secuencias etiquetadas y casos ambiguos
```

## 12. Frase guía

> E.C.O. debe avanzar como un sistema medible: cada nueva capa debe demostrar qué mejora, qué limita y contra qué baseline se compara.
