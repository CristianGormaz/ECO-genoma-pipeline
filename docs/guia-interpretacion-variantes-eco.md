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

## Flujo E.C.O. de variantes

```text
Archivo TSV/ClinVar-style
→ ingesta
→ normalización de campos
→ clasificación de significado clínico
→ estimación de fuerza de evidencia
→ lectura práctica no diagnóstica
→ reporte JSON/Markdown
```

## Comando de demo

```bash
make variant-demo
```

Esto genera:

```text
results/eco_variant_demo_report.json
results/eco_variant_demo_report.md
```

El archivo de entrada demostrativo está en:

```text
examples/clinvar_style_demo_variants.tsv
```

## Próximo salto empírico

La demo actual usa un archivo reducido estilo ClinVar. El siguiente paso es conectar una descarga real y reducida desde ClinVar/NCBI o usar un archivo exportado desde una fuente clínica pública.

La regla de seguridad se mantiene:

> Fuente externa actualizada + interpretación prudente + límites explícitos + cero diagnóstico médico.

## Uso esperado dentro del portafolio

Esta etapa muestra que E.C.O. puede evolucionar desde motivos regulatorios simples hacia interpretación genómica más cercana a problemas reales, manteniendo trazabilidad, prudencia científica y estructura profesional.
