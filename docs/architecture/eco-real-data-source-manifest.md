# E.C.O. real data source manifest

## Propósito

Este manifiesto define la ficha mínima para describir una fuente externa antes de cualquier ingestión de datos reales.
Su función es convertir la puerta de datos reales en un contrato revisable y verificable.

## Lectura rápida

E.C.O. no debe interpretar una fuente real sin antes registrar origen, permiso, sensibilidad, uso permitido, uso bloqueado y decisión de readiness.

## Campos mínimos

- source_id: identificador estable de la fuente candidata.
- source_name: nombre legible de la fuente.
- source_kind: tipo de fuente.
- origin: procedencia documentada.
- license_or_permission: licencia, permiso o condición de uso.
- sensitivity_classification: permitido, condicional o bloqueado.
- contains_identifiable_people: indica si hay personas identificables.
- contains_genetic_data: indica si contiene datos genéticos.
- contains_clinical_data: indica si contiene datos clínicos.
- allowed_use: uso permitido.
- blocked_use: uso bloqueado.
- readiness_decision: allow, review o block.
- responsible_limits: límites explícitos del manifiesto.

## Límite responsable

Este manifiesto no ingiere datos reales.
No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Este manifiesto es la ficha de ingreso: antes de que una fuente toque el sistema, E.C.O. debe saber qué es, de dónde viene, qué riesgo tiene y qué se permite hacer con ella.
