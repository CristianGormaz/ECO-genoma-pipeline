# Plan de admisión estable E.C.O.

Este documento define una regla operativa para decidir cuándo una pieza del sistema E.C.O. puede considerarse candidata a integración estable.

## Objetivo

Evitar que ideas, ramas antiguas, scripts experimentales o documentos conceptuales entren a `main` sin revisión, límites responsables y validación mínima.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Alcance: gobernanza, admisión y trazabilidad.
- No ejecuta modelos.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No incorpora datos sensibles.
- No incorpora evidencia externa automáticamente.

## Principio central

Una pieza puede avanzar hacia integración estable solo si cumple tres condiciones:

1. Es comprensible.
2. Es verificable.
3. Respeta los límites responsables del proyecto.

## Estados de admisión

| Estado | Significado | Acción recomendada |
|---|---|---|
| `draft` | Idea inicial o documento incompleto. | Mantener fuera de main estable. |
| `review_needed` | Tiene valor, pero requiere inspección. | Revisar en sprint documental. |
| `candidate` | Puede rescatarse como pieza pequeña. | Crear PR acotado. |
| `accepted` | Cumple límites y validaciones. | Integrar con test o checklist. |
| `blocked` | Riesgo alto o límites no claros. | No integrar sin auditoría. |

## Criterios mínimos para aceptar una pieza

Una pieza candidata debe cumplir:

- propósito claro;
- archivo o área bien definida;
- límites responsables explícitos;
- validación local posible;
- compatibilidad con el estado actual de `main`;
- ausencia de datos sensibles;
- ausencia de afirmaciones biomédicas aplicadas;
- ausencia de cambios de baseline o umbrales;
- trazabilidad del origen si proviene de una rama antigua.

## Criterios de bloqueo

Una pieza debe bloquearse si:

- mezcla documentación con cambios de datos, scripts y CI;
- modifica baseline sin comparación;
- recalibra umbrales sin auditoría;
- incorpora datos reales sin manifiesto;
- usa datos sensibles;
- convierte metáforas bioinspiradas en conclusiones clínicas;
- requiere integración masiva desde una rama antigua;
- no puede validarse con comandos simples.

## Flujo recomendado

1. Revisar la rama o archivo origen.
2. Identificar una sola pieza rescatable.
3. Crear rama nueva desde `main`.
4. Adaptar la pieza al estado actual del repo.
5. Agregar test documental o validación mínima.
6. Ejecutar pruebas.
7. Crear PR pequeño.
8. Integrar solo si los checks pasan.

## Aplicación a ramas antiguas

Las ramas antiguas no deben entrar completas. Deben tratarse como fuentes de ideas, no como paquetes listos para merge.

Cuando una rama antigua tenga valor, se debe rescatar una pieza por vez.

## Comandos seguros de revisión

```bash
git rev-list --count main..NOMBRE_RAMA
git diff --stat main..NOMBRE_RAMA
git diff --name-only main..NOMBRE_RAMA
git log --oneline main..NOMBRE_RAMA
```

## Resultado esperado de una admisión estable

Una admisión estable debe producir:

- un archivo claro;
- un test o checklist;
- una validación reproducible;
- un PR pequeño;
- un main limpio después del merge.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
