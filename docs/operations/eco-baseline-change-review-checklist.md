# Checklist de revisión de cambios de baseline E.C.O.

Este documento define una revisión mínima antes de admitir cualquier cambio relacionado con baseline, datos o evaluación dentro del sistema E.C.O.

## Objetivo

Evitar que cambios sensibles entren a `main` sin trazabilidad, justificación, validación y límites responsables.

## Clasificación

- Tipo de sprint: documentación operativa.
- Clasificación: permitido.
- Alcance: gobernanza de baseline, datos y evaluación.
- No modifica baseline.
- No recalibra umbrales.
- No entrena modelos.
- No incorpora datos sensibles.
- No incorpora datos reales.

## Cuándo usar este checklist

Usar antes de aceptar cualquier cambio que toque:

- baseline;
- datasets;
- scripts de evaluación;
- métricas comparativas;
- umbrales de decisión;
- gates de admisión;
- resultados que puedan interpretarse como mejora del sistema.

## Checklist mínimo

Antes de admitir un cambio, confirmar:

- [ ] El propósito del cambio está escrito con claridad.
- [ ] El archivo o área afectada está identificada.
- [ ] El cambio no usa datos sensibles.
- [ ] El cambio no usa datos genéticos privados.
- [ ] El cambio no incorpora datos reales sin manifiesto.
- [ ] El cambio no modifica baseline sin comparación.
- [ ] El cambio no recalibra umbrales sin auditoría.
- [ ] El cambio no entrena modelos.
- [ ] El cambio no presenta afirmaciones biomédicas aplicadas.
- [ ] El cambio puede validarse con comandos simples.
- [ ] El cambio tiene test, checklist o evidencia documental.
- [ ] El PR es pequeño y revisable.

## Estados posibles

| Estado | Significado | Acción recomendada |
|---|---|---|
| `safe_doc` | Solo documentación operativa o conceptual. | Puede avanzar con test documental. |
| `review_needed` | Tiene valor, pero toca zona sensible. | Revisar en PR pequeño. |
| `compare_required` | Cambia baseline, evaluación o métrica. | Requiere comparación explícita. |
| `audit_required` | Toca umbrales, datos reales o decisiones fuertes. | No integrar sin auditoría. |
| `blocked` | Usa datos sensibles o afirmaciones aplicadas. | Bloquear. |

## Criterios de bloqueo

Bloquear el cambio si:

- mezcla datos, scripts, baseline y documentación en un solo PR;
- modifica baseline sin comparación previa;
- recalibra umbrales sin auditoría;
- usa datos sensibles;
- usa datos genéticos privados;
- incorpora datos reales sin manifiesto;
- presenta resultados como evidencia clínica;
- convierte metáforas bioinspiradas en conclusiones biomédicas aplicadas;
- no puede explicarse ni validarse de forma simple.

## Validación mínima recomendada

Para documentación:

```bash
.venv/bin/python -m pytest -q tests/test_eco_baseline_change_review_checklist.py
.venv/bin/python -m pytest -q
make eco-check-clean
```

Para cambios sensibles futuros, agregar además comparación o auditoría específica antes de merge.

## Decisión operativa

Este checklist no autoriza cambios de baseline. Solo define el filtro mínimo antes de considerar un cambio como candidato.

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin datos genéticos privados;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin integración masiva de ramas antiguas.
