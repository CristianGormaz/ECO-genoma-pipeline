# Checklist de admisión de evidencia externa E.C.O.

Esta checklist convierte la política mínima de evidencia externa en una revisión práctica antes de aceptar una fuente, argumento o referencia externa dentro del proyecto E.C.O.

## Objetivo

Evitar que una fuente externa se convierta automáticamente en dato real, conclusión aplicada, cambio de baseline, cambio de umbral o evidencia operativa sin revisión explícita.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Alcance: checklist, admisión documental y trazabilidad.
- No ingiere datos reales.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No produce afirmaciones biomédicas aplicadas.

## Checklist rápida

| Pregunta | Respuesta esperada para avanzar | Bloquear si... |
|---|---|---|
| ¿La fuente tiene origen identificable? | Sí. | No se puede rastrear origen, autoría o contexto. |
| ¿El uso está definido? | Contexto, comparación, checklist o referencia documental. | Se quiere usar como verdad operativa automática. |
| ¿Contiene datos sensibles? | No. | Contiene datos personales, genéticos privados o información sensible. |
| ¿Requiere ingestión de datos reales? | No, o requiere flujo separado. | Se intenta ingresar datos reales sin manifiesto. |
| ¿Modifica baseline? | No. | Cambia baseline sin auditoría. |
| ¿Recalibra umbrales? | No. | Cambia umbrales sin justificación y revisión. |
| ¿Hace afirmaciones biomédicas aplicadas? | No. | Deriva diagnóstico, predicción clínica o recomendación aplicada. |
| ¿Puede revisarse como pieza pequeña? | Sí. | Requiere integrar una rama antigua completa. |
| ¿Tiene validación reproducible? | Sí, test documental o checklist. | No hay forma simple de verificarla. |

## Decisión de admisión

| Resultado | Significado | Acción |
|---|---|---|
| `accept_as_context` | Sirve para explicar contexto. | Puede documentarse con límites. |
| `accept_as_reference` | Sirve como referencia documental. | Puede enlazarse o resumirse con trazabilidad. |
| `review_needed` | Tiene valor, pero no está lista. | Crear revisión documental separada. |
| `blocked` | Riesgo alto o fuera de alcance. | No integrar. |

## Flujo recomendado

1. Identificar la fuente o argumento externo.
2. Definir para qué se quiere usar.
3. Responder la checklist rápida.
4. Clasificar la decisión de admisión.
5. Si avanza, crear una pieza documental pequeña.
6. Agregar test documental o validación mínima.
7. Integrar solo por PR pequeño con checks pasando.

## Señales de bloqueo inmediato

- Datos sensibles.
- Datos genéticos privados.
- Diagnóstico clínico.
- Entrenamiento con datos reales sin manifiesto.
- Cambio de baseline sin auditoría.
- Recalibración de umbrales sin revisión.
- Evidencia externa usada como conclusión biomédica aplicada.
- Integración masiva desde rama antigua.

## Relación con la política externa

Documento base:

```bash
make eco-external-evidence-policy
```

Esta checklist no reemplaza la política. La vuelve ejecutable como revisión práctica.

## Resultado esperado

Una fuente externa admitida debe quedar clasificada, limitada y trazable. No debe entrar al pipeline como dato real ni modificar decisiones técnicas sin un flujo separado.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin ingestión automática de datos reales;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
