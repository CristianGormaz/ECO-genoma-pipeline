# E.C.O. — Agentic Scaffold Proposal Registry

Registro documental — no ejecutable — para propuestas Agentic Scaffold.

## Propósito del registro

El registro cataloga propuestas Agentic Scaffold para mantener trazabilidad de
módulos candidatos, estado, clasificación, revisión humana, decisión final
humana y límites responsables. Su función es ordenar ejemplos y propuestas
documentales futuras sin convertirlas en capacidades integradas ni aprobadas por
defecto.

## Referencias obligatorias

- docs/operations/eco-agentic-scaffold-protocol.md
- docs/operations/eco-agentic-scaffold-proposal-template.md
- docs/operations/eco-agentic-scaffold-proposal-example.md

## Alcance

Este registro:

- es documental;
- no ejecuta funciones;
- no aprueba integración por sí mismo;
- no reemplaza revisión humana;
- no modifica principios admitidos;
- no modifica baseline;
- no recalibra umbrales;
- no usa datos reales;
- no entrena modelos.

El registro no propone endpoints, no propone scripts, no propone pipelines y no
modifica índices operativos en este sprint.

## Relación con Agentic Scaffold Protocol

Este registro queda subordinado al Agentic Scaffold Protocol. Mantiene la
separación entre autodesarrollo asistido y gobernado, construcción documental
por agente generativo y revisión humana obligatoria. No implica autonomía real,
conciencia ni libre albedrío real.

## Relación con Agentic Scaffold Proposal Template

Cada entrada del registro debe derivar de una propuesta compatible con la
Agentic Scaffold Proposal Template. La plantilla define la estructura mínima de
clasificación inicial, archivos mínimos sugeridos, validaciones esperadas,
criterios de pausa, límites responsables y decisión final humana.

El registro no sustituye a la plantilla: solo enumera propuestas y conserva su
estado documental.

## Criterios de inclusión

Una propuesta puede incluirse cuando:

- tiene documento asociado identificable;
- declara módulo candidato;
- declara estado y clasificación permitidos;
- conserva revisión humana y decisión final humana como campos explícitos;
- preserva límites responsables;
- no introduce código ejecutable;
- no habilita datos reales, entrenamiento, baseline ni umbrales.

## Campos mínimos por propuesta

Cada propuesta registrada debe listar:

- proposal_id
- título
- documento asociado
- módulo candidato
- tipo
- estado
- clasificación
- revisión humana
- decisión final humana
- validaciones esperadas
- límites responsables
- notas

## Registro inicial de propuestas

| proposal_id | título | documento asociado | módulo candidato | tipo | estado | clasificación | revisión humana | decisión final humana | validaciones esperadas | límites responsables | notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASC-PROP-001 | Governed Operational Trace Scaffold | docs/operations/eco-agentic-scaffold-proposal-example.md | Candidate Module: Governed Operational Trace Scaffold | ejemplo documental | pendiente de revisión humana | requiere revisión | pendiente | pendiente | test contractual, eco-status, suite completa, eco-check-clean | preservados | no ejecutable, no aprueba integración por sí misma |

## Estados permitidos

- borrador
- pendiente de revisión humana
- requiere cambios
- aprobado documentalmente
- rechazado
- pausado

## Clasificaciones permitidas

- permitido
- requiere revisión
- bloqueado

## Revisión humana y decisión final humana

Toda propuesta registrada conserva revisión humana y decisión final humana como
campos obligatorios. El registro no aprueba integración por sí mismo, no cambia
estados automáticamente y no reemplaza la evaluación de una persona revisora.

La decisión final humana debe quedar explícita antes de cualquier integración
futura. Una entrada registrada como ejemplo documental no concede autorización
operativa ni técnica.

## Límites responsables

El registro preserva estos límites:

- sin autonomía real;
- sin conciencia;
- sin libre albedrío real;
- sin datos reales;
- sin entrenamiento;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas.

Además, el registro no accede a datos reales, no entrena modelos, no modifica
baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Criterios de pausa

Debe pausarse la evolución de una propuesta registrada si:

- se intenta convertir el registro documental en función ejecutable;
- se solicita aprobar integración sin revisión humana;
- se intenta cambiar estados automáticamente;
- se propone tocar baseline, umbrales, entrenamiento o datos reales;
- se introduce lenguaje de autonomía real, conciencia o libre albedrío real;
- se formulan afirmaciones biomédicas aplicadas;
- se pretende modificar índices operativos dentro de este sprint.

## Uso esperado

El uso esperado del registro es consultar el estado documental de propuestas
Agentic Scaffold, ubicar su documento asociado, revisar su clasificación,
confirmar validaciones esperadas y conservar límites responsables antes de una
revisión humana.

El registro no ejecuta validaciones, no genera resultados técnicos y no decide
aceptación, rechazo o integración.

## Estado final del registro

Estado final del registro: documental, no ejecutable y pendiente de revisión
humana para cualquier cambio de estado o decisión final humana sobre propuestas
registradas.
