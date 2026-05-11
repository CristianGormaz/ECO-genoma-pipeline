# Matriz de escenarios externos sintéticos E.C.O.

Este documento clasifica escenarios externos posibles para el proyecto E.C.O. sin incorporar datos reales, sin entrenar modelos y sin hacer afirmaciones biomédicas aplicadas.

## Objetivo

Definir una guía simple para decidir si un escenario externo puede documentarse, requiere revisión o debe bloquearse.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Alcance: gobernanza, evidencia externa, admisión y trazabilidad.
- No ejecuta modelos.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No incorpora datos sensibles.
- No incorpora evidencia externa automáticamente.

## Regla central

Un escenario externo solo puede avanzar si sirve para mejorar trazabilidad, límites, comprensión o revisión documental.

No debe usarse para entrenar, diagnosticar, inferir causalidad biomédica ni validar afirmaciones aplicadas.

## Estados de clasificación

| Estado | Significado | Acción recomendada |
|---|---|---|
| `permitted` | Escenario sintético, educativo o documental. | Puede documentarse con límites explícitos. |
| `review_needed` | Escenario útil, pero con riesgo conceptual o de interpretación. | Revisar con checklist antes de integrar. |
| `blocked` | Escenario sensible, aplicado, clínico, privado o no verificable. | No integrar sin autorización y auditoría. |

## Matriz operativa

| Tipo de escenario externo | Estado sugerido | Condición mínima | Riesgo principal | Acción segura |
|---|---|---|---|---|
| Ejemplo sintético inventado | `permitted` | Debe declarar que no representa datos reales. | Confundir simulación con evidencia. | Documentar como demo sintética. |
| Fuente pública usada solo como referencia conceptual | `review_needed` | Debe registrarse origen, fecha y uso previsto. | Incorporar evidencia sin revisión. | Pasar por checklist y registro. |
| Artículo científico usado para contexto general | `review_needed` | Debe separarse contexto de afirmación aplicada. | Exagerar conclusiones. | Resumir límites y no convertirlo en dato. |
| Dataset público no ingerido | `review_needed` | Debe evaluarse licencia, sensibilidad y propósito. | Usarlo como datos reales sin manifiesto. | Crear manifiesto antes de cualquier uso. |
| Dataset público con datos biomédicos o genéticos | `blocked` | Requiere autorización clara y auditoría. | Datos sensibles o interpretación aplicada. | No integrar en sprint documental. |
| Datos personales, clínicos o genéticos privados | `blocked` | No permitido en flujo actual. | Privacidad, seguridad y daño aplicado. | Bloquear. |
| Comparación de modelos sobre datos reales | `blocked` | Requiere protocolo separado. | Entrenamiento o evaluación aplicada. | No mezclar con documentación. |
| Umbral nuevo derivado de evidencia externa | `blocked` | Requiere auditoría y comparación formal. | Recalibración no controlada. | Bloquear hasta revisión. |
| Metáfora bioinspirada para explicar arquitectura | `permitted` | Debe declararse como analogía. | Convertir metáfora en conclusión científica. | Documentar límites. |
| Escenario de admisión de rama antigua | `review_needed` | Debe rescatar una pieza por vez. | Integración masiva. | Crear PR pequeño. |

## Criterios para permitir

Un escenario puede clasificarse como `permitted` si cumple:

- es sintético, educativo o documental;
- no contiene datos sensibles;
- no contiene datos reales ingeridos;
- no modifica baseline;
- no recalibra umbrales;
- no entrena modelos;
- no hace afirmaciones biomédicas aplicadas;
- incluye límites responsables claros.

## Criterios para revisión

Un escenario debe ir a `review_needed` si:

- menciona fuentes externas;
- podría confundirse con evidencia empírica;
- requiere registrar origen o fecha;
- toca datos públicos;
- afecta decisiones de admisión;
- proviene de una rama antigua;
- necesita checklist antes de integrarse.

## Criterios para bloquear

Un escenario debe ir a `blocked` si:

- incluye datos sensibles personales;
- incluye datos genéticos privados;
- busca diagnóstico clínico;
- hace afirmaciones biomédicas aplicadas;
- entrena o evalúa modelos con datos reales;
- modifica baseline sin comparación;
- recalibra umbrales sin auditoría;
- no puede validarse de forma simple.

## Flujo recomendado

1. Describir el escenario.
2. Clasificarlo como `permitted`, `review_needed` o `blocked`.
3. Si es `permitted`, documentar límites.
4. Si es `review_needed`, usar checklist y registro.
5. Si es `blocked`, no integrarlo al sprint actual.
6. Mantener cualquier rescate en PR pequeño.

## Relación con documentos existentes

- Política de evidencia externa.
- Checklist de evidencia externa.
- Registro de evidencia externa.
- Ejemplo de registro.
- Guía de revisión de evidencia externa.
- Revisión de rama de expansión de escenarios externos.

## Resultado esperado

La matriz debe ayudar a decidir rápidamente qué tipo de escenario externo puede avanzar y qué tipo debe detenerse.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
