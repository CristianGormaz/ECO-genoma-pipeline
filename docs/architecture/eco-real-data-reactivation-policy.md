# E.C.O. real data reactivation policy

## Propósito

Este documento define cuándo una fuente real, manifiesto candidato o registro previamente detenido puede volver a revisión activa dentro de E.C.O.
Su función es evitar que una fuente bloqueada, retirada o marcada como needs_review sea reactivada sin evidencia, trazabilidad y límites responsables.

## Lectura rápida

Reactivar no significa usar datos reales automáticamente.
Solo significa que la fuente puede volver a revisión documental si se resolvió el motivo de detención y existe una nueva decisión registrada.

## Estados que pueden solicitar reactivación

- needs_review: puede volver a evaluación si se completa permiso, licencia, trazabilidad o alcance.
- retired: puede volver solo si existe motivo documentado para reabrirlo.
- superseded: no se reactiva directamente; se revisa la versión nueva.
- blocked: solo puede reconsiderarse si el bloqueo fue por error documental demostrado o si la fuente cambió de forma verificable.

## Condiciones mínimas para reactivar revisión

- Existe motivo de reactivación documentado.
- Existe evidencia nueva o corrección verificable.
- Se identifica el motivo original de detención, rollback o bloqueo.
- Se conserva historial previo sin borrar la decisión anterior.
- Se crea o actualiza un decision record.
- Se revisa nuevamente permiso, licencia, trazabilidad y sensibilidad.
- Se declara explícitamente que la reactivación no autoriza ingestión ni interpretación aplicada.

## Reglas de seguridad

- Una fuente bloqueada por datos sensibles no se reactiva sin revisión estricta.
- Una fuente con datos personales identificables permanece bloqueada.
- Una fuente con datos clínicos, genéticos humanos privados, forenses o biomédicos aplicados permanece bloqueada.
- Una fuente sin licencia clara vuelve a needs_review, no a activa.
- Una fuente reactivada debe volver a pasar por checklist, decisión y manifiesto.
- Toda reactivación requiere nuevo PR o registro equivalente.

## Qué permite la reactivación

- Reabrir revisión documental.
- Actualizar un manifiesto candidato.
- Corregir una decisión previa con trazabilidad.
- Volver a ejecutar validaciones documentales.
- Preparar una nueva decisión operativa.

## Qué no permite la reactivación

- No autoriza ingerir datos reales.
- No autoriza entrenar modelos.
- No autoriza modificar baseline.
- No autoriza recalibrar umbrales.
- No autoriza diagnóstico, recomendación clínica ni interpretación genética humana.
- No convierte una fuente bloqueada en segura por omisión.

## Decisión operativa

- Permitido: documentar criterios de reactivación y reabrir revisión documental.
- Condicional: volver a evaluar una fuente solo con evidencia nueva, trazabilidad y nueva decisión.
- Bloqueado: reactivar fuentes sensibles, privadas, clínicas, genéticas humanas privadas, forenses o biomédicas aplicadas sin autorización clara y revisión estricta.

## Límite responsable

Este documento es preventivo y documental.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Esta política define cómo una fuente detenida puede volver a revisión sin saltarse controles. No abre la puerta de golpe: solo permite volver a mirar la fuente con más evidencia y mejores límites.
