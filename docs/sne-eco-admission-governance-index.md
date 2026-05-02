# S.N.E.-E.C.O. — Admission Governance Index

## Propósito

Este documento organiza la cadena de gobernanza de admisión para evidencia externa posterior a `sne-eco-v1.0-rc1`.

La prioridad es mantener estable la línea base RC1 mientras el sistema observa, clasifica, evalúa y simula la entrada de nuevos escenarios sin modificar el dataset estable, el baseline, las reglas ni los umbrales.

## Línea base protegida

Baseline congelado:

```text
sne-eco-v1.0-rc1
```

Criterios protegidos:

```text
Rutas confundidas: 0
Recurrencias confundidas: 0
Default_state confundido: 0
Dataset estable modificado: False
Baseline modificado: False
```

## Cadena de gobernanza

```text
external scenario probe
→ external evidence review
→ external evidence policy
→ stable admission plan
→ stable admission dry-run
→ comparison against RC1
```

## Módulos de la cadena

| Etapa | Script | Rol |
|---|---|---|
| Observabilidad | `run_sne_eco_observability_dashboard.py` | Resume reportes existentes sin recalibrar reglas |
| Comparación RC1 | `run_sne_eco_compare_against_rc1.py` | Contrasta el estado actual contra `sne-eco-v1.0-rc1` |
| Sonda externa | `run_sne_eco_external_scenario_probe.py` | Evalúa escenarios externos sin incorporarlos |
| Revisión de evidencia | `run_sne_eco_external_evidence_review.py` | Clasifica diferencias externas observadas |
| Política externa | `run_sne_eco_external_evidence_policy.py` | Define gobernanza: observar, excluir, documentar o retener |
| Plan de admisión | `run_sne_eco_stable_admission_plan.py` | Ordena qué podría admitirse más adelante |
| Dry-run | `run_sne_eco_stable_admission_dry_run.py` | Simula admisión sin modificar nada |

## Estado operativo actual

```text
Admisiones simuladas ahora: 0
Candidatos futuros: 4
Retenciones por umbral: 2
Exclusiones temporales: 2
Controles observacionales: 2
```

## Lectura bioinspirada

En términos E.C.O., la evidencia externa entra como alimento nuevo al sistema. Primero se observa, luego se clasifica, después se revisa su riesgo, y finalmente se simula su admisión.

El sistema no absorbe inmediatamente lo externo. Lo retiene en una aduana digestiva computacional hasta contar con evidencia repetida, política explícita o revisión segura.

## Regla de estabilidad

Ningún escenario externo debe ingresar al dataset estable si antes no pasa por:

```text
observación externa
→ revisión de evidencia
→ política de evidencia
→ plan de admisión
→ dry-run
→ comparación contra RC1
```

## Qué queda prohibido en esta etapa

No modificar directamente:

- `adaptive_state_baseline.py`
- reglas de `recurrence_guard`
- umbrales de homeostasis
- dataset estable
- criterios RC1

## Próximo paso sugerido

```text
SNE-22 — Admission governance command
```

Objetivo: crear un comando único que ejecute toda la cadena de gobernanza y entregue un reporte consolidado.

## Límite responsable

Este índice documenta una arquitectura educativa y experimental. No representa desempeño clínico, forense ni biomédico. No modela conciencia humana. La metáfora entérica se usa como lenguaje de diseño para organizar decisiones computacionales con trazabilidad.
