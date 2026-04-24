# ECO-genoma-pipeline

Pipeline bioinspirado para análisis genómico utilizando datos regulatorios, ENCODE, embeddings tipo DNABERT y clasificación automática.

## Idea central

E.C.O. significa **Entérico Codificador Orgánico**. El proyecto nace de una analogía funcional: así como el sistema digestivo recibe alimento, lo procesa y entrega nutrientes útiles al cuerpo, este pipeline recibe datos genómicos, los procesa computacionalmente y entrega señales interpretables sobre regiones regulatorias.

La metáfora operativa es:

1. **Entrada de alimento**: coordenadas genómicas, secuencias FASTA o regiones anotadas.
2. **Digestión**: extracción, limpieza, validación, generación de características y embeddings.
3. **Nutrientes interpretables**: motivos regulatorios, métricas, clasificaciones y reportes.

## Estado actual del repositorio

Este repositorio comenzó con un `README.md` y una licencia MIT. La primera incorporación funcional es el módulo:

```text
src/eco_motif_analysis.py
```

Este script permite analizar secuencias FASTA y buscar patrones regulatorios clásicos.

## Motivos regulatorios incluidos

El módulo detecta:

- **TATA box canónica**: `TATAAA`
- **TATA box degenerada**: `TATA[AT][AT]`
- **CAAT box**: `CCAAT`
- **GC box**: `GGGCGG`
- **Señal de poliadenilación**: `AATAAA`
- **Repeticiones homopoliméricas largas**: `A{6,}`, `T{6,}`, `C{6,}`, `G{6,}`

Además calcula:

- Longitud de la secuencia.
- Porcentaje GC.
- Porcentaje de bases ambiguas `N`.
- Posición de cada motivo en base 1.

## Uso básico

```bash
python src/eco_motif_analysis.py --fasta examples/demo_promoter.fa
```

Guardar reporte JSON:

```bash
python src/eco_motif_analysis.py --fasta examples/demo_promoter.fa --json results/reporte.json
```

Guardar reporte CSV:

```bash
python src/eco_motif_analysis.py --fasta examples/demo_promoter.fa --csv results/reporte.csv
```

Modo estricto, rechazando bases `N`:

```bash
python src/eco_motif_analysis.py --fasta examples/demo_promoter.fa --strict-acgt
```

## Ejemplos incluidos

El repositorio incluye:

```text
examples/demo_promoter.fa
results/demo_report.json
```

El archivo `examples/demo_promoter.fa` contiene secuencias pequeñas de demostración. El archivo `results/demo_report.json` muestra una salida esperada para revisar rápidamente el formato del reporte.

## Ejemplo mínimo de FASTA

```fasta
>ejemplo_promotor
ACGTACGTCCAATTTTTTTTATAAAGGGCGGAATAAA
```

## Limitaciones

Este proyecto se encuentra en fase MVP/prototipo. Actualmente detecta motivos mediante expresiones regulares simples y no reemplaza herramientas bioinformáticas especializadas.

Limitaciones actuales:

- La presencia de un motivo no confirma por sí sola actividad regulatoria real.
- No considera todavía contexto cromatínico, conservación evolutiva, accesibilidad, metilación ni expresión génica.
- No integra aún datos reales de ENCODE, EnhancerAtlas u otras bases externas dentro del flujo automatizado.
- No usa todavía embeddings de DNABERT ni modelos de clasificación MLP en esta primera versión funcional.
- Las posiciones reportadas son relativas a la secuencia entregada, no necesariamente a coordenadas genómicas absolutas.
- Los ejemplos incluidos son pequeños y sirven para validar funcionamiento, no para obtener conclusiones biológicas.

## Próximos pasos

- Integrar datos regulatorios reales en formato BED/FASTA.
- Añadir conversión desde coordenadas BED hacia secuencias FASTA.
- Incorporar embeddings tipo DNABERT.
- Entrenar un clasificador inicial para distinguir regiones regulatorias y no regulatorias.
- Agregar visualizaciones y reportes comparativos.

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. - Entérico Codificador Orgánico

Actualización asistida por ChatGPT.
