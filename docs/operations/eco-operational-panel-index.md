# Índice operativo de comandos y estados E.C.O.

Este índice funciona como panel de control para operar el repositorio E.C.O. sin perder contexto.

## Objetivo

Responder rápidamente:

1. ¿En qué estado está el repositorio?
2. ¿Qué comando corresponde ejecutar ahora?
3. ¿Cuándo debo detenerme antes de seguir?

## Estados operativos

| Estado | Qué significa | Acción recomendada |
|---|---|---|
| `green` | Árbol limpio, validaciones pasando y contexto claro. | Puedes detenerte, iniciar sprint desde `main` o continuar una rama de sprint controlada. |
| `attention` | Hay algo que revisar: rama abierta, cambios pendientes o validación parcial. | No abras otro objetivo. Diagnostica antes de avanzar. |
| `recovery` | Hay error de terminal, cambios accidentales, rama confusa o riesgo de pérdida. | Respaldar, diagnosticar, limpiar y volver a estado estable. |

## Comandos de estado

| Comando | Uso | Modifica archivos |
|---|---|---|
| `make eco-status` | Ver estado operativo del repositorio. | No |
| `git status --short` | Ver cambios locales pendientes. | No |
| `git rev-list --left-right --count HEAD...origin/main` | Ver si HEAD y `origin/main` coinciden. | No |
| `gh pr list --state open --limit 20` | Ver PRs abiertos. | No |

## Comandos de validación

| Comando | Cuándo usarlo | Lectura esperada |
|---|---|---|
| `python -m pytest -q` | Validación general rápida de pruebas. | Todas las pruebas pasan. |
| `make check-fast` | Iteración local rápida S.N.E.-E.C.O. | Tests, validación S.N.E. y rutas confundidas OK. |
| `make eco-check` | Validación operativa amplia E.C.O. | Estado, manifiestos, demos sintéticas, reportes y pytest OK. |
| `make eco-check-clean` | Validar y limpiar resultados generados. | Validación OK y `results/` sin residuos sintéticos temporales. |
| `make eco-validate-synthetic-demos` | Ejecutar y validar demos sintéticas registradas. | Estado global `passed`. |
| `make sne-validation` | Validar el núcleo S.N.E.-E.C.O. | Reporte Markdown/JSON generado. |
| `make sne-state-confusion` | Revisar rutas confundidas. | Rutas confundidas controladas según política actual. |


## Mapa de capacidades actuales

Referencia: `docs/operations/eco-current-capabilities-map.md`.

Este mapa de capacidades actuales sirve para revisar:

- capacidades existentes;
- cómo se validan en el estado operativo actual;
- qué falta para avanzar al siguiente salto operativo sin romper trazabilidad.


## Contrato LAOS para agencia simulada

Referencia: `docs/operations/eco-laos-agency-formula.md`.

LAOS (Libre Albedrío Operativo Simulado) se mantiene como contrato conceptual para futura **agencia simulada** y futura compuerta de **autodesarrollo gobernado** en entorno sintético, sin implicar libre albedrío real ni conciencia.

## LAOS Governance Gate

Referencia: `docs/operations/eco-laos-governance-gate.md`.

LAOS Governance Gate funciona como compuerta sintética de gobernanza para decidir pausa, revisión humana o avance controlado dentro de autodesarrollo gobernado; no activa autonomía real y solo documenta una recomendación operativa bajo límites responsables.

Límites preservados: sin libre albedrío real, sin conciencia, sin datos reales, sin entrenamiento, sin modificación de baseline y sin recalibración de umbrales.

## Agentic Scaffold Protocol

Referencia: `docs/operations/eco-agentic-scaffold-protocol.md`.

Agentic Scaffold Protocol guía la construcción asistida de plantillas, refinamiento y nuevas funciones o módulos candidatos mediante agente generativo bajo revisión humana.

Toda nueva función o módulo candidato debe pasar por documentación, tests, límites responsables y revisión humana antes de incorporarse al estado operativo.

Este protocolo describe autodesarrollo asistido y autodesarrollo gobernado sin autonomía real, sin conciencia y sin libre albedrío real.

## Autonomía Variable

Referencia: `docs/operations/eco-variable-autonomy.md`.

Autonomía Variable define un marco documental de gobernanza para ajustar niveles de independencia operativa en E.C.O., sin autonomía humana, conciencia, ejecución autónoma de herramientas ni libre albedrío real.

## Snapshot de Gobernanza E.C.O.

Referencia: `docs/operations/eco-governance-snapshot.md`.

Snapshot documental, sintético y no clínico del estado actual de gobernanza E.C.O.; resume IAFA, LAOS como alias conceptual/histórico, Autonomía Variable, validación flexible y límites responsables sin implementar lógica funcional.

## Snapshot estable actual

Referencia operativa estable del sprint: `docs/operations/eco-post-governance-snapshot.md`.

Estado esperado del panel operativo:

- dashboard sintético operativo con **8 componentes**;
- governance panel integrado;
- autodesarrollo gobernado activo;
- Suite esperada: **pytest passing**.
- Conteo de referencia reciente: **512 passed** (informativo, no criterio rígido).

Este snapshot mantiene límites responsables: sin datos reales, sin entrenamiento, sin modificación de baseline, sin recalibración de umbrales y sin afirmaciones biomédicas aplicadas.


## Checklist de liberación de sprint

Referencia: `docs/operations/eco-sprint-release-checklist.md`.

Usa esta checklist de liberación en tres momentos obligatorios:

- antes de abrir PR;
- antes de mergear;
- después de mergear.

## Flujo antes de iniciar sprint

```bash
git switch main
git pull --ff-only origin main
make eco-status
python -m pytest -q
git status --short
git rev-list --left-right --count HEAD...origin/main
```

Resultado esperado: `main`, estado `green`, árbol limpio, tests pasando y relación `0 0`.

## Flujo durante sprint

```bash
git branch --show-current
git status --short
make eco-status
python -m pytest -q
```

Es normal que `make eco-status` avise que no estás en `main` si trabajas en una rama de sprint.

## Flujo antes de commit

```bash
git diff --stat
python -m pytest -q
make eco-check-clean
git status --short
```

## Cuándo detenerse

Detente si aparece cualquiera de estos casos:

- `git status --short` muestra archivos que no reconoces.
- `pytest` falla.
- `make eco-check-clean` falla.
- `git pull --ff-only` rechaza actualizar.
- La terminal queda en `>`.
- Git muestra `(END)` y no sabes cómo salir.
- Hay PR abierto pendiente y quieres iniciar otro sprint.

Acciones rápidas:

- Si aparece `(END)`: presiona `q`.
- Si aparece `>`: presiona `Ctrl + C`.
- Si hay cambios inesperados: no uses `reset --hard`; primero diagnostica o respalda.

## Límites responsables

Este índice es operacional y documental.

Permitido: ordenar comandos, explicar estados, orientar validaciones, mejorar onboarding y agregar pruebas documentales.

No permitido en este sprint: entrenar modelos, ingerir datos reales, usar datos sensibles, modificar baseline, recalibrar umbrales o hacer afirmaciones biomédicas aplicadas.

Lista explícita de límites:

- sin entrenamiento;
- sin datos sensibles;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas.
