# Guía operativa de revisión de evidencia externa E.C.O.

Esta guía convierte la política, el checklist, el registro y el ejemplo sintético de evidencia externa en un flujo de revisión ejecutable.

## Objetivo

Ayudar a decidir si una evidencia externa puede registrarse como referencia contextual del proyecto sin convertirla en dato de entrenamiento, conclusión biomédica o modificación de baseline.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Alcance: revisión, trazabilidad y decisión documental.
- No ingiere datos reales.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No genera afirmaciones biomédicas aplicadas.

## Cuándo usar esta guía

Usar esta guía cuando aparezca una fuente externa que pueda servir como contexto para E.C.O., por ejemplo:

- artículo científico;
- documentación técnica;
- dataset público descrito, pero no ingerido;
- paper de referencia;
- fuente educativa;
- evidencia conceptual para justificar una metáfora bioinspirada.

## Flujo recomendado

| Paso | Acción | Resultado esperado |
|---|---|---|
| 1 | Leer la fuente externa. | Se entiende qué afirma y qué no afirma. |
| 2 | Aplicar política de evidencia externa. | Se descartan usos fuera de límite. |
| 3 | Aplicar checklist. | Se confirma trazabilidad, alcance y riesgo. |
| 4 | Registrar la fuente si corresponde. | Queda una entrada documental, no un dato entrenable. |
| 5 | Clasificar decisión. | `accepted`, `review_needed` o `blocked`. |
| 6 | Definir uso permitido. | Contexto, glosario, comparación conceptual o referencia. |

## Estados de decisión

| Estado | Significado | Acción |
|---|---|---|
| `accepted` | La fuente es segura como referencia contextual. | Registrar con límites explícitos. |
| `review_needed` | La fuente parece útil, pero falta claridad. | Mantener fuera de integración estable. |
| `blocked` | La fuente cruza límites responsables. | No integrar. |

## Criterios mínimos de aceptación

Una fuente externa solo puede registrarse si cumple:

- origen claro;
- propósito claro;
- relación explícita con E.C.O.;
- uso limitado a contexto o documentación;
- ausencia de datos sensibles;
- ausencia de diagnóstico o aplicación clínica;
- ausencia de entrenamiento;
- ausencia de modificación de baseline;
- ausencia de recalibración de umbrales;
- trazabilidad suficiente para revisión futura.

## Criterios de bloqueo

Bloquear una fuente si:

- contiene datos personales sensibles;
- contiene datos genéticos privados;
- requiere ingestión de datos reales;
- exige entrenamiento o ajuste de modelo;
- modifica baseline o umbrales;
- permite inferencias clínicas;
- convierte metáforas bioinspiradas en conclusiones biomédicas;
- no tiene trazabilidad suficiente;
- mezcla evidencia con afirmaciones aplicadas no verificadas.

## Uso permitido dentro de E.C.O.

La evidencia externa puede usarse para:

- enriquecer documentación;
- mejorar glosarios;
- justificar analogías bioinspiradas;
- comparar conceptos de forma no aplicada;
- diseñar preguntas de investigación;
- mejorar criterios de revisión.

No puede usarse para:

- entrenar modelos;
- ajustar parámetros;
- cambiar baseline;
- recalibrar umbrales;
- emitir conclusiones clínicas;
- validar hipótesis biomédicas aplicadas.

## Relación con piezas ya integradas

Esta guía actúa como puente operativo entre:

- política de evidencia externa;
- checklist de evidencia externa;
- registro de evidencia externa;
- ejemplo sintético del registro;
- auditoría de rama de revisión externa.

## Resultado esperado

Cada revisión de evidencia externa debería terminar con una decisión simple:

```text
fuente: identificada
uso permitido: contexto documental
estado: accepted | review_needed | blocked
límites: explícitos
sin entrenamiento: sí
sin datos sensibles: sí
sin modificación de baseline: sí
sin recalibración: sí
```

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
