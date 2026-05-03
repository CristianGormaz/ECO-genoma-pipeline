# ECO-genoma-pipeline

![E.C.O. Validation](https://github.com/CristianGormaz/ECO-genoma-pipeline/actions/workflows/eco-validation.yml/badge.svg)

**E.C.O. — Entérico Codificador Orgánico** es un pipeline bioinspirado para procesar datos genómicos como un metabolismo de información: ingesta, filtrado, transformación, absorción, feedback, descarte, lectura entérica del estado interno y estabilización adaptativa de rutas.

> Uso educativo, bioinformático y experimental. No interpreta pacientes, no entrega diagnósticos, no reemplaza evaluación profesional y no modela conciencia humana.

## Estado actual

La rama **S.N.E.-E.C.O. v1.0** quedó estabilizada y evoluciona como línea **S.N.E.-E.C.O. v1.x** con una suite de regresión:

```text
153 tests passing
Rutas confundidas: 0
Rutas confundidas de recurrencia: 0
Default_state inesperado: eliminado en rutas confundidas
```

Comandos reproducibles:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
make sne-state-confusion
.venv/bin/python scripts/run_sne_eco_recurrence_audit.py
```

También puedes activar el entorno y usar `python` dentro del `.venv`:

```bash
source .venv/bin/activate
python -m pytest -q
```

En Linux Mint u otras distribuciones, si `python` no existe fuera del entorno virtual, usa `python3` o `.venv/bin/python`.

## Idea central

Así como el sistema digestivo transforma alimento en nutrientes útiles, E.C.O. transforma datos crudos en señales interpretables.

```text
entrada de datos
→ digestión computacional
→ señales útiles
→ reporte interpretable
→ comparación responsable
```

La capa `eco_core.enteric_system` agrega una lectura más fiel al Sistema Nervioso Entérico como arquitectura de software: sensado local, barrera epitelial informacional, reflejo autónomo, motilidad, absorción, cuarentena, descarte, memoria microbiota mínima, defensa informacional, homeostasis del flujo y reporte eje intestino-cerebro.

```text
dato crudo
→ barrera epitelial
→ sensado submucoso
→ motilidad mientérica
→ absorción / cuarentena / descarte
→ memoria microbiota
→ defensa informacional
→ homeostasis
→ reporte eje intestino-cerebro
```

## Rutas principales del proyecto

1. **Secuencias/regiones:** BED → FASTA → `eco_core` → análisis de motivos → reporte.
2. **Variantes públicas:** registros estilo ClinVar → clasificación E.C.O. → evidencia → reporte JSON/Markdown/HTML + visualizaciones SVG.
3. **Clasificación baseline:** secuencias etiquetadas → auditoría de dataset → baseline v1/v2/v3 → comparación formal → sensibilidad → evaluación repetida → métricas JSON/Markdown/HTML.
4. **Embeddings experimentales:** secuencias etiquetadas → embedding placeholder/semireal → centroides → comparación contra v1/v3 → reporte JSON/Markdown/HTML.
5. **S.N.E.-E.C.O. v1.0/v1.x:** barrera, sensor submucoso, motilidad mientérica, microbiota, defensa, homeostasis, eje intestino-cerebro, estado adaptativo, auditoría de recurrencia y estabilidad.

## S.N.E.-E.C.O. v1.0 / v1.x

El módulo **S.N.E.-E.C.O. v1.0** convierte la metáfora entérica en arquitectura computacional verificable. La línea **v1.x** mantiene esa base y agrega estabilización adaptativa:

```text
barrier.py                    → mucosa / barrera informacional
sensor_local.py               → plexo submucoso / sensado local
motility.py                   → plexo mientérico / tránsito operativo
microbiota.py                 → memoria adaptativa / recurrencia
defense.py                    → sistema inmune informacional
homeostasis.py                → equilibrio operativo del flujo
gut_brain_axis.py             → reporte comunicable del estado interno
adaptive_state_dataset.py     → filas entrenables de transición de estado
adaptive_state_baseline.py    → baseline jerárquico auditable
adaptive_state_evaluation.py  → evaluación holdout y matriz de confusión
adaptive_state_coverage.py    → diagnóstico de cobertura
adaptive_state_confusion.py   → análisis de rutas confundidas
enteric_system.py             → coordinación de órganos entéricos
```

### Evolución empírica reciente

```text
SNE-03 → variantes dirigidas: rutas confundidas 5 → 2
SNE-04 → baseline jerárquico: elimina default_state prematuro
SNE-05 → proyección homeostática: rutas confundidas 2 → 1
SNE-06 → auditoría de recurrencia: identifica recurrent_valid_d
SNE-07 → recurrence guard: rutas confundidas 1 → 0
SNE-08 → suite de estabilidad: 153 tests, 0 rutas confundidas
SNE-09 → narrativa empírica documentada
```

Documento principal de esta evolución:

```text
docs/sne-eco-empirical-narrative.md
```

Lectura breve:

> E.C.O. funciona como un intestino informacional. No solo revisa si un dato entra o no entra; observa cómo ese dato afecta el equilibrio del sistema. Si el dato es útil, lo absorbe. Si es ambiguo, lo pone en cuarentena. Si es inválido, lo rechaza. Si es repetido, lo reconoce. Y si la repetición no es peligrosa, no sobrerreacciona.

## Quickstart

```bash
git clone https://github.com/CristianGormaz/ECO-genoma-pipeline.git
cd ECO-genoma-pipeline
make install-dev
make check
```

Validación unitaria esperada en la fase S.N.E.-E.C.O. estabilizada:

```text
153 passed
```

Validación rápida del estado adaptativo:

```bash
.venv/bin/python -m pytest -q
make sne-state-confusion
.venv/bin/python scripts/run_sne_eco_recurrence_audit.py
```

Salidas principales:

```text
results/sne_eco_state_confusion_report.md
results/sne_eco_state_confusion_report.json
results/sne_eco_recurrence_audit.md
results/sne_eco_recurrence_audit.json
```

Lectura esperada:

```text
Rutas confundidas: 0
Rutas confundidas de recurrencia: 0
```

## Validaciones S.N.E.-E.C.O.

Validación entérica base:

```bash
make sne-validation
```

Artefactos:

```text
results/sne_eco_validation_report.md
results/sne_eco_validation_report.json
```

Dataset adaptativo:

```bash
make sne-state-dataset
```

Baseline adaptativo:

```bash
make sne-state-baseline
```

Evaluación holdout:

```bash
make sne-state-holdout
```

Cobertura:

```bash
make sne-state-coverage
```

Rutas confundidas:

```bash
make sne-state-confusion
```

Auditoría de recurrencia:

```bash
.venv/bin/python scripts/run_sne_eco_recurrence_audit.py
```

## Demo de portafolio

Para preparar una demo completa de presentación:

```bash
make portfolio-demo
```

Este comando ejecuta validaciones locales, genera reportes Markdown/JSON, descarga o reutiliza cache de la muestra ClinVar, crea visualizaciones SVG, exporta informes HTML, agrega evaluación repetida/sensibilidad del clasificador, ejecuta rutas experimentales de embeddings y genera la validación S.N.E.-E.C.O.

Al finalizar, deja reportes en `results/` y documentos de apoyo en `docs/`.

## Documentos principales

Para lectura rápida de portafolio S.N.E.-E.C.O.:

```text
docs/sne-eco-portfolio-index.md
docs/sne-eco-public-summary.md
docs/case-study-sne-eco-neurogastro-pipeline.md
```

Para una lectura profesional, breve y orientada a empleabilidad:

```text
docs/resumen-ejecutivo-eco.md
docs/caso-estudio-portafolio-eco.md
```

Para entender la evolución empírica S.N.E.-E.C.O.:

```text
docs/sne-eco-empirical-narrative.md
docs/sne-eco-v1-indice-demo.md
docs/guia-validacion-sne-eco.md
docs/guia-dataset-adaptativo-eco.md
docs/guia-baseline-adaptativo-eco.md
docs/guia-evaluacion-holdout-eco.md
docs/guia-diagnostico-cobertura-eco.md
docs/guia-rutas-confundidas-eco.md
docs/guia-trazabilidad-sne-eco.md
```

Para revisión técnica del clasificador:

```text
docs/ficha-tecnica-clasificador-eco.md
docs/nota-tecnica-v3-vs-v2.md
docs/criterios-dataset-clasificador-eco.md
```

Para la ruta experimental de embeddings/router:

```text
docs/nota-tecnica-embedding-placeholder.md
docs/nota-tecnica-embedding-semireal.md
docs/guia-router-adaptativo-eco.md
docs/guia-router-adaptativo-batch-eco.md
```

Para entender E.C.O. como sistema de rutas:

```text
docs/arquitectura-pipeline-eco.md
docs/roadmap-tecnico-eco.md
docs/roadmap-sne-eco-v1-1.md
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
make sne-validation                 # Valida S.N.E.-E.C.O. y exporta Markdown/JSON
make sne-state-dataset              # Genera dataset adaptativo S.N.E.-E.C.O.
make sne-state-baseline             # Genera baseline adaptativo
make sne-state-holdout              # Evalúa holdout adaptativo
make sne-state-coverage             # Diagnostica cobertura adaptativa
make sne-state-confusion            # Analiza rutas confundidas
make enteric-report                 # Reporte entérico interno
make enteric-html                   # Exporta HTML entérico
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
make classifier-compare             # Compara baseline v1/v2/v3 en Markdown/HTML
make classifier-repeated-eval       # Repite evaluación v1/v2/v3 con splits estratificados
make classifier-sensitivity         # Diagnostica feature modes, k-mers y normalización
make embedding-placeholder          # Ejecuta ruta experimental de embeddings placeholder
make embedding-semireal             # Ejecuta ruta experimental de embeddings semireales
make embedding-repeated-eval        # Evaluación repetida de embeddings placeholder
make model-decision                 # Reporte de decisión comparativa de modelos
make adaptive-router-predict-demo   # Demo de router adaptativo para una secuencia
make adaptive-router-batch          # Router adaptativo por lotes
make clinvar-sample                 # Muestra pública real desde ClinVar con reporte E.C.O.
make clinvar-charts                 # Genera visualizaciones SVG desde el JSON ClinVar
make clinvar-html                   # Convierte el reporte JSON de ClinVar en HTML estático integrado
make portfolio-demo                 # Prepara demo completa para portafolio/entrevista
make check                          # Pruebas + demos locales estables
make clean                          # Limpieza de cachés/resultados temporales
```

`make clinvar-sample` queda fuera de `make check` porque depende de red externa/cache y de un archivo público cambiante.

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

### Dataset actual

```text
Total: 60 secuencias
Train: 36
Test: 24
Clases: regulatory y non_regulatory
```

El dataset actual es demostrativo, balanceado y contiene casos fáciles, ambiguos y difíciles. No representa un benchmark científico general.

### Baseline v1/v2/v3

```bash
make dataset-audit
make classifier-baseline
make classifier-baseline-v2
make classifier-baseline-v3
make classifier-compare
```

Resultado resumido sobre el dataset demostrativo ampliado:

```text
baseline_v1 | motif      | none       | Test macro F1 0.8333
baseline_v2 | motif_kmer | k=2 minmax | Test macro F1 0.7333
baseline_v3 | motif_kmer | k=3 minmax | Test macro F1 0.9161
```

Lectura prudente:

> v3 obtiene el mejor resultado en el split fijo, pero debe contrastarse con evaluación repetida, sensibilidad y futuros datos externos antes de tratarlo como desempeño general.

### Evaluación repetida y sensibilidad

```bash
make classifier-repeated-eval
make classifier-sensitivity
```

Resultado actual:

```text
v1 macro F1 promedio: 0.7126
v2 macro F1 promedio: 0.6872
v3 macro F1 promedio: 0.7880
Mejor promedio: v3
Delta v3 vs v1: +0.0755
```

## Ruta 4: embeddings experimentales

Esta ruta prepara el contrato vectorial antes de incorporar DNABERT u otro modelo real. No descarga modelos pesados ni suma dependencias nuevas al flujo estable.

```bash
make embedding-placeholder
make embedding-semireal
make embedding-repeated-eval
make model-decision
```

Lectura prudente:

> La ruta placeholder/semireal no busca reemplazar a v3. Su objetivo es dejar lista la arquitectura para que un embedding real pueda compararse de forma honesta contra v1 y v3.

## Ruta 5: estado adaptativo S.N.E.-E.C.O.

Esta ruta valida el cuerpo entérico adaptativo del pipeline.

```bash
make sne-validation
make sne-state-dataset
make sne-state-baseline
make sne-state-holdout
make sne-state-coverage
make sne-state-confusion
.venv/bin/python scripts/run_sne_eco_recurrence_audit.py
```

Flujo:

```text
lote mínimo de secuencias
→ barrera informacional
→ sensor local submucoso
→ motilidad mientérica
→ defensa informacional
→ microbiota adaptativa
→ homeostasis
→ baseline jerárquico
→ proyección homeostática
→ recurrence guard
→ auditoría de confusión y recurrencia
→ suite de estabilidad
```

Salidas principales:

```text
results/sne_eco_validation_report.md
results/sne_eco_validation_report.json
results/sne_eco_state_dataset.json
results/sne_eco_state_dataset.tsv
results/sne_eco_state_baseline_report.json
results/sne_eco_state_baseline_report.md
results/sne_eco_state_holdout_report.json
results/sne_eco_state_holdout_report.md
results/sne_eco_state_coverage_report.json
results/sne_eco_state_coverage_report.md
results/sne_eco_state_confusion_report.json
results/sne_eco_state_confusion_report.md
results/sne_eco_recurrence_audit.json
results/sne_eco_recurrence_audit.md
```

## Pipeline parametrizable

Para usar tus propios archivos BED y FASTA:

```bash
.venv/bin/python scripts/run_eco_pipeline.py \
  --bed data/mis_regiones.bed \
  --reference data/mi_referencia.fa \
  --output-dir results \
  --prefix mi_analisis
```

## Estado actual del repositorio

```text
src/eco_core/
scripts/
tests/
docs/
examples/
.github/workflows/eco-validation.yml
data/README.md
Makefile
requirements-dev.txt
```

## Limitaciones

- Proyecto en fase MVP/prototipo.
- El análisis de motivos usa expresiones regulares simples.
- El clasificador baseline usa un dataset demostrativo y no representa desempeño general.
- v3 es candidato pre-embeddings, no modelo final.
- Las rutas de embeddings actuales son experimentales; no son DNABERT ni embedding profundo real.
- La evaluación repetida reduce dependencia de un split, pero no reemplaza validación externa.
- La conversión BED → FASTA requiere que BED y FASTA usen el mismo sistema de referencia.
- La analogía con el Sistema Nervioso Entérico es arquitectónica, no biológica literal.
- Los reportes son educativos/bioinformáticos y no deben usarse como conclusión médica personal.

## Próximos pasos

- Mantener v1 como control explicable y v3 como candidato principal pre-embeddings.
- Usar `embedding-placeholder` y `embedding-semireal` como contratos técnicos antes de integrar modelos reales.
- Comparar cualquier modelo avanzado contra v1 y v3.
- Mantener S.N.E.-E.C.O. como módulo de trazabilidad, validación, homeostasis y UX del pipeline.
- Diseñar S.N.E.-E.C.O. v1.1 con lectura por lotes, estados comparativos y dashboard HTML.
- Añadir ejemplos con coordenadas regulatorias reales y muestras reducidas cuando exista una fuente adecuada.
- Agregar visualizaciones y reportes comparativos adicionales.
- Expandir la normalización de variantes y fuentes externas.

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. - Entérico Codificador Orgánico

Actualización asistida por ChatGPT.


## Gobernanza de admisión posterior a RC1

Comando principal:

`make sne-admission-governance`

Este comando ejecuta la cadena completa de gobernanza de admisión S.N.E.-E.C.O. posterior a `sne-eco-v1.0-rc1`: observabilidad, sonda de escenarios externos, revisión de evidencia externa, política de evidencia externa, plan de admisión estable, dry-run de admisión y comparación contra RC1.

Lectura esperada:

- Estado: yellow
- Dataset estable modificado: False
- Baseline modificado: False
- Reglas modificadas: False
- Umbrales modificados: False
- Solo dry-run: True

yellow no representa falla. `yellow` indica que existen observaciones externas retenidas por gobernanza y que ninguna evidencia externa se admite todavía al dataset estable.

Para evaluar rápidamente el proyecto S.N.E.-E.C.O.:
- [Guía rápida de evaluación](docs/sne-eco-quick-evaluation.md)

Para entender el flujo interno de S.N.E.-E.C.O.:
- [Mapa de arquitectura](docs/sne-eco-architecture-map.md)
