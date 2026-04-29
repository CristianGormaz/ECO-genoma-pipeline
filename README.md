# ECO-genoma-pipeline

![E.C.O. Validation](https://github.com/CristianGormaz/ECO-genoma-pipeline/actions/workflows/eco-validation.yml/badge.svg)

**E.C.O. — Entérico Codificador Orgánico** es un pipeline bioinspirado para procesar datos genómicos como un metabolismo de información: ingesta, filtrado, transformación, absorción, feedback y descarte.

El proyecto trabaja hoy con dos rutas principales:

1. **Secuencias/regiones:** BED → FASTA → `eco_core` → análisis de motivos → reporte.
2. **Variantes públicas:** registros estilo ClinVar → clasificación E.C.O. → evidencia → reporte JSON/Markdown/HTML + visualizaciones SVG.

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
24 passed
OK: metabolismo informacional mínimo funcionando.
Estado: OK, intestino informacional demo funcionando.
Estado: OK, pipeline parametrizable E.C.O. funcionando.
Estado: OK, interpretación de variantes generada sin diagnóstico médico.
```

## Demo de portafolio

Para preparar una demo completa de presentación:

```bash
make portfolio-demo
```

Este comando ejecuta validaciones locales, genera reportes Markdown/JSON, descarga o reutiliza cache de la muestra ClinVar, crea visualizaciones SVG y exporta el informe HTML integrado.

Al finalizar, deja rutas listas para revisar:

```text
results/eco_demo_pipeline_report.md
results/eco_custom_demo_report.md
results/eco_variant_demo_report.md
results/eco_clinvar_sample_report.md
results/eco_clinvar_sample_report.html
results/eco_clinvar_sample_charts/index.html
docs/caso-estudio-portafolio-eco.md
```

Abrir HTML:

```bash
make open-clinvar-html
```

Abrir gráficos:

```bash
make open-clinvar-charts
```

## Caso de estudio para portafolio

Para una lectura profesional, breve y orientada a empleabilidad, revisa:

```text
docs/caso-estudio-portafolio-eco.md
```

Este documento resume el problema, la solución, la arquitectura, los resultados demostrables, las tecnologías usadas, los límites responsables y frases listas para CV, LinkedIn o entrevista.

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
make test                  # Ejecuta pytest
make validate              # Valida ingesta, filtro, absorción, descarte y feedback
make demo                  # Ejecuta BED -> FASTA -> eco_core -> análisis de motivos
make review                # Revisa el JSON integrado en formato humano
make report                # Exporta el reporte integrado a Markdown
make pipeline              # Ejecuta pipeline parametrizable con BED/FASTA
make public-demo           # Descarga referencia pública pequeña y genera informe
make variant-demo          # Demo educativa de variantes desde TSV local
make clinvar-sample        # Muestra pública real desde ClinVar con reporte E.C.O.
make clinvar-charts        # Genera visualizaciones SVG desde el JSON ClinVar
make clinvar-html          # Convierte el reporte JSON de ClinVar en HTML estático integrado
make preview-clinvar       # Vista rápida del Markdown ClinVar en terminal
make inspect-clinvar-json  # Vista rápida del JSON ClinVar formateado
make open-clinvar-html     # Abre el HTML principal en navegador
make open-clinvar-charts   # Abre el índice visual de gráficos SVG
make portfolio-demo        # Prepara demo completa para portafolio/entrevista
make check                 # Pruebas + demos locales estables
make clean                 # Limpieza de cachés/resultados temporales
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

Entradas/salidas:

```text
examples/clinvar_style_demo_variants.tsv
results/eco_variant_demo_report.json
results/eco_variant_demo_report.md
```

Muestra pública real desde ClinVar:

```bash
make clinvar-sample
```

El comando descarga o reutiliza cache local de:

```text
https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz
```

Por defecto usa una muestra exploratoria `gene-balanced` con:

```text
BRCA1, BRCA2, CFTR, TP53
```

Salidas:

```text
results/eco_clinvar_sample.tsv
results/eco_clinvar_sample_report.json
results/eco_clinvar_sample_report.md
```

Para generar visualizaciones desde el JSON:

```bash
make clinvar-charts
```

Salidas:

```text
results/eco_clinvar_sample_charts/variants_by_gene.svg
results/eco_clinvar_sample_charts/categories.svg
results/eco_clinvar_sample_charts/evidence_strength.svg
results/eco_clinvar_sample_charts/gene_category_matrix.svg
results/eco_clinvar_sample_charts/index.html
```

Para generar una vista HTML estática integrada desde el JSON y los gráficos:

```bash
make clinvar-html
```

Salida:

```text
results/eco_clinvar_sample_report.html
```

Abrir en navegador:

```bash
make open-clinvar-html
make open-clinvar-charts
```

El informe incluye:

- Resumen por categoría.
- Resumen por gen.
- Matriz gen × categoría.
- Visualizaciones SVG integradas.
- Resumen ejecutivo.
- Lectura prudente del conjunto.
- Detalle por variante.
- Límites de uso.

Para leerlo en terminal:

```bash
make preview-clinvar
```

Para inspeccionar el JSON:

```bash
make inspect-clinvar-json
```

Guía completa:

```text
docs/guia-interpretacion-variantes-eco.md
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

Salidas:

```text
data/public/ucsc_hg38_chrM/
results/eco_public_chrM.fa
results/eco_public_chrM_report.json
results/eco_public_chrM_interpretive_report.md
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

Genera:

```text
results/mi_analisis.fa
results/mi_analisis_report.json
results/mi_analisis_report.md
```

Guías útiles:

```text
docs/guia-uso-archivos-propios.md
docs/ejemplo-local-coordenadas-bed.md
data/README.md
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
src/eco_core/
scripts/run_eco_validation.py
scripts/run_eco_demo_pipeline.py
scripts/run_eco_pipeline.py
scripts/run_eco_public_chrM_report.py
scripts/run_eco_variant_demo.py
scripts/run_eco_clinvar_sample_report.py
scripts/export_eco_clinvar_charts.py
scripts/export_eco_variant_html.py
scripts/review_eco_demo_report.py
scripts/export_eco_demo_markdown.py
tests/
.github/workflows/eco-validation.yml
data/README.md
docs/modulo-sne-eco-digestion-bioinspirada.md
docs/resultado-demostrativo-eco.md
docs/guia-uso-archivos-propios.md
docs/guia-interpretacion-variantes-eco.md
docs/uso-responsable-datos-eco.md
docs/caso-estudio-portafolio-eco.md
docs/ejemplo-local-coordenadas-bed.md
examples/clinvar_style_demo_variants.tsv
Makefile
requirements-dev.txt
```

## Validación automática

GitHub Actions ejecuta validación en cada `push` o `pull request` hacia `main`:

```text
.github/workflows/eco-validation.yml
```

Además, `make check` valida localmente las piezas principales del MVP.

## Limitaciones

- Proyecto en fase MVP/prototipo.
- El análisis de motivos usa expresiones regulares simples.
- Los ejemplos incluidos son pequeños y demostrativos.
- La conversión BED → FASTA requiere que BED y FASTA usen el mismo sistema de referencia.
- La ruta de variantes usa registros públicos y metadatos externos.
- La analogía con el Sistema Nervioso Entérico es arquitectónica, no biológica literal.
- Los reportes son educativos/bioinformáticos y no deben usarse como conclusión médica personal.

## Próximos pasos

- Añadir ejemplos con coordenadas regulatorias reales y muestras reducidas.
- Incorporar embeddings tipo DNABERT.
- Entrenar un clasificador inicial para distinguir regiones regulatorias y no regulatorias.
- Agregar visualizaciones y reportes comparativos.
- Expandir la normalización de variantes y fuentes externas.

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. - Entérico Codificador Orgánico

Actualización asistida por ChatGPT.
