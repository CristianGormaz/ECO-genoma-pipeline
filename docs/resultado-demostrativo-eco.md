# Resultado demostrativo E.C.O.

Este documento muestra una salida demostrativa del primer recorrido integrado del sistema E.C.O.:

```text
BED → FASTA → eco_core → análisis de motivos → reporte integrado
```

La demo usa archivos pequeños incluidos en el repositorio. Su objetivo es validar el flujo técnico, la trazabilidad y la presentación del resultado; no busca obtener conclusiones biológicas reales.

## Resumen ejecutivo

| Métrica | Valor |
| --- | --- |
| Regiones procesadas | 4 |
| Motivos encontrados | 4 |
| Paquetes aceptados | 4 |
| Paquetes rechazados | 0 |
| Paquetes absorbidos | 4 |
| Tasa de rechazo | 0.0% |
| Tasa de absorción | 100.0% |

## Entradas y salidas

| Tipo | Ruta |
| --- | --- |
| BED de entrada | `examples/demo_regions.bed` |
| FASTA de referencia | `examples/tiny_reference.fa` |
| FASTA generado | `results/eco_demo_pipeline.fa` |
| JSON integrado | `results/eco_demo_pipeline_report.json` |
| Markdown generado | `results/eco_demo_pipeline_report.md` |

## Detalle por región

| Región | Historial | Longitud | GC | N ambiguas | Motivos |
| --- | --- | --- | --- | --- | --- |
| `caat_box_region\|chrDemo:8-13(+)` | ingestion:ok → filtering:ok → absorption:ok | 5 bp | 40.0% | 0.0% | CAAT_box |
| `tata_box_region\|chrDemo:19-25(+)` | ingestion:ok → filtering:ok → absorption:ok | 6 bp | 0.0% | 0.0% | TATA_box_canonica, TATA_box_degenerada |
| `gc_box_region\|chrDemo:25-31(+)` | ingestion:ok → filtering:ok → absorption:ok | 6 bp | 100.0% | 0.0% | GC_box |
| `reverse_demo\|chrReverse:4-8(-)` | ingestion:ok → filtering:ok → absorption:ok | 4 bp | 100.0% | 0.0% | sin motivos |

## Qué demuestra

Este resultado demuestra que E.C.O. puede:

1. Leer coordenadas genómicas en formato BED.
2. Extraer secuencias desde un FASTA de referencia.
3. Ingerir cada secuencia como paquete trazable dentro de `eco_core`.
4. Filtrar secuencias de ADN.
5. Absorber features básicas como longitud, GC% y N%.
6. Detectar motivos regulatorios simples.
7. Generar un reporte integrado y auditable.
8. Convertir el resultado en una salida legible para humanos.

## Lectura final

**OK: digestión informacional completa y sin rechazos.**

## Nota metodológica

Esta demo usa archivos pequeños incluidos en `examples/`. Sirve para validar el flujo técnico y la trazabilidad del prototipo, no para obtener conclusiones biológicas reales.
