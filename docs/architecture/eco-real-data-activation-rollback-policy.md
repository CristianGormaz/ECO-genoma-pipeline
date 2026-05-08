# E.C.O. real data activation rollback policy

## Propósito

Este documento define cómo desactivar, revertir o bloquear un manifiesto de fuente real si aparece riesgo, permiso dudoso, sensibilidad no detectada o uso fuera de alcance dentro de E.C.O.
Su función es asegurar que toda activación tenga una salida segura, trazable y documentada.

## Lectura rápida

Si una fuente real candidata deja de cumplir límites responsables, no se fuerza el avance.
Se detiene, se documenta el motivo, se revierte el estado operativo y se evita cualquier ingestión, entrenamiento o interpretación aplicada.

## Cuándo aplicar rollback

- La fuente contiene datos sensibles no detectados.
- La fuente contiene personas identificables.
- La fuente contiene datos clínicos, genéticos humanos privados o biomédicos aplicados.
- La licencia, permiso o trazabilidad no es clara.
- El uso previsto cambia desde análisis estructural hacia interpretación aplicada.
- El manifiesto fue activado por error.
- La revisión posterior contradice la decisión inicial.
- Aparece riesgo de diagnóstico, inferencia individual, uso forense o afirmación biomédica aplicada.

## Acciones de rollback

- Cambiar estado a bloqueado o needs_review.
- Retirar el manifiesto del flujo validable si corresponde.
- Registrar motivo, fecha, evidencia revisada y decisión.
- Mantener la trazabilidad documental sin borrar historial relevante.
- Detener cualquier siguiente paso de ingestión, análisis real o automatización.
- Requerir nueva revisión antes de cualquier reactivación.

## Estados posteriores posibles

- needs_review: falta claridad, permiso o trazabilidad.
- blocked: existe riesgo sensible, clínico, genético privado, personal, forense o aplicado.
- retired: el manifiesto queda archivado por obsolescencia o reemplazo.
- superseded: existe una versión corregida que reemplaza la anterior.

## Qué no permite rollback

- No autoriza borrar evidencia sin registro.
- No autoriza ocultar una activación equivocada.
- No autoriza reinterpretar datos sensibles como seguros.
- No autoriza continuar si aparece riesgo aplicado.
- No autoriza entrenamiento, ingestión ni recalibración.

## Reglas mínimas

- Ante duda razonable, detener avance.
- Ante sensibilidad, bloquear.
- Ante permiso dudoso, volver a revisión.
- Ante error documental, corregir con nuevo registro.
- Ante cambio de alcance, abrir nuevo PR y nueva decisión.

## Decisión operativa

- Permitido: documentar rollback, bloquear manifiestos y volver a revisión.
- Condicional: reactivar solo con nueva revisión, nueva decisión y límites explícitos.
- Bloqueado: continuar con una fuente riesgosa, sensible, privada, clínica, genética humana privada o aplicada.

## Límite responsable

Este documento es preventivo y documental.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Esta política es el freno de emergencia de E.C.O. Si una fuente que parecía segura deja de serlo, el sistema se detiene, registra el motivo y vuelve a un estado seguro.
