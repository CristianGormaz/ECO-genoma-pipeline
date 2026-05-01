# Guía de trazabilidad S.N.E.-E.C.O.

Esta guía explica cómo leer la **ruta digestiva** de cada paquete dentro del Sistema Nervioso Entérico de E.C.O.

## Qué es una ruta digestiva

Una ruta digestiva resume el tránsito de un paquete por el intestino informacional:

```text
ingesta
→ barrera
→ sensado
→ motilidad
→ defensa
→ decisión final
→ absorción / cuarentena / descarte
→ memoria microbiota
```

Su objetivo es mejorar la observabilidad del pipeline: no solo saber el resultado final, sino explicar por qué el dato llegó ahí.

## Comando directo

```bash
python scripts/run_sne_eco_trace.py --output-json results/sne_eco_packet_trace.json --output-md results/sne_eco_packet_trace.md
```

## Artefactos generados

```text
results/sne_eco_packet_trace.json
results/sne_eco_packet_trace.md
```

## Campos principales

```text
packet_id                 Identificador único del paquete.
source                    Origen asignado al dato.
payload_length            Largo del payload.
barrier_status            Resultado de la barrera/mucosa informacional.
barrier_permeability      Nivel de permeabilidad asignado.
motility_action           Movimiento decidido por el plexo mientérico.
defense_category          Categoría de defensa informacional.
defense_severity          Severidad defensiva.
final_decision            Acción final: absorb, reject, quarantine, discard_duplicate.
absorbed                  Indica si fue absorbido.
quarantined               Indica si quedó retenido.
discarded                 Indica si fue descartado.
rejected                  Indica si fue rechazado.
microbiota_seen_count     Veces que la microbiota informacional ha visto ese payload.
```

## Cómo leer la traza

Una secuencia válida debería mostrar:

```text
barrier_status: ok
motility_action: advance
final_decision: absorb
absorbed: true
```

Una secuencia inválida debería mostrar:

```text
barrier_status: rejected
motility_action: immune_discard
final_decision: reject
discarded: true
```

Una secuencia corta debería mostrar:

```text
barrier_status: quarantined
motility_action: quarantine
final_decision: quarantine
quarantined: true
```

Un duplicado debería mostrar:

```text
motility_action: discard_duplicate
final_decision: discard_duplicate
microbiota_seen_count: 2
```

## Uso responsable

La traza digestiva es una salida técnica de observabilidad del pipeline. Sirve para depurar, explicar y demostrar el flujo interno de E.C.O. No representa diagnóstico, conclusión clínica ni interpretación personal de datos genéticos.

## Relación con v1.1

Este documento implementa la primera línea del roadmap S.N.E.-E.C.O. v1.1:

```text
Trazabilidad del paquete
```

En simple:

```text
v1.0 demuestra que el sistema funciona.
v1.1 empieza mostrando por dónde pasó cada dato.
```
