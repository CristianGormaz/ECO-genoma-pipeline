# ECO-genoma-pipeline

Pipeline bioinspirado para análisis genómico utilizando datos regulatorios, ENCODE, embeddings tipo DNABERT y clasificación automática.

## Idea central

E.C.O. significa **Entérico Codificador Orgánico**. El proyecto nace de una analogía funcional: así como el sistema digestivo recibe alimento, lo procesa y entrega nutrientes útiles al cuerpo, este pipeline recibe datos genómicos, los procesa computacionalmente y entrega señales interpretables sobre regiones regulatorias.

La metáfora operativa es:

1. **Entrada de alimento**: coordenadas genómicas, secuencias FASTA o regiones anotadas.
2. **Digestión**: extracción, limpieza, validación, generación de características y embeddings.
3. **Nutrientes interpretables**: motivos regulatorios, métricas, clasificaciones y reportes.

## Marco conceptual SNE-E.C.O.

El proyecto cuenta con una pieza maestra conceptual que conecta el **Sistema Nervioso Entérico (SNE)** con la arquitectura de procesamiento de datos de E.C.O.

Puedes revisarla aquí:

```text
docs/modulo-sne-eco-digestion-bioinspirada.md
```

Esta pieza define a E.C.O. como un **metabolismo de información**: un sistema que recibe datos crudos, los fragmenta, filtra, transforma, absorbe como conocimiento útil y descarta lo que no aporta valor.

En términos simples:

> Así como el intestino convierte alimento en energía disponible para el organismo, E.C.O. convierte datos crudos en conocimiento disponible para la inteligencia del sistema.

## Estado actual del repositorio

Este repositorio ya incluye dos módulos funcionales y una pieza conceptual base:

```text
src/eco_motif_analysis.py
src/eco_bed_to_fasta.py
docs/modulo-sne-eco-digestion-bioinspirada.md
```

El primer módulo analiza secuencias FASTA y busca patrones regulatorios clásicos. El segundo módulo convierte coordenadas BED en secuencias FASTA usando un genoma de referencia local. La pieza conceptual documenta la arquitectura bioinspirada SNE-E.C.O. y sugiere cómo transformar el proyecto desde un conjunto de scripts hacia un pipeline orgánico, trazable y modular.

## Motivos regulatorios incluidos

El módulo `eco_motif_analysis.py` detecta:

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

## Uso básico: análisis de motivos en FASTA

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

## Uso básico: conversión BED → FASTA

```bash
python src/eco_bed_to_fasta.py \
  --bed examples/demo_regions.bed \
  --reference examples/tiny_reference.fa \
  --output results/demo_regions.fa
```

Este paso permite pasar desde coordenadas genómicas a secuencias extraídas. El formato BED se interpreta como coordenadas 0-based y semiabiertas: `start` incluido y `end` excluido.

Ejemplo BED:

```text
chrDemo	8	13	caat_box_region	0	+
chrDemo	19	25	tata_box_region	0	+
chrDemo	25	31	gc_box_region	0	+
chrReverse	4	8	reverse_demo	0	-
```

Salida FASTA esperada:

```fasta
>caat_box_region|chrDemo:8-13(+)
CCAAT
>tata_box_region|chrDemo:19-25(+)
TATAAA
>gc_box_region|chrDemo:25-31(+)
GGGCGG
>reverse_demo|chrReverse:4-8(-)
GGGG
```

## Ejemplos incluidos

El repositorio incluye:

```text
examples/demo_promoter.fa
examples/tiny_reference.fa
examples/demo_regions.bed
results/demo_report.json
results/demo_regions.fa
```

Estos archivos son pequeños y demostrativos. Sirven para probar el funcionamiento del proyecto sin descargar datos externos.

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
- Las posiciones reportadas en el análisis de motivos son relativas a la secuencia entregada.
- La conversión BED → FASTA depende de que el FASTA de referencia y las coordenadas BED usen el mismo sistema de referencia/genome build.
- Los ejemplos incluidos son pequeños y sirven para validar funcionamiento, no para obtener conclusiones biológicas.
- La analogía con el Sistema Nervioso Entérico se usa como inspiración arquitectónica, no como afirmación de que el software sea un organismo vivo o consciente.

## Próximos pasos

- Conectar la salida BED → FASTA con el análisis de motivos.
- Añadir ejemplos con coordenadas regulatorias reales y muestras reducidas.
- Incorporar embeddings tipo DNABERT.
- Entrenar un clasificador inicial para distinguir regiones regulatorias y no regulatorias.
- Agregar visualizaciones y reportes comparativos.
- Convertir el marco SNE-E.C.O. en módulos técnicos: ingesta, filtro, flujo, absorción, feedback y descarte.

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. - Entérico Codificador Orgánico

Actualización asistida por ChatGPT.
