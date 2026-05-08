# E.C.O. real data candidate manifest example

## Propósito

Este documento muestra un ejemplo ficticio de manifiesto candidato para una fuente de datos reales en E.C.O.
Su función es enseñar el formato esperado antes de crear un manifiesto real validable.

## Lectura rápida

Este ejemplo no es un manifiesto activo.
No debe guardarse todavía dentro de `docs/architecture/real-data-source-manifests/` porque eso lo convertiría en candidato para validación operativa.

## Example candidate manifest

```yaml
manifest_id: eco_real_data_candidate_manifest_example_v1
candidate_id: eco_candidate_public_environmental_example
source_name: Synthetic public environmental aggregate example
source_reference: documentation_example_only
source_kind: public_environmental_aggregate
decision_record: eco-real-data-candidate-example-decision-record.md
review_status: example_only_not_approved_source
allowed_use:
  - document_structure
  - describe_fields
  - validate_manifest_shape
blocked_use:
  - ingest_real_data
  - train_models
  - recalibrate_thresholds
  - modify_baseline
  - biomedical_claims
sensitivity:
  contains_personal_data: false
  contains_clinical_data: false
  contains_private_human_genetic_data: false
  contains_biomedical_applied_data: false
responsible_limit: Documentation example only; no ingestion, no training, no baseline change, no threshold recalibration.
next_action: create a real manifest only after source review, license check and explicit approval
```

## Por qué este ejemplo no entra al validador todavía

El validador operativo revisa manifiestos ubicados en el directorio de manifiestos candidatos.
Este archivo queda como documentación para evitar que un ejemplo ficticio sea tratado como fuente real.

## Decisión operativa

- Permitido: usar este ejemplo para entender cómo se vería un manifiesto candidato.
- Condicional: crear un manifiesto real solo después de checklist, decisión y revisión de licencia.
- Bloqueado: usar este ejemplo como fuente real aprobada o como autorización de ingestión.

## Límite responsable

Este documento es ficticio, preventivo y documental.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Este ejemplo es una maqueta: muestra cómo se llenaría un manifiesto, pero todavía no abre la puerta a datos reales.
