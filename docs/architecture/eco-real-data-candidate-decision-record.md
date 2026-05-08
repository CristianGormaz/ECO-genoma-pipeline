# E.C.O. real data candidate decision record

## Propósito

Este documento define la ficha mínima para registrar decisiones sobre fuentes candidatas de datos reales en E.C.O.
Su función es dejar trazabilidad antes de aceptar, revisar o bloquear una fuente.

## Lectura rápida

Cada candidato debe tener una decisión explícita antes de avanzar.
La decisión no autoriza ingestión automática, entrenamiento, interpretación aplicada ni uso clínico.

## Estados de decisión

- accepted_for_manifest: la fuente puede avanzar a manifiesto descriptivo.
- needs_review: falta información antes de avanzar.
- blocked: la fuente no puede avanzar por sensibilidad, riesgo o falta crítica.

## Campos mínimos

- candidate_id: identificador del candidato.
- source_name: nombre de la fuente.
- source_reference: URL, referencia o ubicación reproducible.
- decision_status: accepted_for_manifest, needs_review o blocked.
- decision_date: fecha de la decisión.
- decision_reason: motivo breve de la decisión.
- reviewer: persona o rol que revisó.
- evidence_checked: documentos, checklist o política revisada.
- responsible_limit: límite responsable declarado.
- next_action: bloquear, revisar o preparar manifiesto.

## Plantilla mínima

```yaml
candidate_id: eco_candidate_example
source_name: Example public environmental source
source_reference: https://example.org/source
decision_status: needs_review
decision_date: YYYY-MM-DD
decision_reason: Falta confirmar licencia y alcance permitido.
reviewer: project_operator
evidence_checked:
  - eco-real-data-first-safe-candidate-policy.md
  - eco-real-data-candidate-review-checklist.md
  - eco-real-data-candidate-lifecycle.md
responsible_limit: No ingerir datos reales hasta contar con manifiesto validado.
next_action: revisar licencia antes de preparar manifiesto
```

## Reglas

- accepted_for_manifest no autoriza ingestión de datos reales.
- needs_review debe indicar qué falta antes de avanzar.
- blocked debe indicar el motivo de bloqueo.
- Toda decisión debe poder leerse sin abrir el dataset.
- Toda decisión debe mantener trazabilidad con checklist, política y ciclo de vida.

## Bloqueos explícitos

- No aceptar datos personales sensibles.
- No aceptar datos clínicos privados.
- No aceptar datos genéticos humanos privados.
- No aceptar fuentes con uso diagnóstico, forense o biomédico aplicado.
- No usar la decisión como permiso para entrenar modelos.
- No usar la decisión como permiso para recalibrar umbrales.
- No usar la decisión como permiso para modificar baseline.

## Límite responsable

Este documento es preventivo y documental.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Esta ficha es la huella de decisión: deja claro si una fuente avanza, queda pendiente o se bloquea, y por qué.
