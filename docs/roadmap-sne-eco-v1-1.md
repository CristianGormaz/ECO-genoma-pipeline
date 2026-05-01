# Roadmap S.N.E.-E.C.O. v1.1

> Evolución técnica propuesta para el Sistema Nervioso Entérico de E.C.O. después del cierre v1.0.

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

Validación reproducible:

```bash
python -m pytest -q
make sne-validation
```

Artefactos actuales:

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

Crear una vista resumida tipo ruta digestiva completa:

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

Artefactos sugeridos:

```text
results/sne_eco_packet_trace.json
results/sne_eco_packet_trace.md
```

## Línea 2 — Reporte HTML S.N.E.-E.C.O.

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

Targets futuros:

```bash
make sne-validation-html
make open-sne-validation-html
```

## Línea 3 — Contrato público del módulo entérico

Crear una guía breve:

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

## Línea 4 — Integración con demo de portafolio

Destacar el flujo entérico como caso independiente:

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

## Línea 5 — Escenarios de validación ampliados

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

Comando sugerido:

```bash
python scripts/run_sne_eco_validation.py --scenario extended
```

## Línea 6 — Límites de uso responsable

S.N.E.-E.C.O. se mantiene como sistema técnico, educativo y bioinspirado. Sus salidas deben leerse como señales de pipeline y no como conclusiones personales o clínicas.

Reglas v1.1:

- mantener disclaimers en Markdown, JSON y futuro HTML;
- evitar lenguaje concluyente fuera del alcance técnico;
- no usar datos personales sensibles;
- usar datos públicos con trazabilidad de fuente;
- presentar clasificaciones como señales técnicas.

## Orden recomendado de implementación

```text
1. Trazabilidad por paquete
2. Exportador HTML de validación
3. Guía de API pública S.N.E.-E.C.O.
4. README / portafolio: sección visible S.N.E.-E.C.O.
5. Escenario extendido de validación
6. Revisión transversal de salidas
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
límite de uso visible en todas las salidas
```

## Lectura conceptual

```text
v1.0 = el sistema funciona
v1.1 = el sistema se explica, se muestra y se defiende mejor
```
