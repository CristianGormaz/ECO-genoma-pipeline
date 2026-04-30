# ECO-genoma-pipeline

![E.C.O. Validation](https://github.com/CristianGormaz/ECO-genoma-pipeline/actions/workflows/eco-validation.yml/badge.svg)

**E.C.O. — Entérico Codificador Orgánico** es un pipeline bioinspirado para procesar datos genómicos como un metabolismo de información: ingesta, filtrado, transformación, absorción, feedback y descarte.

El proyecto trabaja hoy con tres rutas principales:

1. **Secuencias/regiones:** BED → FASTA → `eco_core` → análisis de motivos → reporte.
2. **Variantes públicas:** registros estilo ClinVar → clasificación E.C.O. → evidencia → reporte JSON/Markdown/HTML + visualizaciones SVG.
3. **Clasificación baseline:** secuencias etiquetadas → auditoría de dataset → baseline v1/v2 → comparación formal → evaluación repetida → métricas JSON/Markdown/HTML.

> Uso educativo y bioinformático. No interpreta pacientes ni reemplaza evaluación profesional.

## Idea central

Así como el sistema digestivo transforma alimento en nutrientes útiles, E.C.O. transforma datos genómicos crudos en señales interpretables.

```text
entrada de datos
→ digestión computacional
→ señales útiles
→ reporte interpretable
```

## Quickstart

```bash
git clone https://github.com/CristianGormaz/ECO-genoma-pipeline.git
cd ECO-genoma-pipeline
make install-dev
make check
```

Resultado esperado actual:

```text
34 passed
OK: metabolismo informacional mínimo funcionando.
Estado: OK, intestino informacional demo funcionando.
Estado: OK, pipeline parametrizable E.C.O. funcionando.
Estado: OK, interpretación de variantes generada sin diagnóstico médico.
Estado: OK, auditoría del dataset generada.
Estado: OK, baseline explicable con métricas por clase ejecutado.
Estado: OK, comparación baseline v1/v2 generada.
```

## Demo de portafolio

Para preparar una demo completa de presentación:

```bash
make portfolio-demo
```

Este comando ejecuta validaciones locales, genera reportes Markdown/JSON, descarga o reutiliza cache de la muestra ClinVar, crea visualizaciones SVG, exporta informes HTML y agrega evaluación repetida del clasificador.

Al finalizar, deja rutas listas para revisar:

```text
results/eco_demo_pipeline_report.md
results/eco_custom_demo_report.md
results/eco_variant_demo_report.md
results/eco_dataset_audit_report.md
results/eco_classifier_baseline_report.md
results/eco_classifier_baseline_report.html
results/eco_classifier_baseline_v2_report.md
results/eco_classifier_baseline_v2_report.html
results/eco_classifier_comparison_report.md
results/eco_classifier_comparison_report.html
results/eco_classifier_repeated_eval_report.md
results/eco_classifier_repeated_eval_report.html
results/eco_clinvar_sample_report.md
results/eco_clinvar_sample_report.html
results/eco_clinvar_sample_charts/index.html
docs/resumen-ejecutivo-eco.md
docs/ficha-tecnica-clasificador-eco.md
docs/caso-estudio-portafolio-eco.md
docs/arquitectura-pipeline-eco.md
docs/roadmap-tecnico-eco.md
```

Abrir HTML del clasificador v1:

```bash
make open-classifier-html
```

Abrir HTML del clasificador v2:

```bash
make open-classifier-html-v2
```

Abrir comparación v1/v2:

```bash
make open-classifier-comparison
```

Abrir evaluación repetida:

```bash
make open-classifier-repeated-eval
```

Abrir HTML ClinVar:

```bash
make open-clinvar-html
```

Abrir gráficos ClinVar:

```bash
make open-clinvar-charts
```

## Documentos principales

Para una lectura profesional, breve y orientada a empleabilidad:

```text
docs/resumen-ejecutivo-eco.md
docs/caso-estudio-portafolio-eco.md
```

Para revisión técnica del clasificador:

```text
docs/ficha-tecnica-clasificador-eco.md
```

Para entender E.C.O. como sistema de rutas:

```text
docs/arquitectura-pipeline-eco.md
```

Para ver la evolución recomendada:

```text
docs/roadmap-tecnico-eco.md
```

## Uso responsable de datos públicos

Antes de publicar resultados, compartir capturas o usar datos externos, revisa:

```text
docs/uso-responsable-datos-eco.md
```

Reglas centrales:

- citar ClinVar/NCBI como fuente cuando se usen sus registros;
- no subir bases externas completas al repositorio;
- no subir datos genéticos personales;
- mantener los reportes como bioinformáticos/educativos, no diagnósticos;
- presentar las clasificaciones externas como información reportada por fuentes externas.

## Comandos principales

```bash
make test                           # Ejecuta pytest
make validate                       # Valida ingesta, filtro, absorción, descarte y feedback
make demo                           # Ejecuta BED -> FASTA -> eco_core -> análisis de motivos
make review                         # Revisa el JSON integrado en formato humano
make report                         # Exporta el reporte integrado a Markdown
make pipeline                       # Ejecuta pipeline parametrizable con BED/FASTA
make public-demo                    # Descarga referencia pública pequeña y genera informe
make variant-demo                   # Demo educativa de variantes desde TSV local
make dataset-audit                  # Audita composición del dataset etiquetado
make classifier-baseline            # Entrena/evalúa baseline v1 con features de motivos
make classifier-baseline-v2         # Entrena/evalúa baseline v2 con motivos + k-mers + minmax_train
make classifier-html                # Convierte el JSON del baseline v1 en HTML estático
make classifier-html-v2             # Convierte el JSON del baseline v2 en HTML estático
make classifier-compare             # Compara baseline v1 vs v2 en Markdown/HTML
make classifier-repeated-eval       # Repite evaluación v1/v2 con splits estratificados
make clinvar-sample                 # Muestra pública real desde ClinVar con reporte E.C.O.
make clinvar-charts                 # Genera visualizaciones SVG desde el JSON ClinVar
make clinvar-html                   # Convierte el reporte JSON de ClinVar en HTML estático integrado
make preview-clinvar                # Vista rápida del Markdown ClinVar en terminal
make inspect-clinvar-json           # Vista rápida del JSON ClinVar formateado
make open-classifier-html           # Abre el HTML del clasificador v1 en navegador
make open-classifier-html-v2        # Abre el HTML del clasificador v2 en navegador
make open-classifier-comparison     # Abre el HTML comparativo v1/v2 en navegador
make open-classifier-repeated-eval  # Abre HTML de evaluación repetida
make open-clinvar-html              # Abre el HTML principal en navegador
make open-clinvar-charts            # Abre el índice visual de gráficos SVG
make portfolio-demo                 # Prepara demo completa para portafolio/entrevista
make check                          # Pruebas + demos locales estables
make clean                          # Limpieza de cachés/resultados temporales
```

`make clinvar-sample` y `make portfolio-demo` quedan fuera de `make check` porque dependen de red externa/cache y de un archivo público cambiante.

## Ruta 1: regiones y motivos regulatorios

La demo integrada ejecuta:

```bash
make demo
```

Flujo:

```text
examples/demo_regions.bed
+ examples/tiny_reference.fa
→ results/eco_demo_pipeline.fa
→ results/eco_demo_pipeline_report.json
```

También puedes generar un reporte Markdown:

```bash
make report
```

Salida:

```text
results/eco_demo_pipeline_report.md
```

Motivos incluidos en el MVP:

- TATA box canónica: `TATAAA`
- TATA box degenerada: `TATA[AT][AT]`
- CAAT box: `CCAAT`
- GC box: `GGGCGG`
- Señal de poliadenilación: `AATAAA`
- Repeticiones homopoliméricas largas

## Ruta 2: interpretación segura de variantes públicas

Demo local con archivo pequeño incluido en el repositorio:

```bash
make variant-demo
```

Muestra pública real desde ClinVar:

```bash
make clinvar-sample
make clinvar-charts
make clinvar-html
```

Salidas principales:

```text
results/eco_clinvar_sample.tsv
results/eco_clinvar_sample_report.json
results/eco_clinvar_sample_report.md
results/eco_clinvar_sample_report.html
results/eco_clinvar_sample_charts/index.html
```

El informe incluye resumen por categoría, resumen por gen, matriz gen × categoría, visualizaciones SVG, lectura prudente y detalle por variante.

## Ruta 3: clasificación baseline de secuencias

Antes de incorporar embeddings tipo DNABERT, E.C.O. incluye una línea base simple, medible y auditable.

### Auditoría del dataset

```bash
make dataset-audit
```

Salidas:

```text
results/eco_dataset_audit_report.json
results/eco_dataset_audit_report.md
```

La auditoría revisa tamaño, clases, splits, longitud promedio, GC promedio y motivos detectados.

### Baseline v1: motivos

```bash
make classifier-baseline
make classifier-html
```

Usa:

```text
motivos + longitud + GC + N + señales simples
feature_scaling = none
```

### Baseline v2: motivos + k-mers + normalización

```bash
make classifier-baseline-v2
make classifier-html-v2
```

Usa:

```text
motivos + longitud + GC + N + frecuencias k-mer de k=2
feature_scaling = minmax_train
```

La normalización min-max se ajusta solo con el split de entrenamiento para evitar fuga de información desde prueba.

### Comparación formal v1/v2

```bash
make classifier-compare
```

Resultado actual sobre el dataset demostrativo ampliado:

```text
baseline_v1 | motif | scaling none | Test macro F1 0.7917
baseline_v2 | motif_kmer | scaling minmax_train | Test macro F1 1.0
```

### Evaluación repetida

```bash
make classifier-repeated-eval
```

Salidas:

```text
results/eco_classifier_repeated_eval_report.json
results/eco_classifier_repeated_eval_report.md
results/eco_classifier_repeated_eval_report.html
```

Objetivo:

```text
revisar si v2 mejora de forma estable o solo en un split puntual
```

Lectura prudente:

> En la muestra actual, v2 mejora a v1. Esta mejora es una señal inicial útil, pero debe validarse con un dataset más grande y más variado antes de tratarla como evidencia general.

## Demo pública con descarga real de secuencia

```bash
make public-demo
```

Flujo:

```text
descarga pública chrM.fa.gz
→ descompresión
→ generación BED
→ FASTA
→ eco_core
→ análisis de motivos
→ informe interpretativo
```

## Pipeline parametrizable

Para usar tus propios archivos BED y FASTA:

```bash
python3 scripts/run_eco_pipeline.py \
  --bed data/mis_regiones.bed \
  --reference data/mi_referencia.fa \
  --output-dir results \
  --prefix mi_analisis
```

## Marco conceptual SNE-E.C.O.

Documento principal:

```text
docs/modulo-sne-eco-digestion-bioinspirada.md
```

Define E.C.O. como un **metabolismo de información** inspirado en el Sistema Nervioso Entérico:

```text
dato crudo
→ fragmentación
→ filtro
→ transformación
→ absorción
→ feedback
→ descarte
```

## Estado actual del repositorio

```text
src/eco_motif_analysis.py
src/eco_bed_to_fasta.py
src/eco_variant_interpretation.py
src/eco_sequence_classifier.py
src/eco_core/
scripts/audit_eco_labeled_dataset.py
scripts/run_eco_classifier_repeated_eval.py
scripts/run_eco_classifier_baseline.py
scripts/compare_eco_classifier_baselines.py
scripts/run_eco_validation.py
scripts/run_eco_demo_pipeline.py
scripts/run_eco_pipeline.py
scripts/run_eco_public_chrM_report.py
scripts/run_eco_variant_demo.py
scripts/run_eco_clinvar_sample_report.py
scripts/export_eco_classifier_html.py
scripts/export_eco_clinvar_charts.py
scripts/export_eco_variant_html.py
scripts/review_eco_demo_report.py
scripts/export_eco_demo_markdown.py
tests/
.github/workflows/eco-validation.yml
data/README.md
docs/resumen-ejecutivo-eco.md
docs/ficha-tecnica-clasificador-eco.md
docs/modulo-sne-eco-digestion-bioinspirada.md
docs/arquitectura-pipeline-eco.md
docs/roadmap-tecnico-eco.md
docs/resultado-demostrativo-eco.md
docs/guia-uso-archivos-propios.md
docs/guia-interpretacion-variantes-eco.md
docs/uso-responsable-datos-eco.md
docs/caso-estudio-portafolio-eco.md
docs/ejemplo-local-coordenadas-bed.md
examples/clinvar_style_demo_variants.tsv
examples/eco_labeled_sequences.tsv
Makefile
requirements-dev.txt
```

## Limitaciones

- Proyecto en fase MVP/prototipo.
- El análisis de motivos usa expresiones regulares simples.
- El clasificador baseline usa un dataset demostrativo y no representa desempeño general.
- La mejora actual de v2 sobre v1 es exploratoria y debe validarse con más datos.
- La evaluación repetida reduce dependencia de un split, pero no reemplaza validación externa.
- La conversión BED → FASTA requiere que BED y FASTA usen el mismo sistema de referencia.
- La analogía con el Sistema Nervioso Entérico es arquitectónica, no biológica literal.
- Los reportes son educativos/bioinformáticos y no deben usarse como conclusión médica personal.

## Próximos pasos

- Ampliar el dataset etiquetado para validar si la mejora v2 sobre v1 se mantiene.
- Añadir ejemplos con coordenadas regulatorias reales y muestras reducidas.
- Incorporar embeddings tipo DNABERT cuando exista una línea base más robusta.
- Comparar el baseline explicable contra un modelo con embeddings.
- Agregar visualizaciones y reportes comparativos adicionales.
- Expandir la normalización de variantes y fuentes externas.

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. - Entérico Codificador Orgánico

Actualización asistida por ChatGPT.
