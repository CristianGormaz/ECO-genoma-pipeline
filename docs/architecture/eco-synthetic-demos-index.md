# Índice de demos sintéticas E.C.O.

## Estado

Estado: experimental.

Clasificación: permitido.

## Propósito

Este índice organiza las demos sintéticas del proyecto E.C.O. que simulan comportamiento educativo sin usar datos reales, sin entrenamiento y sin afirmaciones aplicadas.

## Demos disponibles

### 1. Demo mínima de simulación

- Comando: `make eco-minimal-simulation-demo`
- Salida JSON: `results/eco_minimal_simulation_demo.json`
- Salida Markdown: `results/eco_minimal_simulation_demo.md`
- Validación: `make eco-validate-synthetic-contract`
- Propósito: observar una secuencia mínima de nutriente, señal, residuo, estabilidad y acción.

### 2. Demo de equilibrio de señal

- Comando: `make eco-signal-balance-demo`
- Salida JSON: `results/eco_signal_balance_demo.json`
- Salida Markdown: `results/eco_signal_balance_demo.md`
- Validación: `make eco-validate-signal-balance-demo`
- Propósito: observar una secuencia sintética de equilibrio entre señal, nutriente, residuo y estabilidad.

## Contrato común

Las demos deben respetar el contrato sintético E.C.O.:

- Usar datos sintéticos.
- No usar datos sensibles.
- No entrenar modelos.
- No modificar baseline.
- No recalibrar umbrales.
- No hacer afirmaciones biomédicas aplicadas.

## Acciones permitidas actuales

Por ahora, el contrato permite estas acciones:

- `digest`
- `rest`

## Límite responsable

Este índice es documental y operativo. No ejecuta simulaciones, no modifica resultados, no entrena modelos, no usa datos sensibles y no convierte metáforas simbólicas en conclusiones científicas.

## Validador global

Comando recomendado:

```bash
make eco-validate-synthetic-demos
```

Uso: validar todas las demos sintéticas registradas sin usar datos sensibles, sin entrenamiento y sin recalibrar umbrales.

## Registro de demos

- [Registro de demos sintéticas E.C.O.](eco-synthetic-demo-registry.md)

Uso: ubicar demos oficiales, comandos, salidas esperadas y validadores asociados.

- Waste pressure: demo sintética de presión residual y estabilidad.

## Demo: absorption threshold

- Comando: `make eco-absorption-threshold-demo`
- Runner: `scripts/run_eco_absorption_threshold_demo.py`
- Salidas: `results/eco_absorption_threshold_demo.json` y `results/eco_absorption_threshold_demo.md`

## Comparación de demos sintéticas

- [Comparación de demos sintéticas E.C.O.](eco-synthetic-demo-comparison.md)
- Uso: entender qué patrón mínimo representa cada demo registrada.
