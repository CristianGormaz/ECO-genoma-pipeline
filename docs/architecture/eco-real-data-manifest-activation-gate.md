# E.C.O. real data manifest activation gate

## Propósito

Este documento define cuándo un manifiesto de fuente real puede pasar desde ejemplo, borrador o revisión hacia manifiesto candidato validable dentro de E.C.O.
Su función es evitar que una fuente externa entre al flujo operativo sin revisión, decisión, límites responsables y trazabilidad mínima.

## Lectura rápida

Activar un manifiesto no significa ingerir datos reales.
Activar un manifiesto solo significa que la descripción de una fuente candidata puede entrar al validador operativo de manifiestos.

## Estados del manifiesto

- Ejemplo documental: archivo ficticio usado para enseñar formato.
- Borrador candidato: fuente posible, todavía sin revisión suficiente.
- Revisado: fuente evaluada con checklist y ficha de decisión.
- Aprobado para manifiesto: fuente pública, no sensible, trazable y compatible con uso estructural no aplicado.
- Activado para validación: manifiesto descriptivo ubicado en `docs/architecture/real-data-source-manifests/` y revisado por el validador.
- Bloqueado: fuente con datos sensibles, personales, clínicos, genéticos privados, riesgo aplicado o permiso insuficiente.

## Puerta de activación

Un manifiesto solo puede activarse si cumple todas estas condiciones:

- Existe revisión de fuente candidata.
- Existe ficha de decisión asociada.
- La decisión permite avanzar a manifiesto.
- La fuente es pública o cuenta con permiso claro.
- No contiene datos sensibles.
- No contiene personas identificables.
- No contiene datos clínicos.
- No contiene datos genéticos humanos privados.
- No requiere diagnóstico, interpretación biomédica aplicada ni uso forense.
- El uso previsto es estructural, descriptivo y no aplicado.
- El manifiesto declara límites, bloqueo de usos y siguiente acción segura.

## Qué permite la activación

- Registrar una fuente candidata como manifiesto descriptivo.
- Validar que el manifiesto cumple contrato documental.
- Mantener trazabilidad entre checklist, decisión, manifiesto y límites.
- Preparar el camino para una revisión posterior más estricta.

## Qué no permite la activación

- No activa ingestión de datos.
- No descarga datasets.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No genera conclusiones aplicadas.
- No autoriza afirmaciones biomédicas, clínicas, genéticas ni forenses.

## Decisión operativa

- Permitido: documentar la puerta de activación y sus condiciones.
- Condicional: activar un manifiesto real solo después de revisión completa y decisión explícita.
- Bloqueado: mover ejemplos, borradores o fuentes no revisadas al directorio validable.

## Límite responsable

Este documento es preventivo y documental.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Esta puerta decide cuándo una ficha deja de ser maqueta y puede entrar como manifiesto revisable. Todavía no digiere datos; solo autoriza revisar la etiqueta del alimento antes de abrirlo.
