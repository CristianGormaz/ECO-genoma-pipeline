# S.N.E.-E.C.O. — Plan de admisión de escenarios estables

## Propósito

Este documento define la aduana de admisión para evidencia externa observada después de `sne-eco-v1.0-rc1`.

El objetivo no es entrenar ni modificar el baseline. El objetivo es separar, con trazabilidad, qué evidencia externa puede aspirar a convertirse en escenario estable futuro y qué evidencia debe quedar retenida, excluida o solo observada.

## Estado operativo

S.N.E.-E.C.O. ya cuenta con:

```text
RC1 congelado
→ observabilidad
→ comparación contra RC1
→ sonda externa
→ revisión de evidencia externa
→ política de evidencia externa
→ plan de admisión estable
```

## Regla principal

Ninguna evidencia externa entra automáticamente al dataset estable.

Toda evidencia debe pasar por una decisión de admisión:

| Acción de política | Decisión de admisión |
|---|---|
| `candidate_for_future_stable_scenario` | `admit_later` |
| `candidate_for_threshold_review` | `hold_for_threshold_review` |
| `keep_out_of_stable_dataset` | `exclude_until_policy_defined` |
| `do_not_train_yet` | `keep_as_observation_control` |
| alto riesgo / acción desconocida | `manual_review_required` |

## Criterios

### `admit_later`

La evidencia puede ser candidata futura, pero requiere:

- repetición externa;
- documentación de frontera;
- comparación contra RC1;
- nuevo sprint de incorporación controlada.

### `hold_for_threshold_review`

La evidencia indica tensión defensiva. No se debe incorporar sin revisar umbrales o criterios de defensa.

### `exclude_until_policy_defined`

La evidencia contiene payload inválido o simbólico/numeral fuera de política. Debe quedar fuera del dataset estable hasta definir una regla explícita.

### `keep_as_observation_control`

La evidencia coincide con el comportamiento esperado, pero no debe entrenarse todavía. Sirve como control externo.

### `manual_review_required`

La evidencia queda bloqueada si aparece alto riesgo, `default_state` inesperado o acción desconocida.

## Candados de estabilidad

Este plan exige que el sprint mantenga:

```text
stable_dataset_modified = False
baseline_modified = False
admission_locked = True
```

Esto protege el RC1 como línea base congelada.

## Comando reproducible

```bash
source .venv/bin/activate
python scripts/run_sne_eco_external_evidence_policy.py
python scripts/run_sne_eco_stable_admission_plan.py
cat results/sne_eco_stable_admission_plan.md
```

## Lectura UX

En lenguaje simple:

> S.N.E.-E.C.O. ya no solo observa evidencia externa. Ahora tiene una aduana: decide qué puede esperar afuera para entrar más adelante, qué necesita revisión, qué debe quedar fuera y qué sirve solo como control.

## Límite responsable

Este plan es educativo y experimental. No modifica dataset estable, baseline, reglas ni umbrales. No representa desempeño general, no modela conciencia humana y no tiene uso clínico/forense.
