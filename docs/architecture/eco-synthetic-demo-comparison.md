# Comparación de demos sintéticas E.C.O.

## Estado

Estado: experimental.

Clasificación: permitido.

## Propósito

Este documento compara las demos sintéticas oficiales del pipeline E.C.O. para facilitar su lectura empírica, operativa y simbólica controlada.

## Tabla comparativa

| Demo | Comando | Patrón mínimo observado | Lectura operativa | Límite responsable |
|---|---|---|---|---|
| Minimal simulation | `python3 scripts/run_eco_minimal_simulation.py` | Procesamiento mínimo de una señal sintética | Representa una digestión inicial de datos controlados | No representa biología real ni diagnóstico |
| Signal balance | `python3 scripts/run_eco_signal_balance_demo.py` | Balance entre señales sintéticas | Representa estabilidad o desbalance interno del sistema simulado | No mide estados humanos reales |
| Waste pressure | `python3 scripts/run_eco_waste_pressure_demo.py` | Acumulación de presión residual | Representa carga no procesada o residuo operativo | No equivale a toxicidad biológica real |
| Absorption threshold | `python3 scripts/run_eco_absorption_threshold_demo.py` | Umbral de aceptación de señal | Representa decisión sintética entre absorber, limitar o rechazar | No modela absorción fisiológica real |

## Lectura integrada

Las cuatro demos forman un ciclo mínimo de E.C.O.:

1. Recibir una señal sintética.
2. Balancear su comportamiento.
3. Detectar presión residual.
4. Evaluar si la señal puede absorberse según un umbral.

## Uso recomendado

Antes de agregar una nueva demo, revisar si representa un patrón nuevo o si duplica una dimensión ya cubierta por estas cuatro demos.

## Validación asociada

Comando recomendado:

```bash
make eco-check-clean
```

## Límite responsable

Este documento es interpretativo y operativo. Usa solo demos sintéticas, no datos sensibles, no entrenamiento de modelos, no modificación de baseline, no recalibración de umbrales y no convierte metáforas simbólicas en conclusiones científicas o biomédicas.

## Reporte comparativo de demos sintéticas

- Comando: `make eco-synthetic-demo-comparison-report`
- Salida JSON: `results/eco_synthetic_demo_comparison_report.json`
- Salida Markdown: `results/eco_synthetic_demo_comparison_report.md`
- Uso: comparar patrones mínimos, lectura operativa y límites responsables de cada demo registrada.
