# Registro de evidencia externa E.C.O.

Este documento define un formato mínimo para registrar fuentes, argumentos o referencias externas revisadas dentro del proyecto E.C.O.

## Objetivo

Dejar trazabilidad clara de cada evidencia externa revisada, sin convertirla automáticamente en dato real, baseline, umbral, conclusión aplicada o insumo de entrenamiento.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Alcance: registro, trazabilidad y control documental.
- No ingiere datos reales.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No produce afirmaciones biomédicas aplicadas.

## Cuándo usar este registro

Usar este formato cuando una fuente externa sea revisada para:

- contexto conceptual;
- referencia documental;
- comparación teórica;
- apoyo de gobernanza;
- revisión futura;
- bloqueo por límite responsable.

## Campos mínimos

| Campo | Descripción | Ejemplo |
|---|---|---|
| `evidence_id` | Identificador interno breve. | `EXT-ECO-0001` |
| `source_label` | Nombre corto de la fuente o argumento. | `Artículo sobre microbiota y señales entéricas` |
| `source_type` | Tipo de fuente. | `paper`, `book`, `web`, `dataset_description`, `expert_note` |
| `intended_use` | Uso permitido dentro de E.C.O. | `contexto`, `referencia`, `comparación`, `bloqueado` |
| `admission_decision` | Decisión de admisión. | `accept_as_context`, `accept_as_reference`, `review_needed`, `blocked` |
| `responsible_limits` | Límites aplicables. | `sin datos sensibles; sin entrenamiento` |
| `requires_real_data_manifest` | Indica si requeriría manifiesto para avanzar. | `yes` / `no` |
| `baseline_or_threshold_impact` | Indica si toca baseline o umbrales. | `none`, `requires_audit` |
| `status` | Estado del registro. | `draft`, `reviewed`, `blocked`, `archived` |
| `notes` | Observación breve. | `Solo usar como contexto conceptual.` |

## Plantilla copiable

```text
evidence_id: EXT-ECO-0001
source_label: 
source_type: 
intended_use: 
admission_decision: review_needed
responsible_limits: sin entrenamiento; sin datos sensibles; sin modificación de baseline; sin recalibración de umbrales
requires_real_data_manifest: no
baseline_or_threshold_impact: none
status: draft
notes: 
```

## Decisiones permitidas

| Decisión | Uso permitido | Límite |
|---|---|---|
| `accept_as_context` | Puede usarse para explicar contexto. | No valida conclusiones aplicadas. |
| `accept_as_reference` | Puede citarse o resumirse como referencia documental. | Requiere trazabilidad clara. |
| `review_needed` | Tiene valor, pero falta revisión. | No integrar todavía. |
| `blocked` | Riesgo alto o fuera de alcance. | No integrar. |

## Bloqueos inmediatos

Bloquear el registro si aparece:

- dato sensible;
- dato genético privado;
- diagnóstico clínico;
- recomendación biomédica aplicada;
- entrenamiento con datos reales sin manifiesto;
- modificación de baseline sin auditoría;
- recalibración de umbrales sin revisión;
- intento de usar evidencia externa como verdad operativa automática.

## Relación con piezas previas

Este registro debe usarse junto con:

```bash
make eco-external-evidence-policy
make eco-external-evidence-checklist
```

La política define límites. La checklist ayuda a decidir. El registro deja trazabilidad.

## Resultado esperado

Cada evidencia externa revisada debe quedar documentada con decisión, uso permitido y límites. Ninguna evidencia externa debe entrar al pipeline como dato real sin un flujo separado.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin ingestión automática de datos reales;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
