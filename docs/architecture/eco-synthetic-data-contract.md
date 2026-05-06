# Contrato de datos sintéticos E.C.O.

## Estado

Estado: experimental.

Clasificación: permitido.

## Propósito

Este contrato define la estructura mínima que debe cumplir una simulación sintética E.C.O. antes de crear nuevas demos o comparar resultados.

## Separación operativa

- Estudiar datos: observar registros sintéticos sin entrenar modelos.
- Simular comportamiento: aplicar reglas determinísticas sobre un estado sintético.
- Entrenar modelos: fuera de alcance en este contrato.
- Evaluar resultados: revisar forma, consistencia, trazabilidad y límites declarados.
- Generar hipótesis: permitido solo como exploración educativa.
- Hacer afirmaciones aplicadas: bloqueado sin evidencia, auditoría y propósito explícito.

## Contrato mínimo de entrada

Toda simulación sintética debe declarar:

- simulation_id: identificador textual.
- data_policy: synthetic_only.
- initial_state: estado inicial sintético.
- ticks: cantidad de pasos simulados.
- ruleset: nombre de la regla usada.

## Contrato mínimo de traza

Cada registro de trace debe incluir:

- tick: paso entero mayor o igual a 1.
- nutrient: valor entero no negativo.
- signal: valor entero no negativo.
- waste: valor entero no negativo.
- stability: valor entero no negativo.
- action: acción textual del paso simulado.

## Contrato mínimo de salida

Toda salida debe incluir:

- title.
- scope.
- trace.
- summary.
- limits.

El bloque summary debe declarar:

- classification: allowed.
- data_policy: synthetic_only.
- training: false.
- sensitive_data: false.
- baseline_changed: false.
- threshold_recalibrated: false.

## Criterio de aceptación

- La simulación debe ser determinística.
- Debe usar solo datos sintéticos.
- No debe entrenar modelos.
- No debe usar datos sensibles.
- No debe modificar baseline.
- No debe recalibrar umbrales.
- No debe convertir metáforas simbólicas en conclusiones científicas.
- No debe hacer afirmaciones biomédicas aplicadas.

## Límite responsable

Este contrato es documental y operativo. No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no afirma aplicaciones biomédicas, físicas ni clínicas.
