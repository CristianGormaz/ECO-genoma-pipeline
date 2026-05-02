# Changelog

Todos los cambios relevantes del proyecto se documentarán en este archivo.

## [sne-eco-v1.0-rc1] - 2026-05-02

### Agregado

- Documentación de **S.N.E.-E.C.O. v1.0 Release Candidate**.
- Narrativa empírica del pipeline adaptativo S.N.E.-E.C.O.
- README integrado con estado actual, comandos reproducibles y enlace a documentación empírica.
- Script de auditoría de recurrencia:
  - `scripts/run_sne_eco_recurrence_audit.py`
- Suite de estabilidad:
  - `tests/test_sne_eco_stability_suite.py`

### Mejorado

- Baseline adaptativo con jerarquía de decisión:
  - `feature_key`
  - `digestive_key`
  - `defense_key`
  - `homeostasis_projection`
  - `recurrence_guard`
- Resolución de rutas confundidas mediante variantes dirigidas, proyección homeostática y guardia de recurrencia.
- Cobertura de pruebas para evitar regresiones en:
  - rutas confundidas;
  - recurrencia redundante;
  - uso inesperado de `default_state`;
  - reportes JSON/Markdown.

### Validación local reportada

```text
153 passed
Rutas confundidas: 0
Rutas confundidas de recurrencia: 0
Auditoría de recurrencia: limpia
```

### Alcance

Esta versión candidata estabiliza la capa adaptativa entérica del pipeline E.C.O. como arquitectura de software bioinspirada, educativa y experimental.

### Límite responsable

S.N.E.-E.C.O. v1.0 RC no modela conciencia humana, no entrega diagnóstico clínico, no tiene uso forense y no reemplaza evaluación profesional.

La metáfora entérica funciona como lenguaje de diseño para organizar decisiones computacionales con filtrado, memoria, defensa, equilibrio y estabilidad.
