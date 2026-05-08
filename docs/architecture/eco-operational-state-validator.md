# E.C.O. operational state validator

## Propósito

Este validador revisa que los ejemplos de estados operativos sintéticos cumplan el schema operacional de E.C.O.
Su función es convertir la documentación operacional en una pieza verificable por pruebas automáticas.

## Comando

```bash
make eco-validate-operational-state-examples
```

## Límite responsable

Este validador trabaja solo con documentación y JSON sintéticos.
No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.
