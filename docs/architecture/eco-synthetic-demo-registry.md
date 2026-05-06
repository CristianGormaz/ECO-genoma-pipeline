# Registro de demos sintéticas E.C.O.

## Estado

Estado: experimental.

Clasificación: permitido.

## Propósito

Este registro enumera las demos sintéticas oficiales del proyecto E.C.O., sus comandos, salidas esperadas y validadores asociados.

## Regla operativa

Una demo sintética registrada debe:

- usar solo datos sintéticos;
- declarar límites responsables;
- generar una salida validable;
- pasar el contrato sintético;
- no entrenar modelos;
- no usar datos sensibles;
- no modificar baseline;
- no recalibrar umbrales;
- no hacer afirmaciones biomédicas aplicadas.

## Demos registradas

| Demo | Comando | Salida JSON | Salida Markdown | Validador | Estado |
|---|---|---|---|---|---|
| Minimal simulation | `python3 scripts/run_eco_minimal_simulation.py` | `results/eco_minimal_simulation_demo.json` | `results/eco_minimal_simulation_demo.md` | `python3 scripts/validate_eco_synthetic_contract.py results/eco_minimal_simulation_demo.json` | experimental |
| Signal balance | `python3 scripts/run_eco_signal_balance_demo.py` | `results/eco_signal_balance_demo.json` | `results/eco_signal_balance_demo.md` | `python3 scripts/validate_eco_synthetic_contract.py results/eco_signal_balance_demo.json` | experimental |

## Comando global recomendado

Para ejecutar y validar todas las demos sintéticas registradas:

```bash
make eco-validate-synthetic-demos
```

## Límite responsable

Este registro es documental y operativo. no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no convierte metáforas simbólicas en conclusiones científicas.
