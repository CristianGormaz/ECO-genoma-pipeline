# Guía de rutas confundidas E.C.O.

Esta guía explica cómo leer el análisis de rutas confundidas del baseline adaptativo S.N.E.-E.C.O.

## Por qué existe

El diagnóstico de cobertura indica cuántas rutas faltan. El análisis de rutas confundidas indica cuáles son y qué escenario conviene agregar.

## Comando directo

```bash
python scripts/run_sne_eco_state_confusion.py --extended --output-json results/sne_eco_state_confusion_report.json --output-md results/sne_eco_state_confusion_report.md
```

## Qué entrega

```text
source
observed_state
predicted_state
matched_rule
final_decision
defense_category
defense_severity
feature_route
suggested_scenario
reason
```

## Cómo leer suggested_scenario

- `add_training_route:*`: falta una ruta equivalente en entrenamiento.
- `add_recurrence_variants_for_duplicate_routes`: faltan variantes de recurrencia.
- `add_retained_payload_length_variants`: faltan variantes de cuarentena por longitud o retención.
- `add_invalid_payload_variants`: faltan variantes de rechazo por payload inválido.
- `add_absorption_variants_for_stable_routes`: faltan variantes absorbibles estables.

## Criterio de uso

No se deben agregar ejemplos para subir artificialmente el accuracy. Se deben agregar escenarios donde el reporte muestre confusión, fallback o baja cobertura.

## Límite responsable

Este análisis es educativo y experimental. No representa desempeño general, no modela conciencia humana, no diagnostica y no tiene uso clínico o forense.
