# E.C.O. real data candidate example decision record

## Propósito

Este documento entrega un ejemplo ficticio de ficha de decisión para una fuente candidata de datos reales en E.C.O.
Su función es mostrar cómo registrar una decisión sin usar, descargar, ingerir ni interpretar datos reales.

## Lectura rápida

El ejemplo representa una fuente ambiental pública agregada y no sensible.
No es una fuente real aprobada; es un caso documental para aprender el formato de decisión.

## Example decision record

```yaml
candidate_id: eco_candidate_public_environmental_example
source_name: Synthetic public environmental aggregate example
source_reference: documentation_example_only
decision_status: accepted_for_manifest
decision_date: YYYY-MM-DD
decision_reason: Fuente ejemplo, pública, agregada, ambiental, no personal y no sensible; apta solo para mostrar cómo preparar un manifiesto descriptivo.
reviewer: project_operator
evidence_checked:
  - eco-real-data-first-safe-candidate-policy.md
  - eco-real-data-candidate-review-checklist.md
  - eco-real-data-candidate-lifecycle.md
  - eco-real-data-candidate-decision-record.md
responsible_limit: No ingerir datos reales hasta contar con manifiesto validado y revisión explícita.
next_action: preparar manifiesto descriptivo de ejemplo sin descarga ni ingestión real
```

## Por qué este ejemplo es seguro

- Es ficticio y documental.
- No contiene personas identificables.
- No contiene datos clínicos.
- No contiene datos genéticos humanos privados.
- No contiene datos biomédicos aplicados.
- No permite inferir salud, identidad, conducta individual ni riesgo personal.
- No autoriza ingestión automática de datos reales.

## Decisión operativa

- Permitido: usar este ejemplo como guía documental.
- Condicional: crear un manifiesto real solo si existe fuente pública, licencia clara y revisión completa.
- Bloqueado: tratar este ejemplo como dataset real aprobado.

## Límite responsable

Este documento es preventivo, ficticio y documental.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Este ejemplo funciona como una ficha de práctica: muestra cómo E.C.O. decide si una fuente podría avanzar a manifiesto, sin tocar datos reales.
