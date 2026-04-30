# Roadmap técnico del Proyecto E.C.O.

## 1. Propósito

Este roadmap define una ruta de evolución para **E.C.O. — Entérico Codificador Orgánico**. Su objetivo es ordenar los próximos avances técnicos sin perder el enfoque responsable del proyecto.

E.C.O. ya cuenta con un MVP funcional. Este documento ayuda a responder:

- qué está listo hoy;
- qué falta para fortalecerlo;
- cuándo conviene mostrarlo en portafolio;
- cuándo conviene discutirlo en comunidades técnicas;
- qué tendría que existir antes de hablar de DNABERT o modelos más avanzados.

## 2. Estado actual

E.C.O. ya tiene tres rutas funcionales:

| Ruta | Estado | Evidencia |
|---|---|---|
| Regiones y motivos | Funcional | BED/FASTA → motivos → JSON/Markdown. |
| Variantes públicas | Funcional | ClinVar → categorías E.C.O. → Markdown/HTML/SVG. |
| Clasificador baseline | Funcional | Features simples → centroides → train/test → métricas por clase. |

Estado operativo actual:

```text
make check
→ 28 passed

make portfolio-demo
→ genera reportes Markdown, JSON, HTML y SVG
```

## 3. Principio guía

El avance de E.C.O. debe ser incremental:

```text
primero funcional
→ luego medible
→ luego comparable
→ luego escalable
→ luego publicable
```

No conviene saltar directo a modelos complejos sin mantener una línea base explicable.

## 4. Fase 1: MVP funcional actual

### Estado

Completado.

### Incluye

- `eco_core` con ingesta, filtrado, absorción, descarte y feedback.
- Conversión BED/FASTA.
- Análisis de motivos simples.
- Interpretación segura de variantes públicas.
- Reportes JSON/Markdown/HTML.
- Visualizaciones SVG.
- Clasificador baseline con split train/test.
- Métricas por clase: precision, recall, F1, support.
- Demo de portafolio con `make portfolio-demo`.

### Criterio de salida

```text
make check
make portfolio-demo
```

Ambos deben ejecutarse sin errores.

## 5. Fase 2: Dataset más amplio y menos artificial

### Objetivo

Reemplazar o complementar el dataset pequeño de demostración por uno más representativo.

### Tareas sugeridas

- Añadir más secuencias etiquetadas.
- Incluir ejemplos difíciles o ambiguos.
- Separar claramente train/test desde el origen.
- Evitar que el dataset sea demasiado fácil.
- Documentar fuente, licencia y criterios de selección.

### Riesgo a evitar

No presentar `accuracy: 1.0` como logro científico si el dataset sigue siendo pequeño y controlado.

### Criterio de salida

```text
baseline ejecutado sobre más ejemplos
métricas por clase generadas
limitaciones explícitas actualizadas
```

## 6. Fase 3: Baseline robusto y comparación interna

### Objetivo

Fortalecer el clasificador explicable antes de incorporar embeddings.

### Tareas sugeridas

- Agregar k-mers simples como features.
- Agregar validación con múltiples splits o holdout fijo documentado.
- Reportar matriz de confusión más informativa.
- Comparar centroides contra reglas simples.
- Crear informe comparativo baseline v1 vs baseline v2.

### Métricas mínimas

- accuracy;
- precision;
- recall;
- F1;
- macro F1;
- weighted F1;
- support por clase.

### Criterio de salida

```text
baseline mejorado supera o iguala al baseline inicial
comparación documentada
HTML/Markdown actualizados
```

## 7. Fase 4: Embeddings tipo DNABERT

### Objetivo

Incorporar una ruta experimental con embeddings de secuencias.

### Tareas sugeridas

- Definir dataset de entrada estable.
- Generar embeddings de secuencias.
- Guardar embeddings como artefactos derivados, no como fuente principal.
- Entrenar un clasificador simple sobre embeddings.
- Comparar contra baseline explicable.

### Riesgo a evitar

No introducir DNABERT solo como etiqueta llamativa. Debe mejorar o complementar algo medible.

### Criterio de salida

```text
embeddings generados
clasificador con embeddings ejecutado
comparación baseline vs embeddings disponible
```

## 8. Fase 5: Comparación formal

### Objetivo

Convertir el proyecto en una evaluación incremental.

### Tabla esperada

| Modelo | Features | Train | Test | Accuracy | Macro F1 | Comentario |
|---|---|---:|---:|---:|---:|---|
| Baseline centroides | motivos + GC | n | n | x | x | Explicable. |
| Baseline k-mers | k-mers + motivos | n | n | x | x | Más granular. |
| Embeddings | DNABERT/otro | n | n | x | x | Más complejo. |

### Criterio de salida

```text
informe comparativo reproducible
comando Makefile dedicado
lectura prudente de resultados
```

## 9. Fase 6: Presentación pública controlada

### Objetivo

Publicar o presentar E.C.O. sin sobredimensionar sus conclusiones.

### Lugares adecuados primero

- LinkedIn personal.
- Portafolio profesional.
- GitHub README.
- Conversaciones de postulación laboral.
- Comunidades de proyectos personales de Python/bioinformática educativa.

### Lugares para después

- r/MachineLearning.
- Foros técnicos de benchmarking.
- Comunidades académicas exigentes.

### Criterio para publicar en espacios más técnicos

Antes de publicar en comunidades exigentes, E.C.O. debería tener:

- dataset más amplio;
- comparación formal;
- baseline claro;
- modelo avanzado opcional;
- limitaciones explícitas;
- reproducibilidad con comandos simples.

## 10. Priorización recomendada

| Prioridad | Acción | Motivo |
|---|---|---|
| Alta | Ampliar dataset etiquetado | Hace más honesta la evaluación. |
| Alta | Agregar comparación baseline v1/v2 | Da lenguaje técnico defendible. |
| Media | Crear informe comparativo HTML | Mejora UX de revisión. |
| Media | Preparar ruta de embeddings | Abre camino a DNABERT. |
| Baja por ahora | Publicar en comunidades exigentes | Todavía falta comparación formal. |

## 11. Próximo paso inmediato

El siguiente avance más razonable es:

```text
crear baseline v2 con features k-mer simples
```

Esto permitiría comparar:

```text
baseline v1: motivos + GC + señales simples
baseline v2: motivos + GC + k-mers
```

Sin depender todavía de modelos pesados.

## 12. Frase guía

> E.C.O. debe avanzar como un sistema medible: cada nueva capa debe demostrar qué mejora, qué limita y contra qué baseline se compara.
