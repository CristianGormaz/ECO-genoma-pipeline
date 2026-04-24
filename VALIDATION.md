# Validación local del proyecto E.C.O.

Este documento registra una validación local de la primera versión funcional del proyecto **E.C.O. — Entérico Codificador Orgánico**.

## Entorno de prueba

- Sistema principal: ChromeOS Flex
- Entorno Linux: Crostini / Penguin
- Distribución Linux: Debian bookworm
- Git: 2.39.5
- Python: 3.11.2
- pip: 23.0.1 del sistema; actualizado a 26.0.1 dentro del entorno virtual
- pytest: 9.0.3 dentro del entorno virtual

## Preparación del entorno

Se instalaron herramientas base:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3 python3-pip python3-venv
```

Se clonó el repositorio:

```bash
git clone https://github.com/CristianGormaz/ECO-genoma-pipeline.git
cd ECO-genoma-pipeline
```

## Prueba funcional del script

Se ejecutó el módulo principal usando el archivo FASTA de ejemplo:

```bash
python3 src/eco_motif_analysis.py --fasta examples/demo_promoter.fa
```

Resultado observado:

- La secuencia `ejemplo_promotor` fue analizada correctamente.
- Se detectaron 6 motivos regulatorios.
- La secuencia `secuencia_con_n` fue analizada permitiendo bases ambiguas `N`.
- La secuencia `sin_motivos_clasicos` no reportó motivos, como se esperaba.

## Exportación de resultados

Se generaron salidas JSON y CSV:

```bash
mkdir -p mis_resultados
python3 src/eco_motif_analysis.py \
  --fasta examples/demo_promoter.fa \
  --json mis_resultados/demo.json \
  --csv mis_resultados/demo.csv
```

Archivos generados correctamente:

```text
mis_resultados/demo.json
mis_resultados/demo.csv
```

## Pruebas automatizadas

Debido a la política de Debian/ChromeOS para entornos Python administrados externamente, se usó un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest
python -m pytest -q
```

Resultado:

```text
.....                                                                           [100%]
5 passed in 0.02s
```

La prueba se repitió y volvió a pasar:

```text
.....                                                                           [100%]
5 passed in 0.01s
```

## Conclusión

La primera versión funcional del módulo `src/eco_motif_analysis.py` fue validada localmente en ChromeOS Flex/Crostini.

El proyecto queda verificado en esta etapa para:

- Lectura de archivos FASTA.
- Análisis de múltiples secuencias.
- Cálculo de longitud, porcentaje GC y porcentaje de bases `N`.
- Detección de motivos regulatorios simples.
- Exportación de resultados en JSON y CSV.
- Ejecución de pruebas automatizadas con `pytest`.

## Firma conceptual

**Cristian Gormaz**  
Proyecto E.C.O. — Entérico Codificador Orgánico
