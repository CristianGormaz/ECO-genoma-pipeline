# Ejemplo sintético de registro de evidencia externa E.C.O.

Este documento muestra cómo completar el registro de evidencia externa usando un caso sintético, no real y no aplicado.

## Objetivo

Probar el formato de registro sin incorporar evidencia externa real, datos sensibles, datos clínicos, datos genéticos privados ni conclusiones biomédicas aplicadas.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Naturaleza del ejemplo: sintético.
- No representa una fuente real.
- No ingiere datos reales.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No produce afirmaciones biomédicas aplicadas.

## Ejemplo completo

```text
evidence_id: EXT-ECO-SYN-0001
source_label: Nota sintética sobre señales bioinspiradas de equilibrio digestivo
source_type: synthetic_reference_note
intended_use: contexto
admission_decision: accept_as_context
responsible_limits: sin entrenamiento; sin datos sensibles; sin modificación de baseline; sin recalibración de umbrales; sin afirmaciones biomédicas aplicadas
requires_real_data_manifest: no
baseline_or_threshold_impact: none
status: reviewed
notes: Usar solo como ejemplo de llenado del registro. No representa evidencia empírica real.
```

## Lectura operativa

Este ejemplo demuestra que una referencia puede aceptarse solo como contexto cuando:

- no contiene datos reales;
- no contiene datos sensibles;
- no se usa para entrenar modelos;
- no altera baseline ni umbrales;
- no se transforma en conclusión científica aplicada;
- deja explícito su uso permitido.

## Decisión del ejemplo

La decisión `accept_as_context` significa que el registro puede ayudar a explicar una idea, pero no valida resultados, no justifica cambios técnicos sensibles y no habilita uso aplicado.

## Relación con el registro base

Este ejemplo debe leerse junto con:

```bash
make eco-external-evidence-register
```

## Cuándo bloquear un registro similar

Un registro parecido debe marcarse como `blocked` si incluye:

- datos sensibles;
- datos genéticos privados;
- diagnóstico clínico;
- evidencia real sin trazabilidad;
- impacto en baseline o umbrales;
- afirmaciones biomédicas aplicadas;
- entrenamiento o evaluación con datos reales sin manifiesto.

## Resultado esperado

El ejemplo permite practicar el llenado del registro sin abrir riesgos operativos. Sirve como patrón para futuras revisiones documentales.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin ingestión automática de datos reales;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa.
