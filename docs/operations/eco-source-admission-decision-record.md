# Registro de decisión para admisión de fuentes E.C.O.

Este documento convierte el siguiente límite operativo del ciclo adaptativo en una pieza verificable antes de considerar cualquier fuente externa.

## Estado

- Estado: attention.
- Clasificación: condicional.
- Uso: documental, sintético y de gobernanza.
- No ingiere datos reales.
- No habilita entrenamiento.
- No modifica baseline.
- No recalibra umbrales.
- No produce afirmaciones biomédicas aplicadas.

## Propósito

Antes de incorporar una fuente externa al flujo E.C.O., debe quedar registrada una decisión explícita sobre:

- origen de datos;
- licencia o permiso de uso;
- ausencia de datos sensibles;
- propósito no clínico;
- criterios de exclusión;
- validación documental;
- separación entre simulación, evaluación e interpretación.

## Relación con piezas existentes

- Snapshot del ciclo: `docs/operations/eco-adaptive-dataset-cycle-snapshot.md`
- Registro de fuentes sensibles: `data/governance/sne_eco_sensitive_source_registry.jsonl`
- Validador del registro sensible: `scripts/run_sne_eco_sensitive_source_registry.py`
- Manifest de fuente real: `docs/architecture/eco-real-data-source-manifest-validator.md`

## Plantilla mínima de decisión

| Campo | Pregunta operativa | Estado permitido |
|---|---|---|
| Origen | ¿De dónde viene la fuente? | Debe ser público, sintético o con permiso verificable. |
| Licencia | ¿La licencia permite uso educativo/experimental? | Debe estar declarada. |
| Sensibilidad | ¿Contiene datos personales, clínicos, genéticos privados o casos identificables? | Debe ser `no`; si es `sí`, queda bloqueado. |
| Propósito | ¿Para qué se usará? | Solo estudio, simulación, documentación o evaluación no aplicada. |
| Exclusión | ¿Qué casos se rechazan? | Datos sensibles, diagnóstico, forense, reclamos aplicados, umbrales sin auditoría. |
| Validación | ¿Qué comando o prueba protege la decisión? | Debe existir test, gate o revisión documental. |
| Separación | ¿Se distingue estudiar, simular, entrenar, evaluar e interpretar? | Debe quedar explícito antes de avanzar. |

## Decisión operativa actual

E.C.O. se mantiene en modo sintético/documental. Las fuentes externas quedan en espera hasta que una fuente candidata cumpla la plantilla mínima y pase por el registro de sensibilidad correspondiente.

## Lectura simple

Este registro actúa como una aduana: no deja entrar datos nuevos solo porque parecen útiles. Primero pregunta de dónde vienen, si pueden usarse, si contienen información sensible y si el uso sigue siendo experimental y responsable.
