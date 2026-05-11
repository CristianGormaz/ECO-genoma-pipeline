# Índice de gobernanza de evidencia externa E.C.O.

Este documento ordena la ruta operativa para revisar, clasificar y registrar evidencia externa o escenarios externos dentro del proyecto E.C.O.

## Objetivo

Unificar las piezas de gobernanza ya integradas para que cualquier revisión futura tenga una ruta clara, segura y verificable.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Alcance: gobernanza, evidencia externa, revisión documental y trazabilidad.
- No ejecuta modelos.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No incorpora datos sensibles.
- No incorpora evidencia externa automáticamente.

## Ruta recomendada

| Paso | Documento | Uso principal | Resultado esperado |
|---:|---|---|---|
| 1 | Política de evidencia externa | Define qué se puede y no se puede hacer. | Límite operativo claro. |
| 2 | Checklist de evidencia externa | Revisa riesgos antes de admitir una pieza. | Decisión preliminar. |
| 3 | Registro de evidencia externa | Documenta origen, propósito y límites. | Trazabilidad mínima. |
| 4 | Ejemplo de registro | Muestra cómo completar el registro sin datos reales. | Ejemplo reproducible. |
| 5 | Guía de revisión de evidencia externa | Ordena el proceso de revisión. | Flujo operativo. |
| 6 | Matriz de escenarios externos | Clasifica escenarios como permitted, review_needed o blocked. | Decisión rápida. |

## Regla de uso

La evidencia externa no entra directamente al sistema. Primero se revisa, se clasifica, se registra y se documentan sus límites.

## Cuándo usar este índice

Usar este índice cuando:

- aparezca una fuente externa;
- se revise una rama antigua con material de evidencia;
- se proponga un escenario externo nuevo;
- se quiera distinguir simulación, documentación, evaluación o afirmación aplicada;
- exista duda sobre si algo es permitido, requiere revisión o debe bloquearse.

## Decisión operativa rápida

| Situación | Acción recomendada |
|---|---|
| Es una idea sintética o educativa | Revisar límites y documentar. |
| Usa fuente externa como contexto | Aplicar checklist y registro. |
| Podría parecer evidencia empírica | Clasificar con matriz de escenarios. |
| Usa datos públicos reales | Revisar licencia, sensibilidad y propósito antes de avanzar. |
| Usa datos personales, clínicos o genéticos privados | Bloquear. |
| Cambia baseline o umbral | Bloquear hasta auditoría separada. |
| Viene de una rama antigua | Rescatar una sola pieza por PR. |

## Orden seguro para futuros sprints

1. Revisar estado del repo.
2. Confirmar main limpio.
3. Identificar una sola pieza externa.
4. Aplicar política.
5. Aplicar checklist.
6. Completar registro si corresponde.
7. Clasificar con matriz.
8. Crear PR pequeño con test documental o validación mínima.

## Relación con ramas antiguas

Las ramas antiguas asociadas a evidencia externa deben tratarse como fuentes de ideas, no como paquetes listos para merge.

Si una rama contiene evidencia, scripts, datos, documentación y CI mezclados, se debe rescatar una pieza por vez.

## Resultado esperado

Este índice debe permitir que una persona entienda rápidamente qué documento usar, en qué orden y con qué límite.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
