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

## Planos oficiales de orientación

Referencia técnica: `docs/operations/eco-technical-blueprint.md`.

Referencia operativa: `docs/operations/eco-operational-blueprint.md`.

El Plano Técnico sirve para entender la construcción de E.C.O.: capas, límites, componentes y relación bioinspirada.

El Plano Operativo sirve para decidir cómo entrar, avanzar, pausar, validar, recuperar y cerrar ciclos de trabajo sin romper el sistema.

Estos planos son documentos de orientación. No son ejecutables, no son scripts, no son compuertas funcionales y no reemplazan comandos reales ni validaciones reales.


## Public Source URL Admission Guard

Referencia funcional: `scripts/eco_public_source_guard.py`.

Referencia de tests: `tests/test_eco_public_source_url_admission_guard.py`.

public-source-url-admission-guard funciona como compuerta de seguridad operacional para URLs públicas externas configurables antes de descargar datos desde internet.

La compuerta protege esquema, dominio, fuente esperada y redirecciones. Por defecto solo admite fuentes públicas allowlisted y exige `--allow-custom-url` para una URL pública personalizada revisada.

No equivale a `real-biological-data-admission-gate`: esta compuerta protege la fuente de descarga, no aprueba el uso ético, técnico o interpretativo de datos biológicos reales.

Límites preservados: no autoriza procesamiento de datos reales, no habilita entrenamiento, no habilita diagnóstico, no habilita interpretación clínica, no modifica baseline y no recalibra umbrales.

Toda ampliación de allowlist o cambio de política requiere revisión humana.


## Manual de Madurez para Datos Reales Biológicos

Referencia: `docs/operations/eco-real-biological-data-maturity-manual.md`.

Manual de Madurez para Datos Reales Biológicos funciona como documento operativo de gobernanza para definir el punto previo a futuras reglas de admisión de datos reales biológicos.

El manual no habilita uso de datos reales y no aprueba procesamiento de datos reales por sí mismo. Cualquier avance futuro requiere revisión humana y evidencia auditable.

Sirve como base documental para futuras fases separadas: Real Biological Data Manifest Schema, Real Biological Data Admission Dry-Run Gate y Real Biological Data Rollback Report.

Estas fases futuras no quedan aprobadas por este enlace.


## Protocolo de Admisión de Datos Reales Biológicos

Referencia: `docs/operations/eco-real-biological-data-admission-protocol.md`.

Protocolo de Admisión de Datos Reales Biológicos funciona como documento operativo de gobernanza para ordenar solicitudes futuras antes de cualquier uso de datos reales biológicos.

Se relaciona con el Manual de Madurez para Datos Reales Biológicos: el manual define el punto de madurez esperado y el protocolo registra la ruta documental de revisión humana, evidencia auditable, decisión, rollback o rechazo.

Sirve como base documental para futuras fases separadas: Real Biological Data Admission Template, Real Biological Data Admission Example, Real Biological Data Manifest Schema, Real Biological Data Admission Dry-Run Gate y Real Biological Data Rollback Report.

Esas fases futuras no quedan aprobadas por este enlace. El protocolo no habilita uso de datos reales, no aprueba procesamiento de datos reales por sí mismo y no reemplaza revisión humana.


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

## Agentic Scaffold Proposal Template

Referencia: `docs/operations/eco-agentic-scaffold-proposal-template.md`.

Agentic Scaffold Proposal Template complementa el Agentic Scaffold Protocol: ordena propuestas de nuevas funciones o módulos candidatos antes de integrarlas al estado operativo.

La plantilla registra clasificación inicial como permitido, requiere revisión o bloqueado; archivos mínimos sugeridos; tests contractuales esperados; validaciones requeridas; revisión humana y decisión final humana.

No aprueba integración por sí misma y preserva límites responsables: sin autonomía real, sin conciencia y sin libre albedrío real.

## Agentic Scaffold Proposal Example

Referencia: `docs/operations/eco-agentic-scaffold-proposal-example.md`.

Agentic Scaffold Proposal Example complementa la Agentic Scaffold Proposal Template mostrando un ejemplo rellenado de módulo candidato: **Candidate Module: Governed Operational Trace Scaffold**.

El ejemplo es documental, no ejecutable y pendiente de revisión humana. No aprueba integración por sí misma; cualquier incorporación requiere revisión humana y decisión final humana.

## Agentic Scaffold Proposal Registry

Referencia: `docs/operations/eco-agentic-scaffold-proposal-registry.md`.

Agentic Scaffold Proposal Registry funciona como catálogo y listado ordenado de propuestas Agentic Scaffold antes de integrarlas al estado operativo.

El registro conserva estado, clasificación, revisión humana y decisión final humana por propuesta. No aprueba integración por sí mismo; cualquier incorporación requiere revisión humana y decisión final humana.

El primer registro es **ASC-PROP-001**, asociado a **Candidate Module: Governed Operational Trace Scaffold**.

Comando de reporte de solo lectura: `make eco-agentic-scaffold-proposal-registry-report`.

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
- public-source-url-admission-guard registrado;
- main green;
- HEAD = origin/main;
- sin PR abiertos;
- Suite esperada: **pytest passing**.
- Criterio de suite: **pytest passing**; no usar conteo rígido como criterio de aceptación.

Este snapshot mantiene límites responsables: sin datos reales, sin entrenamiento, sin modificación de baseline, sin recalibración de umbrales y sin afirmaciones biomédicas aplicadas.


## Ciclo experimental gobernado

Referencia: `docs/operations/eco-governed-experimental-cycle.md`.

Runner:

```bash
.venv/bin/python scripts/run_eco_governed_experimental_cycle.py
```

Salidas:

- `results/eco_governed_experimental_cycle.json`
- `results/eco_governed_experimental_cycle.md`

El ciclo conecta madurez por fase, admisión gobernada, gates, riesgos, rollback visible, límites responsables y decisión final `advance | pause | review | reject`.

Límites preservados: sin datos reales, sin entrenamiento, sin datos sensibles, sin diagnóstico, sin interpretación clínica, sin cambios de baseline, sin recalibración de umbrales, sin conciencia y sin libre albedrío real.


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
