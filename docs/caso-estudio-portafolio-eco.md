# Caso de estudio para portafolio: Proyecto E.C.O.

## 1. Resumen ejecutivo

**E.C.O. — Entérico Codificador Orgánico** es un prototipo bioinformático y bioinspirado que transforma datos genómicos en reportes interpretables. El proyecto usa la metáfora del metabolismo: recibir datos crudos, filtrarlos, transformarlos, absorber señales útiles, generar feedback y descartar ruido.

El objetivo del MVP no es diagnosticar ni reemplazar herramientas clínicas, sino demostrar una arquitectura funcional capaz de:

- procesar secuencias y coordenadas genómicas;
- generar reportes trazables;
- interpretar registros públicos de variantes;
- entrenar/evaluar un clasificador baseline explicable;
- producir salidas JSON, Markdown, HTML y visualizaciones;
- mantener límites científicos explícitos.

## 2. Problema abordado

Los datos genómicos suelen ser difíciles de leer para personas no expertas. Un archivo puede contener coordenadas, secuencias, motivos, variantes, clasificaciones externas, estados de revisión y métricas de modelos. Sin una capa interpretativa, esos datos quedan como tablas técnicas poco accionables.

E.C.O. aborda ese problema desde una pregunta práctica:

> ¿Cómo transformar datos genómicos crudos en una lectura organizada, prudente, verificable y entendible?

## 3. Solución propuesta

E.C.O. funciona como un pipeline de digestión informacional:

```text
entrada
→ validación
→ transformación
→ extracción de señales
→ clasificación
→ reporte interpretable
→ límites de uso
```

El sistema tiene tres rutas principales:

### Ruta A: Secuencias y motivos regulatorios

```text
BED → FASTA → eco_core → análisis de motivos → JSON/Markdown
```

Permite convertir coordenadas genómicas en secuencias y buscar motivos simples como TATA box, CAAT box, GC box o señal de poliadenilación.

### Ruta B: Variantes públicas

```text
registros estilo ClinVar → clasificación E.C.O. → evidencia → JSON/Markdown/HTML + visualizaciones
```

Permite descargar o procesar registros públicos de variantes, agruparlos por categorías interpretativas y generar una lectura prudente.

### Ruta C: Clasificador baseline pre-embeddings

```text
secuencias etiquetadas → features explicables → clasificador por centroides → train/test → métricas
```

Esta ruta no pretende ser un modelo final. Funciona como línea base antes de incorporar embeddings tipo DNABERT u otros modelos más complejos.

## 4. Arquitectura funcional

E.C.O. se apoya en una capa modular llamada `eco_core`:

| Módulo | Función |
|---|---|
| Ingesta | Recibe datos crudos. |
| Filtrado | Detecta errores o entradas inválidas. |
| Flujo | Registra historial y trazabilidad. |
| Absorción | Extrae señales útiles. |
| Feedback | Resume estado del proceso. |
| Descarte | Registra entradas rechazadas. |

A esta arquitectura se suman módulos especializados:

| Módulo | Rol |
|---|---|
| `eco_motif_analysis.py` | Detecta motivos simples y calcula features de secuencia. |
| `eco_bed_to_fasta.py` | Convierte coordenadas BED en secuencias FASTA. |
| `eco_variant_interpretation.py` | Organiza variantes en categorías E.C.O. y estima fuerza de evidencia. |
| `eco_sequence_classifier.py` | Entrena/evalúa un baseline explicable con centroides de features. |

Esta estructura permite explicar el sistema como un metabolismo de información, no solo como una colección de scripts.

## 5. Resultados demostrables

### Validación local

El comando principal de validación es:

```bash
make check
```

Resultado actual esperado:

```text
26 passed
```

Además ejecuta validación del metabolismo mínimo, demo integrada, revisión de reporte, exportación Markdown, pipeline parametrizable, demo local de variantes y clasificador baseline.

### Demo de regiones

```bash
make demo
make report
```

Genera:

```text
results/eco_demo_pipeline_report.md
```

El reporte muestra regiones procesadas, motivos encontrados, aceptación/rechazo y lectura final.

### Muestra pública de variantes

```bash
make clinvar-sample
make clinvar-charts
make clinvar-html
```

Genera:

```text
results/eco_clinvar_sample.tsv
results/eco_clinvar_sample_report.json
results/eco_clinvar_sample_report.md
results/eco_clinvar_sample_report.html
results/eco_clinvar_sample_charts/index.html
```

El informe incluye:

- resumen por categoría;
- resumen por gen;
- matriz gen × categoría;
- visualizaciones SVG;
- resumen ejecutivo;
- lectura prudente;
- detalle por variante;
- límites de uso.

Ejemplo de matriz balanceada:

```text
BRCA1 | 5 variantes
BRCA2 | 5 variantes
CFTR  | 5 variantes
TP53  | 5 variantes
```

### Clasificador baseline explicable

```bash
make classifier-baseline
```

Genera:

```text
results/eco_classifier_baseline_report.json
results/eco_classifier_baseline_report.md
```

Estado actual de la demo:

```text
Train: 6 | Test: 4
Train accuracy: 1.0
Test accuracy: 1.0
```

Lectura prudente:

> Este resultado demuestra que el flujo técnico de entrenamiento/evaluación funciona sobre un dataset pequeño y controlado. No debe presentarse como desempeño científico general.

## 6. Criterios de calidad aplicados

El proyecto incorpora prácticas técnicas útiles para un MVP serio:

- pruebas automáticas con `pytest`;
- validación local con `make check`;
- workflow de GitHub Actions;
- separación entre código, ejemplos, datos locales, documentación y resultados;
- cache local para datos públicos descargados;
- deduplicación de variantes;
- muestreo balanceado por gen y categoría;
- separación explícita train/test para el baseline;
- matriz de confusión y métricas de prueba;
- reportes Markdown para lectura humana;
- HTML estático para demostración visual;
- JSON para trazabilidad estructurada;
- límites explícitos de interpretación.

## 7. Límites responsables

E.C.O. mantiene límites claros:

- no interpreta pacientes;
- no diagnostica;
- no calcula riesgo personal absoluto;
- no reemplaza evaluación profesional;
- no convierte una variante pública en conclusión médica individual;
- no presenta el baseline como modelo científico final;
- usa ejemplos pequeños o muestras exploratorias para demostrar funcionamiento.

Estos límites no debilitan el proyecto; lo hacen más responsable y defendible.

## 8. Valor profesional demostrado

Este proyecto demuestra habilidades transferibles a roles de calidad, experiencia de usuario, datos e IA aplicada:

- diseño de sistemas modulares;
- pensamiento bioinspirado aplicado a software;
- documentación técnica clara;
- diseño de reportes interpretativos;
- validación automatizada;
- manejo prudente de información sensible;
- traducción de datos complejos a lenguaje entendible;
- creación de baseline medible antes de modelos avanzados;
- criterio para separar demostración técnica de conclusión clínica o científica.

## 9. Tecnologías y conceptos utilizados

- Python.
- Pytest.
- Makefile.
- GitHub Actions.
- JSON/Markdown/HTML.
- SVG básico.
- FASTA/BED.
- Registros estilo ClinVar.
- Arquitectura modular.
- Clasificador por centroides.
- Features explicables.
- Matriz de confusión.
- Reportes interpretativos.
- Bioinformática educativa.

## 10. Frase breve para CV o LinkedIn

> Desarrollé E.C.O., un pipeline bioinformático bioinspirado que convierte secuencias, coordenadas genómicas y registros públicos de variantes en reportes JSON/Markdown/HTML interpretables, incorporando validación automatizada, trazabilidad, visualizaciones y un clasificador baseline con separación train/test.

## 11. Frase breve para entrevista

> E.C.O. nació como una metáfora del sistema digestivo aplicada a datos. Lo convertí en un prototipo funcional que ingiere datos genómicos, los filtra, extrae señales, organiza evidencia, genera reportes entendibles y evalúa un baseline explicable antes de pasar a modelos más complejos como DNABERT.

## 12. Próximo avance sugerido

El siguiente paso para fortalecer el proyecto técnicamente es aumentar la seriedad del baseline:

- ampliar el dataset etiquetado;
- agregar secuencias difíciles o ambiguas;
- reportar métricas por clase;
- comparar baseline explicable contra embeddings;
- preparar una futura ruta DNABERT/MLP.

Eso permitiría mostrar E.C.O. no solo como experiencia de lectura, sino como pipeline con evaluación incremental de modelos.
