# E.C.O. real data source manifest validator

## Propósito

Este validador revisa el contrato del manifiesto de fuentes externas antes de cualquier ingestión de datos reales.
Su función es asegurar que E.C.O. pueda distinguir fuentes permitidas, condicionales y bloqueadas.

## Comando

```bash
make eco-validate-real-data-source-manifest
```

## Qué valida

- Existencia del schema del manifiesto.
- Campos mínimos requeridos.
- Valores permitidos para sensibilidad y decisión.
- Límites responsables.
- Manifiestos candidatos futuros si existen.

## Límite responsable

Este validador no ingiere datos reales.
No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.
