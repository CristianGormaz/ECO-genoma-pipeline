# Resumen ejecutivo del Proyecto E.C.O.

## Qué es

**E.C.O. — Entérico Codificador Orgánico** es un pipeline bioinformático bioinspirado que transforma datos genómicos en reportes interpretables. Usa la metáfora del sistema digestivo/entérico como arquitectura funcional: ingesta, filtrado, transformación, absorción, feedback y descarte.

## Problema que aborda

Los datos genómicos pueden ser difíciles de leer cuando aparecen como tablas, coordenadas, secuencias, variantes o métricas aisladas. E.C.O. busca convertir esos datos en una lectura ordenada, trazable y prudente.

## Qué hace actualmente

E.C.O. trabaja con tres rutas principales:

1. **Secuencias y regiones:** convierte coordenadas BED y referencias FASTA en secuencias analizables.
2. **Variantes públicas:** transforma registros estilo ClinVar en reportes JSON/Markdown/HTML con categorías E.C.O.
3. **Clasificación baseline:** compara modelos simples antes de avanzar hacia embeddings tipo DNABERT.

## Resultado técnico actual

El módulo de clasificación compara dos baselines:

| Modelo | Features | Scaling | Lectura |
|---|---|---|---|
| Baseline v1 | motivos + señales simples | none | Línea base explicable. |
| Baseline v2 | motivos + k-mers k=2 | minmax_train | Versión más granular y normalizada. |

Resultado actual del split fijo demostrativo:

```text
v1 Test macro F1: 0.7917
v2 Test macro F1: 1.0
```

La interpretación responsable es que v2 muestra una mejora inicial, pero debe validarse con más datos y evaluación repetida.

## Evidencia generada

El proyecto genera:

```text
results/eco_demo_pipeline_report.md
results/eco_custom_demo_report.md
results/eco_variant_demo_report.md
results/eco_dataset_audit_report.md
results/eco_classifier_baseline_report.md
results/eco_classifier_baseline_v2_report.md
results/eco_classifier_comparison_report.md
results/eco_classifier_repeated_eval_report.md
results/eco_clinvar_sample_report.md
results/eco_clinvar_sample_report.html
results/eco_clinvar_sample_charts/index.html
```

## Comando principal

```bash
make portfolio-demo
```

Este comando prepara una demo revisable con validaciones, reportes, HTML y visualizaciones.

## Límites responsables

E.C.O. no diagnostica, no interpreta pacientes y no calcula riesgo genético personal. Sus reportes son educativos, bioinformáticos e interpretativos. Las métricas actuales corresponden a un dataset demostrativo y no deben presentarse como benchmark científico general.

## Valor profesional

E.C.O. demuestra habilidades en:

- diseño de pipelines modulares;
- IA aplicada con baselines explicables;
- documentación técnica y UX de reportes;
- manejo responsable de datos sensibles;
- comparación incremental de modelos;
- transformación de datos complejos en lectura útil.

## Frase breve para postulación

> Desarrollé E.C.O., un pipeline bioinformático bioinspirado que procesa secuencias, coordenadas genómicas y registros públicos de variantes para generar reportes interpretables en JSON, Markdown, HTML y SVG. El proyecto incorpora validación automatizada, auditoría de dataset, comparación de baselines explicables y límites responsables antes de avanzar hacia modelos de embeddings.
