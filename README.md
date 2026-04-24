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
python src/eco_motif_analysis.py --fasta data/secuencia.fa
```

Guardar reporte JSON:

```bash
python src/eco_motif_analysis.py --fasta data/secuencia.fa --json results/reporte.json
```

Guardar reporte CSV:

```bash
python src/eco_motif_analysis.py --fasta data/secuencia.fa --csv results/reporte.csv
```

Modo estricto, rechazando bases `N`:

```bash
python src/eco_motif_analysis.py --fasta data/secuencia.fa --strict-acgt
```

## Ejemplo mínimo de FASTA

```fasta
>ejemplo_promotor
ACGTACGTCCAATTTTTTTTATAAAGGGCGGAATAAA
```

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. - Entérico Codificador Orgánico

Actualización asistida por ChatGPT.
