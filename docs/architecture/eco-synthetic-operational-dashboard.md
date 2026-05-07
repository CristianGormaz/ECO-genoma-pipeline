# E.C.O. synthetic operational dashboard

## Propósito

Este dashboard resume el estado operativo de las demos sintéticas de E.C.O.
Su función es observar señales generadas por simulaciones controladas, sin usar datos sensibles, sin entrenar modelos y sin modificar baseline.

## Componentes observados

- Minimal simulation demo.
- Signal balance demo.
- Waste pressure demo.
- Absorption threshold demo.
- Synthetic demos suite report.
- Synthetic demo comparison report.
- Synthetic signal matrix report.

## Límite responsable

Este módulo trabaja solo con datos sintéticos.
No entrena modelos, no procesa datos sensibles, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Comandos de validación

```bash
make eco-status
make eco-synthetic-operational-dashboard
python3 -m pytest -q
make eco-check-clean
```
