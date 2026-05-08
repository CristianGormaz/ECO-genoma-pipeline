# E.C.O. real data candidate lifecycle

## Propósito

Este documento define el ciclo de vida de una fuente candidata de datos reales dentro de E.C.O.
Su función es conectar política, checklist, plantilla, manifiesto, validación y decisión operativa sin permitir ingestión prematura.

## Lectura rápida

Una fuente real no entra directamente al pipeline.
Primero se identifica, se revisa, se documenta como candidata, se decide si puede transformarse en manifiesto y recién después puede pasar por validación.

## Flujo principal

1. Descubrimiento de candidato.
2. Revisión contra política de primer candidato seguro.
3. Revisión contra checklist de fuente candidata.
4. Registro en plantilla de candidato.
5. Decisión: bloquear, revisar o preparar manifiesto.
6. Creación de manifiesto descriptivo si corresponde.
7. Validación del manifiesto.
8. Decisión operativa final antes de cualquier uso.

## Estados del candidato

- discovered: fuente encontrada, todavía no revisada.
- under_review: fuente en revisión documental.
- needs_review: falta permiso, licencia, alcance o claridad técnica.
- blocked: fuente rechazada por sensibilidad, riesgo aplicado o falta crítica.
- ready_for_manifest: fuente candidata puede convertirse en manifiesto descriptivo.
- manifest_draft: existe manifiesto, pero todavía no está validado.
- manifest_validated: el manifiesto pasó validación estructural.
- approved_for_structural_use: autorizado solo para revisión estructural no aplicada.

## Reglas de transición

- discovered puede pasar a under_review.
- under_review puede pasar a needs_review, blocked o ready_for_manifest.
- needs_review no puede avanzar sin aclaración documentada.
- blocked no puede convertirse en manifiesto.
- ready_for_manifest puede pasar a manifest_draft.
- manifest_draft debe pasar por validación antes de cualquier uso.
- manifest_validated no autoriza interpretación aplicada.
- approved_for_structural_use solo permite revisar estructura, campos, formato y consistencia básica.

## Puertas de control

### Gate 1: seguridad inicial

- Debe ser pública, no sensible, trazable y pequeña.
- No debe ser clínica, genética humana privada, personal, forense ni biomédica aplicada.

### Gate 2: revisión documental

- Debe pasar por la checklist de revisión.
- Debe quedar registrada la decisión: aceptar para manifiesto, revisar antes de avanzar o bloquear.

### Gate 3: plantilla de candidato

- Debe existir candidate_id, source_name, source_reference, license_or_terms y sensitivity_notes.
- Debe declarar si contiene datos personales, clínicos, genéticos privados o biomédicos aplicados.

### Gate 4: manifiesto descriptivo

- El manifiesto no debe descargar ni contener datos reales.
- Solo describe fuente, permiso, alcance, formato esperado y límites.

### Gate 5: validación

- Debe pasar el validador de manifiesto.
- Debe mantenerse dentro de eco-check.
- Si falla, se bloquea el avance hasta corregir documentación.

## Bloqueos permanentes

- Datos personales sensibles.
- Datos clínicos privados.
- Datos genéticos humanos privados.
- Uso diagnóstico, clínico, forense o biomédico aplicado.
- Entrenamiento de modelos con datos reales sin autorización explícita.
- Recalibración de umbrales sin auditoría.
- Modificación de baseline sin comparación documentada.

## Salida permitida en esta etapa

- Documento de ciclo de vida.
- Plantilla de candidato.
- Manifiesto descriptivo sin datos reales.
- Validación estructural del manifiesto.
- Resumen técnico no aplicado.

## Límite responsable

Este documento es preventivo y arquitectónico.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Este ciclo de vida es el camino seguro de entrada: E.C.O. no se come un dato real de golpe; primero lo mira desde afuera, revisa si es seguro, lo documenta, valida el manifiesto y recién después decide si puede usarse solo de forma estructural.
