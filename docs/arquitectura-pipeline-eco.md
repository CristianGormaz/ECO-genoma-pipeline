# Arquitectura del pipeline E.C.O.

## 1. Propósito del documento

Este documento describe la arquitectura actual del Proyecto **E.C.O. — Entérico Codificador Orgánico** como un sistema de rutas bioinformáticas conectadas por una misma lógica: ingesta, filtrado, transformación, absorción, evaluación, reporte y límites de uso.

La meta es que el proyecto pueda explicarse de forma clara a tres públicos:

- personas técnicas que quieren entender el flujo del código;
- reclutadores o evaluadores que buscan evidencia de habilidades aplicadas;
- usuarios no expertos que necesitan una lectura ordenada y prudente.

## 2. Idea arquitectónica central

E.C.O. funciona como un metabolismo de información.

```text
dato crudo
→ ingesta
→ filtrado
→ transformación
→ extracción de señales
→ evaluación
→ reporte interpretable
→ límites responsables
```

La analogía con el sistema digestivo/entérico se usa como arquitectura funcional, no como afirmación biológica literal. El sistema no “piensa” ni diagnostica: procesa datos y genera lecturas estructuradas.

## 3. Mapa de rutas actuales

| Ruta | Entrada | Proceso | Salida | Propósito |
|---|---|---|---|---|
| Ruta 1: regiones y motivos | BED + FASTA | Conversión BED → FASTA, eco_core, análisis de motivos | JSON/Markdown | Demostrar digestión de secuencias y extracción de señales simples. |
| Ruta 2: variantes públicas | TSV estilo ClinVar | Normalización, categorización E.C.O., evidencia, resumen por gen/categoría | JSON/Markdown/HTML/SVG | Convertir registros públicos de variantes en informe bioinformático prudente. |
| Ruta 3: clasificación baseline | Secuencias etiquetadas | Baseline v1, baseline v2, comparación v1/v2 | JSON/Markdown/HTML | Establecer una línea base medible y comparable antes de embeddings/DNABERT. |
| Ruta futura: embeddings | Secuencias + etiquetas reales | DNABERT/embeddings, clasificador, comparación contra baseline | Métricas comparativas | Evolucionar desde reglas/features simples hacia IA más avanzada. |

## 4. Ruta 1: BED/FASTA → motivos → reporte

### Comandos

```bash
make demo
make report
make pipeline
```

### Flujo

```text
examples/demo_regions.bed
+ examples/tiny_reference.fa
→ extracción FASTA
→ eco_core
→ análisis de motivos
→ reporte integrado
```

### Salidas principales

```text
results/eco_demo_pipeline_report.json
results/eco_demo_pipeline_report.md
results/eco_custom_demo_report.json
results/eco_custom_demo_report.md
```

### Valor arquitectónico

Esta ruta prueba la base digestiva mínima:

- recibe coordenadas;
- extrae secuencias;
- valida paquetes;
- absorbe features;
- detecta motivos;
- genera reporte.

Es la primera demostración del metabolismo E.C.O.

## 5. Ruta 2: ClinVar → interpretación → HTML/SVG

### Comandos

```bash
make clinvar-sample
make clinvar-charts
make clinvar-html
```

### Flujo

```text
ClinVar público/cache local
→ muestra gene-balanced
→ normalización de registros
→ categorización E.C.O.
→ fuerza de evidencia
→ resumen por gen
→ matriz gen × categoría
→ Markdown/JSON/HTML/SVG
```

### Salidas principales

```text
results/eco_clinvar_sample.tsv
results/eco_clinvar_sample_report.json
results/eco_clinvar_sample_report.md
results/eco_clinvar_sample_report.html
results/eco_clinvar_sample_charts/index.html
```

### Categorías E.C.O.

```text
alerta_clinica_alta
incertidumbre_clinica
probablemente_no_patogenica
evidencia_conflictiva
farmacogenomica_o_respuesta_a_farmacos
clasificacion_no_estandarizada
```

### Valor arquitectónico

Esta ruta convierte datos públicos complejos en una lectura de apoyo:

- balancea genes y categorías;
- evita que un solo gen domine la muestra;
- resume evidencia externa;
- declara límites de uso;
- produce una salida visual para portafolio.

No interpreta pacientes. Interpreta registros públicos.

## 6. Ruta 3: clasificación baseline pre-embeddings

### Comandos

```bash
make classifier-baseline
make classifier-baseline-v2
make classifier-compare
make classifier-html
make classifier-html-v2
make open-classifier-comparison
```

### Flujo

```text
examples/eco_labeled_sequences.tsv
→ split train/test
→ baseline v1: motivos + señales simples
→ baseline v2: motivos + k-mers
→ comparación v1/v2
→ métricas por clase
→ JSON/Markdown/HTML
```

### Salidas principales

```text
results/eco_classifier_baseline_report.json
results/eco_classifier_baseline_report.md
results/eco_classifier_baseline_report.html
results/eco_classifier_baseline_v2_report.json
results/eco_classifier_baseline_v2_report.md
results/eco_classifier_baseline_v2_report.html
results/eco_classifier_comparison_report.md
results/eco_classifier_comparison_report.html
```

### Baseline v1

Usa features simples:

| Feature | Lectura |
|---|---|
| length | Longitud de la secuencia. |
| gc_percent | Porcentaje GC. |
| n_percent | Porcentaje de bases ambiguas. |
| motif_count | Cantidad de motivos detectados. |
| motif_density_per_100bp | Densidad de motivos por 100 bp. |
| has_tata | Presencia de TATA box. |
| has_caat | Presencia de CAAT box. |
| has_gc_box | Presencia de GC box. |
| has_polya | Presencia de señal polyA. |
| has_homopolymer | Presencia de homopolímeros largos. |

### Baseline v2

Agrega frecuencias k-mer con `k=2`:

```text
AA, AC, AG, AT, CA, CC, CG, CT, GA, GC, GG, GT, TA, TC, TG, TT
```

### Métricas actuales

Ambos baselines reportan:

- accuracy de entrenamiento;
- accuracy de prueba;
- precision por clase;
- recall por clase;
- F1 por clase;
- support por clase;
- macro average;
- weighted average;
- matriz de confusión;
- predicciones por secuencia;
- distancias a centroides;
- confianza heurística.

### Lectura actual

```text
v1 Test macro F1: 1.0
v2 Test macro F1: 1.0
```

La comparación valida el flujo, pero no demuestra superioridad de v2 porque el dataset actual todavía es pequeño y demostrativo.

### Valor arquitectónico

Esta ruta responde una pregunta clave antes de DNABERT:

> ¿Cuál es la línea base simple y explicable que cualquier modelo avanzado debe superar?

La comparación v1/v2 permite evaluar mejoras incrementales sin saltar directamente a modelos pesados.

## 7. Capa común: eco_core

La carpeta `src/eco_core/` representa la lógica metabólica común:

| Etapa E.C.O. | Rol técnico |
|---|---|
| Ingesta | Recibir paquetes de datos. |
| Filtrado | Validar calidad y detectar problemas. |
| Absorción | Extraer señales útiles. |
| Feedback | Resumir estado del sistema. |
| Descarte | Registrar rechazo o ruido. |

Esta capa permite que el proyecto mantenga coherencia conceptual entre rutas distintas.

## 8. Capa de reportes

E.C.O. no solo procesa datos: también los presenta.

| Formato | Uso |
|---|---|
| JSON | Trazabilidad estructurada y reutilización. |
| Markdown | Lectura técnica rápida y documentación. |
| HTML | Presentación visual para navegador/portafolio. |
| SVG | Visualización simple sin dependencias pesadas. |

Esta capa es importante desde UX conversacional: reduce la fricción entre el dato técnico y la interpretación humana.

## 9. Comando de demostración completa

```bash
make portfolio-demo
```

Este comando ejecuta las rutas principales y deja lista una demo revisable:

```text
results/eco_demo_pipeline_report.md
results/eco_custom_demo_report.md
results/eco_variant_demo_report.md
results/eco_classifier_baseline_report.md
results/eco_classifier_baseline_report.html
results/eco_classifier_baseline_v2_report.md
results/eco_classifier_baseline_v2_report.html
results/eco_classifier_comparison_report.md
results/eco_classifier_comparison_report.html
results/eco_clinvar_sample_report.md
results/eco_clinvar_sample_report.html
results/eco_clinvar_sample_charts/index.html
```

## 10. Control de calidad

El proyecto usa:

```bash
make check
```

Actualmente valida:

- pruebas automáticas con pytest;
- metabolismo mínimo E.C.O.;
- demo BED/FASTA;
- reporte Markdown;
- pipeline parametrizable;
- demo local de variantes;
- baseline v1;
- baseline v2;
- comparación baseline v1/v2.

Estado actual esperado:

```text
34 passed
```

## 11. Límites responsables

E.C.O. mantiene límites explícitos:

- no diagnostica;
- no interpreta pacientes;
- no calcula riesgo genético personal;
- no reemplaza evaluación clínica;
- no presenta el baseline como benchmark científico general;
- no afirma que la analogía entérica sea biología literal;
- no sube bases externas completas ni datos personales al repositorio.

## 12. Ruta futura recomendada

La evolución técnica más natural es:

```text
baseline v1/v2
→ dataset más amplio
→ métricas por clase más robustas
→ embeddings tipo DNABERT
→ comparación baseline vs embeddings
→ clasificador avanzado
→ informe comparativo
```

La pregunta guía será:

> ¿El modelo avanzado supera al baseline explicable de forma medible y justificable?

## 13. Frase corta para explicar la arquitectura

> E.C.O. es un pipeline bioinformático bioinspirado que organiza tres rutas: análisis de secuencias, interpretación prudente de variantes públicas y clasificación baseline pre-embeddings con comparación v1/v2, generando reportes JSON, Markdown, HTML y visualizaciones para transformar datos técnicos en lectura verificable.
