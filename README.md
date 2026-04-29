# ECO-genoma-pipeline

Pipeline bioinspirado para análisis genómico utilizando datos regulatorios, ENCODE, embeddings tipo DNABERT y clasificación automática.

## Idea central

E.C.O. significa **Entérico Codificador Orgánico**. El proyecto nace de una analogía funcional: así como el sistema digestivo recibe alimento, lo procesa y entrega nutrientes útiles al cuerpo, este pipeline recibe datos genómicos, los procesa computacionalmente y entrega señales interpretables sobre regiones regulatorias.

La metáfora operativa es:

1. **Entrada de alimento**: coordenadas genómicas, secuencias FASTA o regiones anotadas.
2. **Digestión**: extracción, limpieza, validación, generación de características y embeddings.
3. **Nutrientes interpretables**: motivos regulatorios, métricas, clasificaciones y reportes.

## Demo rápida / Quickstart

Para clonar, instalar dependencias de desarrollo y validar el prototipo completo:

```bash
git clone https://github.com/CristianGormaz/ECO-genoma-pipeline.git
cd ECO-genoma-pipeline
make install-dev
make check
```

Resultado esperado:

```text
18 passed
OK: metabolismo informacional mínimo funcionando.
Estado: OK, intestino informacional demo funcionando.
OK: el reporte muestra digestión informacional completa y sin rechazos.
Reporte Markdown generado: results/eco_demo_pipeline_report.md
```

Con esto se ejecutan las pruebas automáticas, la validación oficial del metabolismo E.C.O., la demo integrada BED → FASTA → eco_core → análisis de motivos, la revisión humana del JSON y la exportación Markdown del reporte.

## Resultado demostrativo

Puedes revisar una salida demostrativa ya versionada aquí:

```text
docs/resultado-demostrativo-eco.md
```

Este documento muestra el resultado del flujo:

```text
BED → FASTA → eco_core → análisis de motivos → reporte integrado
```

En la demo se procesan 4 regiones, se absorben 4 paquetes, se detectan 4 motivos regulatorios simples y se genera una lectura final sin rechazos. Sirve como vitrina rápida del valor del proyecto antes de ejecutar el código localmente.

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

Este repositorio ya incluye módulos funcionales, una capa técnica base, validación oficial, demo integrada, exportación Markdown, pruebas automáticas y comandos de desarrollo:

```text
src/eco_motif_analysis.py
src/eco_bed_to_fasta.py
src/eco_core/
scripts/run_eco_validation.py
scripts/run_eco_demo_pipeline.py
scripts/review_eco_demo_report.py
scripts/export_eco_demo_markdown.py
tests/
docs/modulo-sne-eco-digestion-bioinspirada.md
docs/resultado-demostrativo-eco.md
Makefile
requirements-dev.txt
```

El primer módulo analiza secuencias FASTA y busca patrones regulatorios clásicos. El segundo módulo convierte coordenadas BED en secuencias FASTA usando un genoma de referencia local. La carpeta `src/eco_core/` transforma la analogía SNE-E.C.O. en módulos técnicos de ingesta, filtrado, absorción, feedback y descarte. La pieza conceptual documenta la arquitectura bioinspirada SNE-E.C.O. y sugiere cómo transformar el proyecto desde un conjunto de scripts hacia un pipeline orgánico, trazable y modular.

## Instalación rápida para desarrollo

Desde una terminal Linux:

```bash
git clone https://github.com/CristianGormaz/ECO-genoma-pipeline.git
cd ECO-genoma-pipeline
make install-dev
```

Esto crea un entorno virtual local en `.venv/`, actualiza `pip` e instala dependencias de desarrollo desde `requirements-dev.txt`.

Si ya tienes el repositorio clonado:

```bash
cd ~/Proyectos/ECO-genoma-pipeline
git pull origin main
make install-dev
```

## Comando único de prueba

Para ejecutar pruebas automáticas, validación oficial, demo integrada, revisión humana y exportación Markdown en una sola orden:

```bash
make check
```

Este comando ejecuta:

```bash
make test
make validate
make demo
make review
make report
```

También puedes correr cada parte por separado:

```bash
make test      # Ejecuta pytest
make validate  # Ejecuta scripts/run_eco_validation.py
make demo      # Ejecuta BED -> FASTA -> eco_core -> análisis de motivos
make review    # Revisa el JSON integrado en formato humano
make report    # Exporta el JSON integrado a Markdown
make clean     # Limpia cachés y resultados temporales de prueba
```

## Demo integrada BED → FASTA → eco_core → análisis de motivos

El repositorio incluye una demo del primer recorrido completo del alimento informacional:

```bash
make demo
```

Equivalente directo:

```bash
python3 scripts/run_eco_demo_pipeline.py
```

La demo usa:

```text
examples/demo_regions.bed
examples/tiny_reference.fa
```

Y genera:

```text
results/eco_demo_pipeline.fa
results/eco_demo_pipeline_report.json
```

Resultado esperado resumido:

```text
E.C.O. DEMO PIPELINE REPORT
Regiones procesadas: 4
Motivos encontrados: 4
Aceptados: 4
Rechazados: 0
Absorbidos: 4
Estado: OK, intestino informacional demo funcionando.
```

## Reporte Markdown para portafolio

Para transformar el JSON integrado en un reporte Markdown legible:

```bash
make report
```

Equivalente directo:

```bash
python3 scripts/export_eco_demo_markdown.py
```

Esto genera:

```text
results/eco_demo_pipeline_report.md
```

El reporte incluye:

- Resumen ejecutivo.
- Entradas y salidas.
- Detalle por región.
- Motivos encontrados.
- Lectura final.
- Nota metodológica.

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

## Validación del metabolismo E.C.O.

El repositorio incluye una validación oficial del metabolismo mínimo E.C.O. Esta prueba ejecuta una secuencia completa y legible:

1. Ingesta de una secuencia válida.
2. Filtrado de calidad.
3. Absorción de features genómicas básicas.
4. Ingesta de una secuencia inválida.
5. Rechazo controlado.
6. Descarte auditable.
7. Feedback final del sistema.

Ejecutar desde la raíz del repositorio:

```bash
make validate
```

Equivalente directo:

```bash
python3 scripts/run_eco_validation.py
```

Resultado esperado resumido:

```text
E.C.O. VALIDATION REPORT
Paquetes procesados: 2
Aceptados: 1
Rechazados: 1
Absorbidos: 1
Tasa de rechazo: 50.0%
Tasa de absorción: 50.0%
OK: metabolismo informacional mínimo funcionando.
```

Esta validación no reemplaza los tests automáticos, pero sirve como demostración UX del flujo SNE-E.C.O.: entrada, filtro, absorción, descarte y retroalimentación. Además, el script oficial está protegido por `pytest` mediante `tests/test_run_eco_validation.py`.

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

- Convertir la demo integrada en un pipeline parametrizable para archivos propios.
- Añadir ejemplos con coordenadas regulatorias reales y muestras reducidas.
- Incorporar embeddings tipo DNABERT.
- Entrenar un clasificador inicial para distinguir regiones regulatorias y no regulatorias.
- Agregar visualizaciones y reportes comparativos.
- Convertir el marco SNE-E.C.O. en módulos técnicos: ingesta, filtro, flujo, absorción, feedback y descarte.

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. - Entérico Codificador Orgánico

Actualización asistida por ChatGPT.
