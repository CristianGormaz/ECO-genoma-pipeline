# Guía E.C.O. para interpretación segura de variantes

## Objetivo

Esta guía define el alcance de la etapa de variantes dentro del Proyecto E.C.O. La meta es obtener un resultado interpretable a partir de registros genómicos, con una estructura similar a un informe clínico, pero sin convertir el proyecto en un diagnóstico médico.

E.C.O. puede ayudar a responder preguntas como:

- ¿Qué variantes fueron procesadas?
- ¿Qué gen y condición aparecen asociados?
- ¿Qué significado clínico declara una fuente externa?
- ¿Qué tan fuerte parece la revisión de esa fuente?
- ¿Qué lectura prudente se puede hacer?
- ¿Qué límites impiden usarlo como diagnóstico?

## Límite central

E.C.O. interpreta registros de variantes, no interpreta pacientes.

No incorpora por sí solo:

- síntomas;
- historia familiar;
- zigosidad;
- penetrancia;
- etnia/población;
- edad o sexo;
- método de laboratorio;
- confirmación clínica;
- consejería genética;
- consentimiento médico.

Por eso el resultado debe llamarse:

> Informe bioinformático interpretativo de variantes

No debe llamarse:

> Diagnóstico genético personal

## Categorías iniciales E.C.O.

| Clasificación externa | Categoría E.C.O. | Lectura prudente |
|---|---|---|
| Pathogenic / Likely pathogenic | alerta_clinica_alta | Puede ser relevante; requiere validación clínica. |
| Uncertain significance / VUS | incertidumbre_clinica | No debe guiar decisiones médicas por sí sola. |
| Benign / Likely benign | probablemente_no_patogenica | No parece patogénica para esa condición; no descarta otros riesgos. |
| Conflicting classifications | evidencia_conflictiva | Hay desacuerdo; revisar submitters, fecha y criterios. |
| Risk factor | factor_de_riesgo_no_determinista | Puede modificar probabilidad; no equivale a enfermedad asegurada. |
| Drug response | farmacogenomica_o_respuesta_a_farmacos | Puede orientar respuesta a fármacos; no cambiar tratamiento sin médico. |
| No classification provided / etiquetas no reconocidas | clasificacion_no_estandarizada | Requiere revisión manual y mejora del diccionario E.C.O. |

## Flujo E.C.O. de variantes

```text
Archivo TSV/ClinVar-style
→ ingesta
→ normalización de campos
→ clasificación de significado clínico
→ estimación de fuerza de evidencia
→ resumen por categoría
→ resumen por gen
→ matriz gen × categoría
→ lectura práctica no diagnóstica
→ reporte JSON/Markdown
```

## Demo educativa local

```bash
make variant-demo
```

Esto usa un TSV pequeño incluido en el repositorio:

```text
examples/clinvar_style_demo_variants.tsv
```

Y genera:

```text
results/eco_variant_demo_report.json
results/eco_variant_demo_report.md
```

## Muestra pública real desde ClinVar

```bash
make clinvar-sample
```

Este comando descarga o reutiliza cache local del archivo público:

```text
https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz
```

Por defecto busca una muestra exploratoria en:

```text
BRCA1, BRCA2, CFTR, TP53
```

El modo de muestreo recomendado es:

```text
gene-balanced
```

Esto intenta equilibrar:

```text
genes representados + categorías E.C.O.
```

El objetivo no es estimar prevalencia real. El objetivo es generar una muestra didáctica y diversa para probar interpretación.

Genera:

```text
results/eco_clinvar_sample.tsv
results/eco_clinvar_sample_report.json
results/eco_clinvar_sample_report.md
```

## Cómo leer el informe Markdown

El informe incluye:

1. **Resumen por categoría:** cuántas variantes caen en alerta, VUS, benignas, conflictivas, farmacogenómicas o no estandarizadas.
2. **Resumen por gen:** cuántas variantes fueron incluidas por cada gen.
3. **Matriz gen × categoría:** permite ver si un gen concentra cierto tipo de hallazgo.
4. **Resumen ejecutivo de variantes:** tabla compacta con ID, gen, condición resumida, clasificación externa, categoría E.C.O., evidencia y acción prudente.
5. **Lectura clínica prudente del conjunto:** explica el significado de cada grupo sin diagnosticar.
6. **Lectura detallada por variante:** conserva trazabilidad, HGVS, fuente ClinVar y recomendación prudente.
7. **Límites científicos y clínicos:** explicita lo que no se puede concluir.

Para revisar el informe en terminal:

```bash
sed -n '1,180p' results/eco_clinvar_sample_report.md
```

Para abrirlo en entorno gráfico:

```bash
xdg-open results/eco_clinvar_sample_report.md
```

## Qué significa una muestra balanceada

Una muestra balanceada puede verse así:

```text
BRCA1 | 5 variantes
BRCA2 | 5 variantes
CFTR  | 5 variantes
TP53  | 5 variantes
```

Y su matriz puede mostrar algo como:

```text
cada gen con 1 alerta, 1 VUS, 1 benigna, 1 conflictiva y, cuando existe, 1 farmacogenómica o no estandarizada
```

Eso no representa frecuencia poblacional. Representa una selección exploratoria útil para demostrar que E.C.O. sabe organizar evidencia diversa.

## Interpretación prudente

- **Alerta clínica alta:** revisar con fuente actualizada y genética clínica si fuera una muestra real.
- **VUS/incertidumbre clínica:** no usar para decisiones médicas por sí sola.
- **Probablemente no patogénica:** no sobredimensionar; tampoco descarta otros riesgos.
- **Evidencia conflictiva:** requiere revisión manual de submitters, fecha y criterios.
- **Farmacogenómica:** no modificar tratamiento sin equipo médico.
- **No estandarizada:** mejorar diccionario y revisar fuente original.

## Validación técnica

La etapa de variantes queda cubierta por pruebas automáticas:

```bash
make check
```

Esto ejecuta, entre otras cosas:

```text
pytest
scripts/run_eco_variant_demo.py
```

La descarga real desde ClinVar no se ejecuta dentro de `make check` porque depende de red externa y de un archivo público cambiante. Por eso se mantiene como comando separado:

```bash
make clinvar-sample
```

## Uso esperado dentro del portafolio

Esta etapa muestra que E.C.O. puede evolucionar desde motivos regulatorios simples hacia interpretación genómica más cercana a problemas reales, manteniendo:

- descarga pública reproducible;
- cache local;
- deduplicación;
- muestreo balanceado;
- clasificación por significado clínico declarado;
- estimación de fuerza de evidencia;
- resumen por gen;
- matriz gen × categoría;
- reporte JSON/Markdown;
- límites explícitos de no diagnóstico.

Una forma breve de presentarlo:

> E.C.O. convierte registros públicos de variantes en un informe bioinformático interpretativo, equilibrando genes y categorías clínicas, sin diagnosticar pacientes ni calcular riesgo personal.
