# Mapa de capacidades actuales de E.C.O.

## Estado operativo actual

E.C.O. se encuentra en estado operativo documental y sintético estable, con `pytest passing` como criterio estable de suite para validar regresión en sprint.

El panel operativo vigente mantiene como referencia explícita:

- dashboard sintético operativo con 8 componentes;
- governance panel integrado;
- checklist de liberación enlazada para pre-PR, pre-merge y post-merge;
- snapshot post-governance como referencia del estado estable.

Snapshot operativo actual:

- main green;
- HEAD = origin/main;
- PR abiertos: ninguno;
- pytest passing como criterio estable;
- criterio de suite: pytest passing, sin conteo rígido como criterio de aceptación;
- public-source-url-admission-guard registrado como capacidad operacional.

## Capacidades documentales

E.C.O. dispone de una base documental operacional activa para:

- onboarding técnico;
- snapshots de estado;
- guías de validación;
- registro de decisiones y protocolos de operación.

Esta capacidad permite distinguir qué piezas existen y cómo se deben operar sin ambigüedad durante un sprint.

## Planos oficiales de orientación E.C.O.

E.C.O. registra dos planos oficiales como capacidades documentales de orientación:

- Plano Técnico: `docs/operations/eco-technical-blueprint.md`.
- Plano Operativo: `docs/operations/eco-operational-blueprint.md`.

El Plano Técnico muestra cómo está construido E.C.O.: arquitectura general, capas, relación bioinspirada, componentes documentales y límites técnicos.

El Plano Operativo muestra cómo trabajar con E.C.O. sin romperlo: entrar, entender, avanzar, pausar, validar, recuperar y cerrar ciclos con trazabilidad.

Ambos planos son capacidades documentales de orientación. No son scripts, no son ejecutables y no son compuertas funcionales.

Estos planos no habilitan datos reales, no entrenan modelos, no modifican baseline, no recalibran umbrales y no hacen afirmaciones biomédicas aplicadas.

También mantienen límites explícitos de agencia: no afirman conciencia, no afirman autonomía real y no afirman libre albedrío real.

## Capacidades de gobernanza

El repositorio integra governance panel y pautas explícitas de control operativo para mantener trazabilidad y límites responsables.

También cuenta con checklist de liberación para controlar hitos antes de abrir PR, antes de mergear y después de mergear.

## Public Source URL Admission Guard

E.C.O. integra **public-source-url-admission-guard** como capacidad de seguridad operacional en `scripts/eco_public_source_guard.py`.

Esta compuerta valida URLs públicas externas antes de que E.C.O. descargue una fuente configurable. Protege la puerta de descarga revisando esquema, dominio, fuente esperada y redirecciones antes de seguirlas.

La política actual permite por defecto solo fuentes públicas esperadas y requiere autorización explícita mediante `--allow-custom-url` para una URL pública no allowlisted.

Esta compuerta no equivale a `real-biological-data-admission-gate`: public-source-url-admission-guard pregunta si la URL externa es pública, permitida, segura y esperada; una compuerta de admisión de datos reales biológicos preguntaría si el dato biológico real puede usarse ética, técnica y responsablemente.

Esta capacidad no autoriza procesamiento de datos reales, no habilita entrenamiento, no habilita diagnóstico, no habilita interpretación clínica, no modifica baseline y no recalibra umbrales.

Toda ampliación de allowlist o cambio de política requiere revisión humana y evidencia auditable.

## Manual de Madurez para Datos Reales Biológicos

E.C.O. enlaza **Manual de Madurez para Datos Reales Biológicos** como capacidad documental de gobernanza en `docs/operations/eco-real-biological-data-maturity-manual.md`.

El manual define el punto de madurez requerido antes de implementar reglas de admisión para datos reales biológicos. Su principio central es: E.C.O. no está maduro cuando puede leer datos reales. E.C.O. está maduro cuando puede rechazar, pausar, auditar y explicar cualquier intento antes de procesarlo.

Esta capacidad ordena criterios de semáforo de madurez, ocho compuertas de madurez, revisión humana, rollback, evidencia auditable y límites interpretativos para futuras fases separadas.

El manual no habilita uso de datos reales y no aprueba procesamiento de datos reales por sí mismo. En esta fase preserva límites responsables: sin datos reales en esta fase, sin entrenamiento, sin modificación de baseline, sin recalibración de umbrales, sin diagnóstico, sin interpretación clínica, sin riesgo genético individual, sin afirmaciones biomédicas aplicadas, sin autonomía real, sin conciencia y sin libre albedrío real.

## Protocolo de Admisión de Datos Reales Biológicos

E.C.O. enlaza **Protocolo de Admisión de Datos Reales Biológicos** como capacidad documental de gobernanza en `docs/operations/eco-real-biological-data-admission-protocol.md`.

El protocolo define una ruta documental previa para evaluar solicitudes futuras de admisión de datos reales biológicos antes de cualquier procesamiento. Opera en relación directa con `docs/operations/eco-real-biological-data-maturity-manual.md`: el Manual de Madurez fija el punto de madurez esperado y el protocolo ordena cómo registrar, revisar, pausar o rechazar una solicitud futura.

La ruta documental contempla solicitud de admisión, identificación de fuente, clasificación de sensibilidad, revisión de licencia o permiso, revisión técnica previa, revisión ética, revisión interpretativa, revisión humana, decisión registrada, evidencia auditable, rollback y rechazo.

El protocolo documenta compuertas mínimas, estados de decisión permitidos, evidencia mínima requerida, condiciones de rechazo obligatorio y validación técnica limitada futura para fases separadas.

Este protocolo no habilita uso de datos reales, no aprueba procesamiento de datos reales por sí mismo y no reemplaza revisión humana.

En esta fase preserva límites responsables: sin datos reales en esta fase, sin ingestión de datos reales, sin entrenamiento, sin modificación de baseline, sin recalibración de umbrales, sin diagnóstico, sin interpretación clínica, sin riesgo genético individual, sin afirmaciones biomédicas aplicadas, sin autonomía real, sin conciencia y sin libre albedrío real.

## Real Biological Data Admission Dry-Run Gate

E.C.O. enlaza **Real Biological Data Admission Dry-Run Gate** como compuerta técnica dry-run en `scripts/run_eco_real_biological_data_admission_dry_run.py`.

La compuerta evalúa manifiestos descriptivos, usa el schema de manifiesto de fuente como referencia estructural y genera reporte auditable en JSON/Markdown.

Documentación operativa: `docs/operations/eco-real-biological-data-admission-dry-run.md`.

Comando operativo estándar:

- `make eco-real-biological-data-admission-dry-run`.

Integración operacional:

- Forma parte de `make eco-check` como validación seca de manifiestos descriptivos.

Salidas generadas:

- `results/eco_real_biological_data_admission_dry_run_report.json`;
- `results/eco_real_biological_data_admission_dry_run_report.md`.

Esta capacidad no lee, no descarga, no procesa y no interpreta datos reales. Tampoco aprueba admisión real, entrenamiento, cambios de baseline, recalibración de umbrales ni afirmaciones biomédicas aplicadas.

Cualquier avance posterior requiere revisión humana, evidencia auditable, rollback y sprint separado.

## Capacidades de dashboard/reportes

El dashboard sintético operativo con 7 componentes está establecido como vista de control del estado operativo.

Además, E.C.O. cuenta con reportes y snapshots (incluyendo snapshot post-governance) para auditar consistencia entre documentación, estado de pruebas y gobernanza.

## Capacidades de demos sintéticas

E.C.O. dispone de demos sintéticas para validar comportamiento del pipeline en condiciones controladas con datos sintéticos.

Estas demos permiten observar el flujo de validación y reporte sin depender de datos reales.

## Capacidades S.N.E.-E.C.O.

S.N.E.-E.C.O. está presente como subsistema operativo para estructurar validaciones del estado entérico computacional y su trazabilidad.

Su capacidad actual se centra en evaluación experimental controlada, reportes verificables y consistencia de suite en entorno sintético.


## Capacidad conceptual LAOS (documental/sintética)

E.C.O. incorpora LAOS — **Libre Albedrío Operativo Simulado** — como capacidad conceptual y documental, definida en `docs/operations/eco-laos-agency-formula.md`.

LAOS se trata como métrica de **agencia simulada** para control operativo en entorno sintético y para uso futuro como gate de **autodesarrollo gobernado**.

Aclaración explícita: LAOS no representa libre albedrío real ni conciencia; es un contrato documental/sintético de evaluación operativa.

E.C.O. también enlaza **LAOS Governance Gate** como compuerta de gobernanza documental en `docs/operations/eco-laos-governance-gate.md`.

Esta compuerta sintética cruza LAOS con estado de validación para recomendar **pausar**, activar **revisión humana** o **avanzar con control**, preservando límites responsables: sin libre albedrío real y sin conciencia.

## Agentic Scaffold Protocol

E.C.O. enlaza **Agentic Scaffold Protocol** como protocolo documental en `docs/operations/eco-agentic-scaffold-protocol.md`.

Este protocolo define autodesarrollo asistido y autodesarrollo gobernado como construcción de plantilla por un agente generativo bajo revisión humana.

El protocolo sirve para estudiar y ordenar nuevas funciones o módulos candidatos sin autonomía real: no implica autonomía real, sin conciencia y sin libre albedrío real.

## Agentic Scaffold Proposal Template

E.C.O. enlaza **Agentic Scaffold Proposal Template** como plantilla operacional en `docs/operations/eco-agentic-scaffold-proposal-template.md`.

Esta plantilla sirve para proponer nuevas funciones o módulos candidatos antes de incorporarlos al estado operativo. Ordena la clasificación inicial como permitido, requiere revisión o bloqueado; archivos mínimos sugeridos; tests contractuales esperados; validaciones requeridas; criterios de revisión humana y decisión final humana.

La plantilla preserva límites responsables: sin autonomía real, sin conciencia, sin libre albedrío real, sin datos reales, sin entrenamiento, sin modificación de baseline, sin recalibración de umbrales y sin afirmaciones biomédicas aplicadas.

## Agentic Scaffold Proposal Example

E.C.O. enlaza **Agentic Scaffold Proposal Example** como ejemplo documental rellenado de propuesta Agentic Scaffold en `docs/operations/eco-agentic-scaffold-proposal-example.md`.

El ejemplo documenta el módulo candidato **Candidate Module: Governed Operational Trace Scaffold**. Es un ejemplo documental, no ejecutable y pendiente de revisión humana; no aprueba integración por sí misma ni implementa función ejecutable.

El ejemplo preserva límites responsables: sin autonomía real, sin conciencia, sin libre albedrío real, sin datos reales, sin entrenamiento, sin modificación de baseline, sin recalibración de umbrales y sin afirmaciones biomédicas aplicadas.

## Agentic Scaffold Proposal Registry

E.C.O. enlaza **Agentic Scaffold Proposal Registry** como registro documental en `docs/operations/eco-agentic-scaffold-proposal-registry.md`.

El registro sirve como catálogo y listado ordenado de propuestas Agentic Scaffold antes de incorporarlas al estado operativo. Conserva por propuesta su estado, clasificación, revisión humana, decisión final humana, validaciones esperadas y límites responsables.

El registro inicial incluye **ASC-PROP-001** para **Candidate Module: Governed Operational Trace Scaffold** como propuesta documental pendiente de revisión humana y decisión final humana; no aprueba integración por sí mismo ni sustituye evaluación humana.

El registro preserva límites responsables: sin autonomía real, sin conciencia, sin libre albedrío real, sin datos reales, sin entrenamiento, sin modificación de baseline, sin recalibración de umbrales y sin afirmaciones biomédicas aplicadas.

## Agentic Scaffold Proposal Registry Report

E.C.O. enlaza **Agentic Scaffold Proposal Registry Report** como reporte documental de solo lectura sobre el registro Agentic Scaffold Proposal Registry.

El reporte lee `docs/operations/eco-agentic-scaffold-proposal-registry.md` y genera evidencia JSON/Markdown sobre propuestas, `proposal_count`, revisión humana requerida y decisión final humana requerida.

Su operación se ejecuta con el target `eco-agentic-scaffold-proposal-registry-report` y el script `scripts/run_eco_agentic_scaffold_proposal_registry_report.py`.

Las salidas generadas son `results/eco_agentic_scaffold_proposal_registry_report.json` y `results/eco_agentic_scaffold_proposal_registry_report.md`.

Este reporte no aprueba integración por sí mismo ni sustituye revisión humana, decisión final humana o evaluación de gobernanza.

El reporte preserva límites responsables: sin autonomía real, sin conciencia, sin libre albedrío real, sin datos reales, sin entrenamiento, sin modificación de baseline, sin recalibración de umbrales y sin afirmaciones biomédicas aplicadas.

## Validaciones disponibles

Validaciones disponibles recomendadas para estado de sprint:

- `python3 -m pytest -q` como validación general;
- `make eco-status` para lectura de estado operativo;
- `make eco-check-clean` para verificación operativa con limpieza de residuos sintéticos.

En este marco, `pytest passing` se utiliza como criterio estable de aceptación técnica del sprint.

## Límites responsables

Límites responsables vigentes:

- uso de datos sintéticos;
- sin datos reales;
- sin entrenamiento;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas.

## Qué NO hace todavía E.C.O.

Actualmente E.C.O. NO hace todavía:

- operación con datos reales en este marco de sprint;
- entrenamiento productivo de modelos;
- recalibración de baseline o umbrales fuera de control de gobernanza;
- generación de afirmaciones biomédicas aplicadas.

## Próximo salto recomendado

Próximo salto recomendado: consolidar una funcionalidad experimental útil mediante un paquete reproducible de evaluación sintética-gobernada que conecte:

1. mapa de capacidades;
2. criterios de validación estable (`pytest passing`);
3. evidencia de dashboard y governance;
4. salida resumida para decisión de avance de sprint.

Este salto debe mantener límites responsables y trazabilidad de decisiones sin introducir datos reales ni entrenamiento.
