# Carpeta `data/`

Esta carpeta está reservada para archivos locales de entrada que quieras procesar con E.C.O.

Aquí puedes guardar, solo en tu equipo:

```text
mis_regiones.bed
mi_referencia.fa
mi_referencia.fasta
otros_archivos_locales
```

## Uso recomendado

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

## Importante

No subas archivos genómicos pesados al repositorio.

El repositorio está configurado para ignorar los datos reales dentro de esta carpeta y conservar solo esta guía y `.gitkeep`.

## Regla clave

El BED y el FASTA deben usar el mismo sistema de referencia.

Ejemplo:

```text
BED hg19  -> FASTA hg19
BED hg38  -> FASTA hg38
```

Además, los nombres de cromosomas o contigs deben coincidir.

Si el BED usa:

```text
chr1
```

El FASTA debe tener:

```fasta
>chr1
```

## Buenas prácticas

- Usa nombres descriptivos para tus archivos.
- Conserva tus datos originales sin modificarlos.
- Genera resultados en `results/`.
- No uses esta carpeta para archivos privados sensibles si vas a compartir el equipo o el repositorio.
