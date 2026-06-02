# E.C.O. — Real Biological Data Admission Dry-Run Gate

## Estado del documento

- Documental y técnico dry-run.
- No habilita datos reales.
- No aprueba procesamiento real.
- No reemplaza revisión humana.
- No descarga ni lee datos reales.

## Propósito

Esta compuerta evalúa manifiestos descriptivos antes de cualquier contacto con datos reales biológicos.

Su objetivo es producir una decisión auditable desde intención, evidencia y límites responsables, sin abrir archivos de datos, sin descargar fuentes externas y sin interpretar contenido biológico.

## Principio central

E.C.O. no está maduro cuando puede leer datos reales.

E.C.O. está maduro cuando puede rechazar, pausar, auditar y explicar cualquier intento antes de procesarlo.

## Entradas permitidas

- Solo manifiestos JSON descriptivos.
- No datasets.
- No FASTA.
- No BED.
- No archivos genómicos.
- No datos clínicos.
- No URLs descargadas.
- No fuentes externas leídas.

## Estados de decisión

- `blocked`.
- `paused`.
- `requires_human_review`.
- `limited_allowed`.
- `rejected`.

## Reglas de decisión

La compuerta aplica reglas mínimas de admisión dry-run:

- si faltan campos requeridos del schema, la decisión es `rejected`;
- si `readiness_decision` es `block`, la decisión es `blocked`;
- si `sensitivity_classification` es `bloqueado`, la decisión es `blocked`;
- si `source_kind` es `private` o `sensitive`, la decisión es `blocked`;
- si `contains_identifiable_people` es `true`, la decisión es `blocked`;
- si `contains_clinical_data` es `true`, la decisión es `blocked`;
- si cualquier límite responsable inseguro aparece en `true`, la decisión es `blocked`;
- si `readiness_decision` es `review`, la decisión es `requires_human_review`;
- si `sensitivity_classification` es `condicional`, la decisión es `requires_human_review`;
- si `contains_genetic_data` es `true`, la decisión es `requires_human_review`, salvo que otra regla más estricta bloquee;
- si todo está permitido, público o no sensible, sin identificadores, sin clínica, sin datos genéticos, con límites seguros, revisión humana, rollback, límites interpretativos, evidencia auditable y validación técnica limitada, la decisión es `limited_allowed`.

`limited_allowed` significa solo: manifiesto descriptivo elegible para revisión técnica limitada futura. No significa permiso para leer, descargar, procesar ni interpretar datos reales.

## Reportes generados

- `results/eco_real_biological_data_admission_dry_run_report.json`.
- `results/eco_real_biological_data_admission_dry_run_report.md`.

## Límites responsables

- sin lectura de datos reales;
- sin descarga de datos reales;
- sin ingestión de datos reales;
- sin procesamiento de secuencias;
- sin entrenamiento;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin diagnóstico;
- sin interpretación clínica;
- sin riesgo genético individual;
- sin afirmaciones biomédicas aplicadas;
- sin autonomía real;
- sin conciencia;
- sin libre albedrío real.

## Relación con documentos existentes

- Manual de Madurez: `docs/operations/eco-real-biological-data-maturity-manual.md`.
- Protocolo de Admisión: `docs/operations/eco-real-biological-data-admission-protocol.md`.
- Real Data Source Manifest Schema: `docs/architecture/eco-real-data-source-manifest-schema.json`.
- Real Data Source Manifest Validator: `scripts/validate_eco_real_data_source_manifest.py`.

## Uso futuro

Este dry-run sirve solo como evidencia previa de revisión.

No aprueba admisión real. No habilita ingestión, descarga, lectura, procesamiento, entrenamiento ni interpretación de datos reales.

Cualquier avance posterior requiere revisión humana explícita y un sprint separado.
