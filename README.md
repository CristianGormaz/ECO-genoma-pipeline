# ECO-genoma-pipeline

![E.C.O. Validation](https://github.com/CristianGormaz/ECO-genoma-pipeline/actions/workflows/eco-validation.yml/badge.svg)

**E.C.O. — Entérico Codificador Orgánico** es un pipeline bioinspirado para procesar datos genómicos como un metabolismo de información: ingesta, filtrado, transformación, absorción, feedback y descarte.

El proyecto trabaja hoy con cuatro rutas principales:

1. **Secuencias/regiones:** BED → FASTA → `eco_core` → análisis de motivos → reporte.
2. **Variantes públicas:** registros estilo ClinVar → clasificación E.C.O. → evidencia → reporte JSON/Markdown/HTML + visualizaciones SVG.
3. **Clasificación baseline:** secuencias etiquetadas → auditoría de dataset → baseline v1/v2/v3 → comparación formal → sensibilidad → evaluación repetida → métricas JSON/Markdown/HTML.
4. **Embeddings experimentales:** secuencias etiquetadas → embedding placeholder → centroides → comparación contra v1/v3 → reporte JSON/Markdown/HTML.

> Uso educativo y bioinformático. No interpreta pacientes ni reemplaza evaluación profesional.

## Idea central

Así como el sistema digestivo transforma alimento en nutrientes útiles, E.C.O. transforma datos genómicos crudos en señales interpretables.

```text
entrada de datos
→ digestión computacional
→ señales útiles
→ reporte interpretable
→ comparación responsable
```

La capa `eco_core.enteric_system` agrega una lectura más fiel al Sistema Nervioso Entérico: sensado local, barrera epitelial informacional, reflejo autónomo, motilidad, absorción, cuarentena, descarte, memoria microbiota mínima y homeostasis del flujo.

```text
dato crudo
→ barrera epitelial
→ sensado entérico
→ reflejo local
→ absorción / cuarentena / descarte
→ memoria microbiota
→ homeostasis
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
39 passed
OK: metabolismo informacional mínimo funcionando.
Estado: OK, intestino informacional demo funcionando.
Estado: OK, pipeline parametrizable E.C.O. funcionando.
Estado: OK, interpretación de variantes generada sin diagnóstico médico.
Estado: OK, auditoría del dataset generada.
Estado: OK, baseline explicable con métricas por clase ejecutado.
Estado: OK, comparación baseline v1/v2/v3 generada.
Estado: OK, ruta experimental de embeddings placeholder generada.
```

## Demo de portafolio

Para preparar una demo completa de presentación:

```bash
make portfolio-demo
```

Este comando ejecuta validaciones locales, genera reportes Markdown/JSON, descarga o reutiliza cache de la muestra ClinVar, crea visualizaciones SVG, exporta informes HTML y agrega evaluación repetida/sensibilidad del clasificador junto a la ruta experimental de embeddings placeholder.

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
results/eco_classifier_baseline_v3_report.md
results/eco_classifier_baseline_v3_report.html
results/eco_classifier_comparison_report.md
results/eco_classifier_comparison_report.html
results/eco_classifier_repeated_eval_report.md
results/eco_classifier_repeated_eval_report.html
results/eco_classifier_sensitivity_report.md
results/eco_classifier_sensitivity_report.html
results/eco_embedding_placeholder_report.md
results/eco_embedding_placeholder_report.html
results/eco_clinvar_sample_report.md
results/eco_clinvar_sample_report.html
results/eco_clinvar_sample_charts/index.html
docs/resumen-ejecutivo-eco.md
docs/ficha-tecnica-clasificador-eco.md
docs/criterios-dataset-clasificador-eco.md
docs/nota-tecnica-v3-vs-v2.md
docs/nota-tecnica-embedding-placeholder.md
docs/caso-estudio-portafolio-eco.md
docs/arquitectura-pipeline-eco.md
docs/roadmap-tecnico-eco.md
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
docs/nota-tecnica-v3-vs-v2.md
```

Para la ruta experimental pre-embeddings:

```text
docs/nota-tecnica-embedding-placeholder.md
```

Para ampliar el dataset etiquetado sin inflar métricas ni perder trazabilidad:

```text
docs/criterios-dataset-clasificador-eco.md
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
make classifier-baseline-v2         # Entrena/evalúa baseline v2 con motivos + k-mers k=2 + minmax_train
make classifier-baseline-v3         # Entrena/evalúa baseline v3 con motivos + k-mers k=3 + minmax_train
make classifier-html                # Convierte el JSON del baseline v1 en HTML estático
make classifier-html-v2             # Convierte el JSON del baseline v2 en HTML estático
make classifier-html-v3             # Convierte el JSON del baseline v3 en HTML estático
make classifier-compare             # Compara baseline v1/v2/v3 en Markdown/HTML
make classifier-repeated-eval       # Repite evaluación v1/v2/v3 con splits estratificados
make classifier-sensitivity         # Diagnostica feature modes, k-mers y normalización
make embedding-placeholder          # Ejecuta ruta experimental de embeddings placeholder
make clinvar-sample                 # Muestra pública real desde ClinVar con reporte E.C.O.
make clinvar-charts                 # Genera visualizaciones SVG desde el JSON ClinVar
make clinvar-html                   # Convierte el reporte JSON de ClinVar en HTML estático integrado
make preview-clinvar                # Vista rápida del Markdown ClinVar en terminal
make inspect-clinvar-json           # Vista rápida del JSON ClinVar formateado
make open-classifier-html           # Abre el HTML del clasificador v1 en navegador
make open-classifier-html-v2        # Abre el HTML del clasificador v2 en navegador
make open-classifier-html-v3        # Abre el HTML del clasificador v3 en navegador
make open-classifier-comparison     # Abre el HTML comparativo v1/v2/v3 en navegador
make open-classifier-repeated-eval  # Abre HTML de evaluación repetida
make open-classifier-sensitivity    # Abre HTML de sensibilidad del clasificador
make open-embedding-placeholder     # Abre HTML de embeddings placeholder
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

### Dataset actual

```text
Total: 60 secuencias
Train: 36
Test: 24
Clases: regulatory y non_regulatory
```

El dataset actual es demostrativo, balanceado y contiene casos fáciles, ambiguos y difíciles. No representa un benchmark científico general.

### Baseline v1: control explicable

```bash
make classifier-baseline
make classifier-html
```

Usa:

```text
motivos + longitud + GC + N + señales simples
feature_scaling = none
Test macro F1 = 0.8333
```

### Baseline v2: variante exploratoria

```bash
make classifier-baseline-v2
make classifier-html-v2
```

Usa:

```text
motivos + longitud + GC + N + frecuencias k-mer de k=2
feature_scaling = minmax_train
Test macro F1 = 0.7333
```

En el dataset actual, v2 queda bajo v1 y no se mantiene como configuración principal.

### Baseline v3: candidato principal pre-embeddings

```bash
make classifier-baseline-v3
make classifier-html-v3
```

Usa:

```text
motivos + longitud + GC + N + frecuencias k-mer de k=3
feature_scaling = minmax_train
Test macro F1 = 0.9161
```

La normalización min-max se ajusta solo con el split de entrenamiento para evitar fuga de información desde prueba.

### Comparación formal v1/v2/v3

```bash
make classifier-compare
make open-classifier-comparison
```

Resultado actual sobre el dataset demostrativo ampliado:

```text
baseline_v1 | motif      | none       | Test macro F1 0.8333
baseline_v2 | motif_kmer | k=2 minmax | Test macro F1 0.7333
baseline_v3 | motif_kmer | k=3 minmax | Test macro F1 0.9161
```

Lectura prudente:

> v3 obtiene el mejor resultado en el split fijo, pero debe contrastarse con evaluación repetida, sensibilidad y futuros datos externos antes de tratarlo como desempeño general.

### Evaluación repetida

```bash
make classifier-repeated-eval
make open-classifier-repeated-eval
```

Salidas:

```text
results/eco_classifier_repeated_eval_report.json
results/eco_classifier_repeated_eval_report.md
results/eco_classifier_repeated_eval_report.html
```

Resultado actual:

```text
v1 macro F1 promedio: 0.7126
v2 macro F1 promedio: 0.6872
v3 macro F1 promedio: 0.7880
Mejor promedio: v3
Delta v3 vs v1: +0.0755
```

### Sensibilidad del clasificador

```bash
make classifier-sensitivity
make open-classifier-sensitivity
```

Objetivo:

```text
diagnosticar si el rendimiento cambia por feature mode, k-mer, normalización o tamaño de k
```

Resultado actual:

```text
Mejor configuración: kmer3_minmax
Delta mejor vs v1: +0.0754
Delta v2 actual vs v1: -0.0254
```

## Ruta 4: embeddings experimentales placeholder

Esta ruta prepara el contrato vectorial antes de incorporar DNABERT u otro modelo real. No descarga modelos pesados ni suma dependencias nuevas al flujo estable.

```bash
make embedding-placeholder
make open-embedding-placeholder
```

Flujo:

```text
examples/eco_labeled_sequences.tsv
→ embedding placeholder determinista
→ normalización minmax_train
→ centroides por clase
→ comparación contra baseline_v1 y baseline_v3
→ JSON/Markdown/HTML
```

Salidas:

```text
results/eco_embedding_placeholder_report.json
results/eco_embedding_placeholder_report.md
results/eco_embedding_placeholder_report.html
```

Lectura prudente:

> La ruta placeholder no busca reemplazar a v3. Su objetivo es dejar lista la arquitectura para que un embedding real pueda compararse de forma honesta contra v1 y v3.

## Decisión técnica actual

```text
v1 = control mínimo explicable
v2 = variante exploratoria no principal
v3 = candidato principal pre-embeddings
embedding-placeholder = contrato experimental para futura ruta DNABERT/embeddings
```

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
scripts/run_eco_classifier_sensitivity.py
scripts/run_eco_classifier_baseline.py
scripts/compare_eco_classifier_baselines.py
scripts/run_eco_embedding_placeholder.py
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
docs/criterios-dataset-clasificador-eco.md
docs/nota-tecnica-v3-vs-v2.md
docs/nota-tecnica-embedding-placeholder.md
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
- v3 es candidato pre-embeddings, no modelo final.
- La ruta de embeddings actual es placeholder; no es DNABERT ni embedding profundo real.
- La evaluación repetida reduce dependencia de un split, pero no reemplaza validación externa.
- La conversión BED → FASTA requiere que BED y FASTA usen el mismo sistema de referencia.
- La analogía con el Sistema Nervioso Entérico es arquitectónica, no biológica literal.
- Los reportes son educativos/bioinformáticos y no deben usarse como conclusión médica personal.

## Próximos pasos

- Mantener v1 como control explicable y v3 como candidato principal pre-embeddings.
- Usar `embedding-placeholder` como contrato técnico antes de integrar modelos reales.
- Comparar cualquier modelo avanzado contra v1 y v3.
- Añadir ejemplos con coordenadas regulatorias reales y muestras reducidas cuando exista una fuente adecuada.
- Agregar visualizaciones y reportes comparativos adicionales.
- Expandir la normalización de variantes y fuentes externas.

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. - Entérico Codificador Orgánico

Actualización asistida por ChatGPT.
