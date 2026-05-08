# E.C.O. operational state schema

## Propósito

Este documento define una ficha mínima para describir estados operativos sintéticos de E.C.O.
Su función es mantener trazabilidad documental sin modificar código funcional, baseline ni umbrales.

## Campos mínimos

- state_id: identificador estable del estado.
- state_kind: tipo de estado dentro de la secuencia operativa.
- classification: permitido, condicional o bloqueado.
- status: estado de ejecución u observación.
- inputs: entradas sintéticas o documentales.
- outputs: salidas sintéticas o documentales.
- validation: comandos o pruebas asociadas.
- responsible_limits: límites de seguridad y alcance.

## Límite responsable

Este esquema es documental y sintético.
No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.
