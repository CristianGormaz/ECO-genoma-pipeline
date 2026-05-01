# Guía del dataset adaptativo E.C.O.

Esta guía describe cómo generar el primer dataset de transiciones internas para S.N.E.-E.C.O.

## Qué es una transición de estado

Una transición resume el cambio del sistema antes y después de procesar un paquete:

```text
homeostasis_before + packet_trace → homeostasis_after
```

En vez de intentar modelar conciencia humana, E.C.O. registra cambios técnicos observables del pipeline.

## Comando directo

```bash
python scripts/run_sne_eco_state_dataset.py --output-json results/sne_eco_state_dataset.json --output-tsv results/sne_eco_state_dataset.tsv
```

## Artefactos generados

```text
results/sne_eco_state_dataset.json
results/sne_eco_state_dataset.tsv
```

## Columnas principales

```text
packet_id
source
payload_length
barrier_status
barrier_permeability
motility_action
defense_category
defense_severity
final_decision
microbiota_seen_count
state_before
state_after
absorption_ratio_before
absorption_ratio_after
immune_load_before
immune_load_after
quarantine_ratio_before
quarantine_ratio_after
recurrence_ratio_before
recurrence_ratio_after
```

## Para qué sirve

Este dataset prepara el terreno para una fase posterior de Machine Learning auditable. Un modelo simple podría aprender patrones como:

```text
señales del paquete + estado previo → estado posterior
```

## Límites responsables

Este dataset no modela conciencia humana, no diagnostica, no identifica personas y no debe usarse como herramienta clínica o forense. Su función es educativa, experimental y arquitectónica: convertir el comportamiento interno de E.C.O. en datos analizables.

## Próximo paso posterior

Cuando este dataset sea estable, el siguiente sprint puede construir un baseline ML simple para comparar:

```text
regla homeostática actual vs modelo aprendido simple
```
