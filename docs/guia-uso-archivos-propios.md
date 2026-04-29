# Guía de uso con archivos propios

Esta guía explica cómo ejecutar E.C.O. con un archivo BED propio y un FASTA de referencia propio.

El flujo ejecutado es:

```text
BED propio → FASTA extraído → eco_core → análisis de motivos → JSON → Markdown
```

## Requisitos de entrada

Necesitas dos archivos compatibles entre sí:

1. Un archivo BED con coordenadas genómicas.
2. Un archivo FASTA de referencia que contenga los cromosomas o contigs mencionados en el BED.

La regla clave:

> El BED y el FASTA deben usar el mismo sistema de referencia.

Por ejemplo, si tus coordenadas BED vienen de `hg19`, el FASTA de referencia también debe ser `hg19`. Si vienen de `hg38`, el FASTA debe ser `hg38`.

## Formato BED esperado

E.C.O. acepta BED3, BED4, BED5 y BED6.

Ejemplo mínimo BED3:

```text
chr1	100	150
chr1	200	260
```

Ejemplo recomendado BED6:

```text
chr1	100	150	region_promotora_1	0	+
chr1	200	260	region_promotora_2	0	-
```

Columnas:

| Columna | Nombre | Descripción |
| --- | --- | --- |
| 1 | chrom | Cromosoma o contig. Debe existir en el FASTA. |
| 2 | start | Inicio 0-based. Incluido. |
| 3 | end | Fin 0-based. Excluido. |
| 4 | name | Nombre de la región. Opcional, pero recomendado. |
| 5 | score | Puntaje. Opcional. |
| 6 | strand | Hebra: `+`, `-` o `.`. Opcional. |

## Coordenadas BED

BED usa coordenadas:

```text
0-based y semiabiertas
```

Esto significa:

```text
start incluido
end excluido
```

Ejemplo:

```text
chr1  0  4
```

Extrae las bases en posiciones 0, 1, 2 y 3. No incluye la posición 4.

## Formato FASTA esperado

Ejemplo:

```fasta
>chr1
ACGTACGTACGTACGTACGT
>chr2
TTTTCCCCAAAAGGGG
```

Los nombres después de `>` deben coincidir con la columna `chrom` del BED.

Si el BED usa:

```text
chr1
```

El FASTA debe tener:

```fasta
>chr1
```

No sirve si el FASTA usa otro nombre como:

```fasta
>1
```

En ese caso, debes armonizar nombres antes de ejecutar E.C.O.

## Comando de ejecución

Desde la raíz del repositorio:

```bash
python3 scripts/run_eco_pipeline.py \
  --bed data/mis_regiones.bed \
  --reference data/mi_referencia.fa \
  --output-dir results \
  --prefix experimento_01
```

Esto genera:

```text
results/experimento_01.fa
results/experimento_01_report.json
results/experimento_01_report.md
```

## Ejemplo usando los archivos incluidos

Puedes probar la misma interfaz con los archivos de ejemplo:

```bash
python3 scripts/run_eco_pipeline.py \
  --bed examples/demo_regions.bed \
  --reference examples/tiny_reference.fa \
  --output-dir results \
  --prefix eco_custom_demo
```

O usar el atajo:

```bash
make pipeline
```

## Salidas generadas

| Archivo | Función |
| --- | --- |
| `<prefix>.fa` | FASTA extraído desde las coordenadas BED. |
| `<prefix>_report.json` | Reporte integrado con trazabilidad, features, motivos y feedback. |
| `<prefix>_report.md` | Reporte Markdown legible para revisión humana o portafolio. |

## Errores comunes

### El cromosoma no existe en el FASTA

Ejemplo de error:

```text
El cromosoma/contig 'chr1' no existe en el FASTA.
```

Causa probable:

- El BED usa `chr1`, pero el FASTA usa `1`.
- El BED y el FASTA pertenecen a referencias distintas.

Solución:

- Alinear nombres de cromosomas/contigs.
- Confirmar que BED y FASTA usan el mismo genome build.

### La región excede el largo del contig

Causa probable:

- Coordenadas fuera de rango.
- BED generado para una referencia distinta.

Solución:

- Revisar `start` y `end`.
- Confirmar que el FASTA corresponde al mismo sistema de referencia.

### Caracteres inválidos en secuencia

E.C.O. acepta bases:

```text
A, C, G, T, N
```

Si aparecen otros caracteres, el sistema rechazará la secuencia o reportará el problema según la etapa.

## Buenas prácticas

- Usa nombres claros para las regiones en la columna 4 del BED.
- Mantén tus archivos propios en una carpeta como `data/`.
- Usa prefijos descriptivos, por ejemplo `experimento_promotores_01`.
- No subas archivos genómicos pesados al repositorio si son grandes.
- Conserva siempre el dato original y genera resultados en `results/`.

## Lectura final

Esta etapa permite que E.C.O. pase de demo controlada a herramienta flexible:

```text
archivos propios → procesamiento trazable → reporte técnico y humano
```

Aún es un MVP: detecta motivos simples y no reemplaza herramientas bioinformáticas especializadas. Su valor actual está en la arquitectura, trazabilidad, validación y presentación del flujo.
