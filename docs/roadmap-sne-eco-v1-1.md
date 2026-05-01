# Roadmap S.N.E.-E.C.O. v1.1

> Evolución propuesta para el Sistema Nervioso Entérico de E.C.O. después del cierre v1.0.

## Estado de partida

S.N.E.-E.C.O. v1.0 ya cuenta con una arquitectura entérica funcional:

```text
barrera / mucosa informacional
→ sensor submucoso local
→ motilidad mientérica
→ microbiota informacional
→ defensa informacional
→ homeostasis
→ eje intestino-cerebro
→ validación UX
→ artefactos Markdown/JSON
```

La validación reproducible se ejecuta con:

```bash
python -m pytest -q
make sne-validation
```

Artefactos esperados:

```text
results/sne_eco_validation_report.md
results/sne_eco_validation_report.json
```

## Objetivo de v1.1

Convertir S.N.E.-E.C.O. desde un módulo funcional validado hacia una capa más observable, demostrable y fácil de integrar con el resto del pipeline E.C.O.

La prioridad no es agregar más órganos, sino mejorar:

```text
trazabilidad
observabilidad
UX técnica
contratos de integración
calidad de demostración
```

## Línea 1 — Trazabilidad del paquete

### Problema

Hoy el sistema registra etapas en `EcoPacket.history` y guarda decisiones en `metadata`, pero aún no existe una vista resumida tipo “ruta digestiva completa”.

### Propuesta

Crear una función o script que genere una traza por paquete:

```text
packet_id
source
payload_length
barrier_status
motility_action
defense_category
final_decision
absorbed / quarantined / discarded
microbiota_seen_count
```

### Artefacto sugerido

```text
results/sne_eco_packet_trace.json
results/sne_eco_packet_trace.md
```

### Validación

- Debe existir una prueba que confirme que cada paquete procesado tiene una ruta completa.
- Ningún paquete debe quedar sin `enteric_decision`.
- Ningún paquete debe quedar sin etapa final trazable.

## Línea 2 — Reporte HTML S.N.E.-E.C.O.

### Problema

La validación actual genera Markdown y JSON, pero para portafolio conviene una salida HTML estática.

### Propuesta

Crear un exportador simple:

```text
scripts/export_sne_eco_validation_html.py
```

Entrada:

```text
results/sne_eco_validation_report.json
```

Salida:

```text
results/sne_eco_validation_report.html
```

### Validación

- El HTML debe contener el estado homeostático.
- Debe mostrar métricas clave.
- Debe incluir el límite ético/biomédico.
- Debe abrirse con un target futuro:

```bash
make sne-validation-html
make open-sne-validation-html
```

## Línea 3 — Contrato público del módulo entérico

### Problema

El sistema ya expone clases y helpers desde `src.eco_core`, pero falta una guía corta de API pública.

### Propuesta

Crear una guía:

```text
docs/api-publica-sne-eco.md
```

Debe explicar:

```text
EntericSystem
process_dna_sequence
homeostasis_snapshot
gut_brain_report
gut_brain_markdown
make sne-validation
```

### Validación

- Agregar test documental que confirme que la guía menciona las APIs públicas principales.

## Línea 4 — Integración con demo de portafolio

### Problema

`make portfolio-demo` ya incorpora S.N.E.-E.C.O., pero el README y la demo podrían destacar mejor el flujo entérico como caso independiente.

### Propuesta

Agregar una sección visible:

```text
S.N.E.-E.C.O. v1.0 — demo entérica
```

Y listar:

```text
docs/sne-eco-v1-indice-demo.md
docs/roadmap-sne-eco-v1-1.md
results/sne_eco_validation_report.md
results/sne_eco_validation_report.json
```

### Validación

- Test documental que confirme que el README o índice de portafolio menciona esos artefactos.

## Línea 5 — Escenarios de validación ampliados

### Problema

La validación actual usa un lote mínimo de 4 paquetes. Es suficiente para v1.0, pero v1.1 puede probar escenarios más variados.

### Propuesta

Agregar un lote extendido opcional:

```text
valid_sequence
invalid_sequence
short_sequence
duplicate_sequence
heavy_sequence
ambiguous_n_sequence
non_text_payload
```

### Posible comando

```bash
python scripts/run_sne_eco_validation.py --scenario extended
```

### Validación

- El escenario mínimo debe seguir estable.
- El escenario extendido debe generar más paquetes sin romper el reporte.
- El estado homeostático debe seguir siendo interpretable.

## Línea 6 — Límites éticos y biomédicos reforzados

### Principio

S.N.E.-E.C.O. es un sistema bioinformático educativo y bioinspirado. No realiza diagnóstico, pronóstico clínico ni interpretación médica individual.

### Reglas v1.1

- Mantener disclaimers en Markdown, JSON y futuro HTML.
- Evitar lenguaje clínico concluyente.
- No usar datos genéticos personales.
- Usar datos públicos solo con trazabilidad de fuente.
- Presentar clasificaciones como señales técnicas, no como conclusiones médicas.

## Orden recomendado de implementación

```text
1. Trazabilidad por paquete
2. Exportador HTML de validación
3. Guía de API pública S.N.E.-E.C.O.
4. README / portafolio: sección visible S.N.E.-E.C.O.
5. Escenario extendido de validación
6. Revisión ética transversal de salidas
```

## Criterio de cierre v1.1

S.N.E.-E.C.O. v1.1 estará cerrado cuando existan:

```text
pytest completo en verde
make sne-validation funcionando
reporte Markdown
reporte JSON
reporte HTML
traza por paquete
API pública documentada
demo de portafolio conectada
límite biomédico visible en todas las salidas
```

## Lectura conceptual

v1.0 demostró que E.C.O. puede operar como intestino informacional.

v1.1 debe demostrar que ese intestino puede explicar su propio tránsito, mostrar evidencia, generar artefactos y ser entendido por otra persona sin entrar al código.

En simple:

```text
v1.0 = el sistema funciona
v1.1 = el sistema se explica, se muestra y se defiende mejor
```
