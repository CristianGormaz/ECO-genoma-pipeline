# Fundamentos de estado adaptativo E.C.O.

Este documento define una base conceptual mínima para hablar de estado adaptativo dentro del sistema E.C.O. sin convertirlo en baseline, diagnóstico, entrenamiento o afirmación biomédica aplicada.

## Objetivo

Establecer una forma simple y verificable de describir cómo una pieza del sistema puede cambiar de estado cuando recibe señales sintéticas, reglas operativas o evidencia revisada.

## Clasificación

- Tipo: fundamento documental.
- Clasificación: permitido.
- Alcance: arquitectura conceptual y operación segura.
- No ejecuta modelos.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No incorpora datos sensibles.
- No incorpora evidencia externa automáticamente.

## Qué significa estado adaptativo

En E.C.O., un estado adaptativo es una etiqueta operativa que describe cómo se encuentra una pieza del sistema frente a una señal o condición.

No representa una verdad biológica. No representa diagnóstico. No representa inferencia clínica. Es una forma ordenada de registrar comportamiento experimental o documental.

## Estados mínimos

| Estado | Significado | Acción recomendada |
|---|---|---|
| `observed` | Se detecta una señal, patrón o necesidad documental. | Registrar sin concluir. |
| `review_needed` | La señal parece útil, pero requiere revisión. | Revisar límites y trazabilidad. |
| `candidate` | La pieza puede avanzar como propuesta pequeña. | Crear PR acotado con test. |
| `accepted` | La pieza cumple límites y validación. | Integrar si los checks pasan. |
| `blocked` | Hay riesgo o falta claridad. | No integrar sin auditoría. |

## Ciclo adaptativo mínimo

1. Observar una señal.
2. Clasificar su estado.
3. Revisar límites responsables.
4. Definir una acción pequeña.
5. Validar con test o checklist.
6. Registrar la decisión.

## Señales permitidas

- documentación incompleta;
- rama antigua con contenido útil;
- ejemplo sintético;
- inconsistencia operativa;
- necesidad de trazabilidad;
- mejora de explicación o navegación.

## Señales sensibles

Requieren revisión separada:

- datos reales;
- datos genéticos privados;
- datasets de entrenamiento;
- métricas de evaluación;
- cambios de baseline;
- cambios de umbral;
- interpretación biomédica fuerte.

## Regla de seguridad

Un estado adaptativo puede orientar decisiones operativas, pero no puede por sí solo justificar cambios de baseline, entrenamiento, evaluación aplicada o afirmaciones biomédicas.

## Relación con admisión estable

Este fundamento debe usarse junto con el plan de admisión estable E.C.O. y el checklist de revisión de cambios de baseline.

## Resultado esperado

Un uso correcto de estado adaptativo debe dejar:

- una etiqueta clara;
- una decisión trazable;
- una validación reproducible;
- límites responsables explícitos;
- separación entre simulación, documentación, evaluación y entrenamiento.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin integración masiva de ramas antiguas.
