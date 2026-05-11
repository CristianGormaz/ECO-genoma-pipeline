# Contrato documental de dataset adaptativo E.C.O.

Este documento define las reglas mínimas para describir un dataset adaptativo dentro del proyecto E.C.O. sin incorporar datos reales, sin entrenamiento y sin modificar baseline.

## Objetivo

Establecer una frontera clara entre estudiar una estructura de datos adaptativa y ejecutar procesos sensibles como entrenamiento, evaluación aplicada, modificación de baseline o recalibración de umbrales.

## Clasificación

- Tipo de pieza: contrato documental.
- Clasificación: condicional.
- Alcance permitido: estructura, trazabilidad, campos descriptivos y criterios de bloqueo.
- No contiene datos reales.
- No contiene datos sensibles.
- No contiene datos genéticos privados.
- No ejecuta modelos.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No genera afirmaciones biomédicas aplicadas.

## Principio central

Un dataset adaptativo E.C.O. solo puede describirse como una estructura controlada, sintética o documental, hasta que exista una autorización explícita, manifiesto válido y revisión separada.

## Campos documentales permitidos

| Campo | Propósito | Límite |
|---|---|---|
| `record_id` | Identificador sintético o documental. | No debe revelar personas, muestras reales ni fuentes sensibles. |
| `source_type` | Tipo de fuente declarada. | Debe indicar `synthetic`, `documental` o `mock`. |
| `adaptive_state` | Estado operativo simulado. | No debe representar diagnóstico ni condición biomédica real. |
| `signal_family` | Familia de señal conceptual. | Debe mantenerse como metáfora técnica o simulación. |
| `evidence_level` | Nivel de respaldo documental. | No convierte evidencia externa en verdad aplicada. |
| `risk_flag` | Bandera de revisión. | Debe activar bloqueo si hay datos reales, sensibles o ambiguos. |
| `review_status` | Estado de revisión. | Debe usar estados como `draft`, `review_needed`, `candidate`, `accepted` o `blocked`. |
| `notes` | Observaciones técnicas. | No debe incluir datos personales ni afirmaciones clínicas. |

## Estados permitidos

| Estado | Significado | Acción recomendada |
|---|---|---|
| `draft` | Borrador conceptual. | Mantener fuera de integración estable. |
| `review_needed` | Requiere revisión humana. | Auditar antes de avanzar. |
| `candidate` | Pieza documental candidata. | Validar límites y trazabilidad. |
| `accepted` | Cumple contrato documental. | Puede integrarse con test. |
| `blocked` | Riesgo alto o ambiguo. | No integrar sin auditoría. |

## Criterios mínimos de aceptación

Una pieza asociada a dataset adaptativo puede avanzar solo si cumple:

- propósito claro;
- origen trazable;
- datos sintéticos o documentales;
- ausencia de datos sensibles;
- ausencia de datos genéticos privados;
- ausencia de entrenamiento;
- ausencia de cambios de baseline;
- ausencia de recalibración de umbrales;
- ausencia de afirmaciones biomédicas aplicadas;
- validación local reproducible;
- revisión en PR pequeño.

## Criterios de bloqueo

Debe bloquearse cualquier pieza que:

- incorpore datos reales sin manifiesto;
- use datos personales, clínicos, genéticos privados o sensibles;
- mezcle dataset con entrenamiento;
- mezcle dataset con evaluación aplicada;
- modifique baseline;
- recalibre umbrales;
- use evidencia externa como conclusión aplicada;
- transforme metáforas bioinspiradas en afirmaciones biomédicas;
- requiera merge masivo desde ramas antiguas.

## Relación con estado adaptativo

El dataset adaptativo no representa personas, pacientes, diagnósticos ni organismos reales. En esta etapa solo describe estados operativos sintéticos para apoyar trazabilidad, simulación educativa y arquitectura experimental.

## Relación con evidencia externa

La evidencia externa puede registrarse como referencia documental, pero no debe activar cambios automáticos en datos, baseline, umbrales o conclusiones.

## Relación con baseline

Cualquier cambio de baseline debe tratarse en sprint separado, con checklist, comparación, justificación y auditoría. Este contrato no autoriza cambios de baseline.

## Resultado esperado

Un dataset adaptativo aceptable en E.C.O. debe ser:

1. sintético o documental;
2. trazable;
3. verificable;
4. limitado;
5. no clínico;
6. no diagnóstico;
7. no entrenable por defecto;
8. separado de baseline y umbrales.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin incorporación de datasets reales;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin integración masiva de ramas antiguas.
