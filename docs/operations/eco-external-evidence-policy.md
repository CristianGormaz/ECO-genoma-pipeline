# Política mínima de evidencia externa E.C.O.

Este documento define cómo el proyecto E.C.O. puede usar evidencia externa de forma descriptiva, trazable y responsable.

## Objetivo

Permitir que fuentes externas ayuden a contextualizar decisiones del proyecto sin convertirlas automáticamente en datos del sistema, conclusiones aplicadas, cambios de baseline o cambios de umbral.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Alcance: gobernanza, evidencia descriptiva y trazabilidad.
- No ingiere datos reales.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No produce afirmaciones biomédicas aplicadas.

## Principio central

La evidencia externa puede orientar, comparar o contextualizar, pero no puede entrar al sistema como verdad operativa sin revisión explícita.

## Tipos de uso permitidos

| Uso | Permitido | Condición |
|---|---|---|
| Contexto conceptual | Sí | Debe citarse o describirse su origen. |
| Inspiración arquitectónica | Sí | Debe mantenerse como analogía o hipótesis. |
| Comparación documental | Sí | No debe modificar baseline ni umbrales. |
| Fuente para checklist | Sí | Debe pasar por revisión humana. |
| Datos reales para pipeline | No automático | Requiere manifiesto, revisión y admisión separada. |
| Evidencia clínica aplicada | Bloqueado | No corresponde al alcance actual del proyecto. |

## Estados de evidencia externa

| Estado | Significado | Acción recomendada |
|---|---|---|
| `mentioned` | Fuente mencionada sin revisión. | No usar como soporte fuerte. |
| `contextual` | Fuente útil para explicar contexto. | Puede citarse en documentación. |
| `candidate` | Fuente potencialmente útil para una política o checklist. | Revisar en PR separado. |
| `accepted_reference` | Fuente aceptada solo como referencia documental. | Usar con límites explícitos. |
| `blocked` | Fuente riesgosa o fuera de alcance. | No integrar. |

## Criterios mínimos de admisión

Una fuente externa solo puede avanzar si cumple:

- propósito claro;
- origen identificable;
- uso limitado a documentación o contexto;
- separación explícita entre evidencia, dato real y dato sensible;
- ausencia de afirmaciones biomédicas aplicadas;
- ausencia de cambios en baseline o umbrales;
- revisión compatible con el estado actual de `main`;
- validación documental o checklist reproducible.

## Criterios de bloqueo

Una fuente o pieza de evidencia debe bloquearse si:

- contiene datos sensibles;
- exige ingestión de datos reales sin manifiesto;
- se usa para diagnóstico, predicción clínica o decisión biomédica aplicada;
- intenta modificar baseline o umbrales;
- mezcla evidencia externa con entrenamiento;
- no permite distinguir entre hipótesis, simulación y afirmación aplicada;
- requiere integrar una rama antigua completa;
- no puede revisarse con comandos simples.

## Flujo recomendado

1. Registrar la fuente o argumento externo.
2. Clasificar su uso: contexto, comparación, checklist o bloqueo.
3. Confirmar que no contiene datos sensibles.
4. Confirmar que no modifica baseline ni umbrales.
5. Convertirla en pieza documental pequeña si aporta valor.
6. Agregar test documental o checklist.
7. Integrar por PR pequeño solo si los checks pasan.

## Relación con datos reales

Evidencia externa no equivale a dato real ingerible. Para usar datos reales se requiere un flujo separado de manifiesto, revisión, admisión y rollback.

## Relación con baseline y umbrales

Ninguna evidencia externa puede modificar baseline, pesos, umbrales o criterios de evaluación sin auditoría separada.

## Resultado esperado

Una evidencia externa aceptada debe quedar como referencia documental trazable, no como conclusión aplicada ni como entrada automática al pipeline.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin ingestión automática de datos reales;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
