# E.C.O. real data candidate manifest template

## Propósito

Esta plantilla define cómo documentar una fuente candidata de datos reales antes de crear un manifiesto activo para E.C.O.
Su función es ordenar la revisión previa sin descargar, ingerir, entrenar ni interpretar datos reales.

## Lectura rápida

Esta plantilla no es un manifiesto activo.
Es un formato de preparación para registrar una fuente candidata y decidir si puede avanzar, requiere revisión o debe bloquearse.

## Estado del documento

- Tipo: plantilla documental.
- Uso: preparación de candidato.
- No valida datos reales.
- No descarga datos reales.
- No activa ingestión.

## Plantilla

### 1. Identificación

- candidate_id: eco_real_data_candidate_placeholder
- source_name: Nombre descriptivo de la fuente candidata.
- source_owner: Institución, publicador o responsable.
- source_reference: URL, DOI, repositorio o referencia reproducible.
- access_date: YYYY-MM-DD.
- candidate_status: draft | needs_review | blocked | ready_for_manifest

### 2. Tipo de fuente

- source_category: ambiental | documental | tabla_publica | otro_no_sensible
- expected_format: CSV | JSON | tabla | documento | desconocido
- expected_size: pequeño | mediano | desconocido
- aggregation_level: agregado | zona_amplia | no_aplica | desconocido

### 3. Permiso y trazabilidad

- license_or_terms: Describir licencia, permiso o condición de uso.
- public_access: sí | no | desconocido
- reproducible_reference: sí | no | desconocido
- permission_notes: Notas sobre restricciones, atribución o dudas pendientes.

### 4. Sensibilidad

- contains_personal_data: no | sí | desconocido
- contains_clinical_data: no | sí | desconocido
- contains_private_genetic_data: no | sí | desconocido
- contains_biomedical_applied_data: no | sí | desconocido
- reidentification_risk: bajo | medio | alto | desconocido
- sensitivity_notes: Explicar cualquier duda o bloqueo.

### 5. Uso permitido previsto

- intended_use: registrar fuente | revisar estructura | validar manifiesto | describir campos
- interpretation_level: ninguno | estructura | descripción_no_aplicada
- allowed_outputs: resumen técnico no aplicado, campos esperados, trazabilidad documental.
- blocked_outputs: diagnóstico, recomendación clínica, interpretación genética humana, afirmación biomédica aplicada.

### 6. Revisión contra checklist

- checklist_reviewed: sí | no
- checklist_result: aceptar_para_manifiesto | revisar_antes_de_avanzar | bloquear
- reviewer_notes: Notas breves de revisión.

### 7. Decisión operativa

- decision: draft | needs_review | blocked | ready_for_manifest
- reason: Justificación breve.
- next_step: documentar_mejor | bloquear | crear_manifiesto_descriptivo

## Ejemplo mínimo sintético

- candidate_id: eco_real_data_candidate_environmental_temperature_public_001
- source_name: Serie pública agregada de temperatura ambiental.
- source_category: ambiental
- expected_format: CSV
- contains_personal_data: no
- contains_clinical_data: no
- contains_private_genetic_data: no
- intended_use: revisar estructura
- checklist_result: aceptar_para_manifiesto
- decision: ready_for_manifest

## Límite responsable

Esta plantilla es documental y preventiva.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Esta plantilla es el formulario previo: antes de crear un manifiesto activo, E.C.O. deja anotado qué fuente quiere revisar, por qué parece segura y qué límites bloquean su uso.
