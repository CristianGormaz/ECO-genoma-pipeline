# Guía de diagnóstico de cobertura E.C.O.

Esta guía explica cómo leer la cobertura del dataset adaptativo S.N.E.-E.C.O.

## Por qué existe

Después de ampliar escenarios sintéticos, no conviene agregar más ejemplos a ciegas. Primero hay que identificar qué rutas digestivas siguen poco representadas.

## Comando directo

```bash
python scripts/run_sne_eco_state_coverage.py --extended --output-json results/sne_eco_state_coverage_report.json --output-md results/sne_eco_state_coverage_report.md
```

## Qué mide

```text
row_count
unique_feature_routes
state_counts
decision_counts
defense_counts
motility_counts
fallback_predictions
incorrect_predictions
coverage_warnings
```

## Cómo leer advertencias

- `state_underrepresented:*`: falta cubrir más ejemplos que terminen en ese estado.
- `decision_underrepresented:*`: falta cubrir más casos de esa decisión digestiva.
- `fallback_predictions_present`: el baseline encontró rutas no vistas y usó el estado por defecto.
- `incorrect_predictions_present`: revisar las rutas confundidas en la matriz de confusión.

## Criterio para el siguiente sprint

Agregar nuevas rutas solo donde el diagnóstico lo indique. No se deben agregar ejemplos para inflar métricas, sino para cubrir zonas digestivas poco representadas.

## Límite responsable

Este diagnóstico no representa desempeño general, no modela conciencia humana, no diagnostica y no debe usarse como herramienta clínica o forense.
