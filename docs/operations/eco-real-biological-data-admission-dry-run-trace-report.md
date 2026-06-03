# E.C.O. Real Biological Data Admission Dry-Run Trace Report

## Estado del documento

- Documental y técnico.
- no habilita datos reales.
- no aprueba admisión real.
- no reemplaza revisión humana.
- no ejecuta entrenamiento.
- no modifica baseline ni umbrales.

## Propósito

Este reporte resume la decisión seca del Real Biological Data Admission Dry-Run Gate para trazabilidad operativa.

Su función es tomar el JSON generado por la compuerta dry-run y producir una lectura auditable de la decisión, razones, evidencia, límites responsables y acción siguiente, sin ampliar el alcance hacia datos reales.

## Entrada

- Solo lee el JSON generado por el dry-run gate.
- No lee manifiestos directamente.
- No lee datasets.
- No descarga URLs.
- No procesa secuencias.
- No interpreta datos biológicos reales.

## Salidas

- `results/eco_real_biological_data_admission_dry_run_trace_report.json`.
- `results/eco_real_biological_data_admission_dry_run_trace_report.md`.

## Comando operativo

Primero se genera el dry-run:

- `make eco-real-biological-data-admission-dry-run`

Luego se genera el trace report:

- `make eco-real-biological-data-admission-dry-run-trace-report`

El trace report depende del JSON del dry-run. Si el JSON fuente no existe, el comando falla de forma controlada y pide ejecutar primero `make eco-real-biological-data-admission-dry-run`.

## Lectura de decisiones

- `blocked`: la decisión seca bloquea el intento y no habilita admisión real.
- `paused`: la decisión seca pausa el flujo hasta completar evidencia o revisión.
- `requires_human_review`: decisión segura y esperada cuando la compuerta requiere revisión humana antes de cualquier paso futuro.
- `limited_allowed`: elegibilidad documental limitada para revisión técnica futura; no es admisión real.
- `rejected`: la decisión seca rechaza el manifiesto fuente o su reporte y no habilita procesamiento real.

Ninguna decisión reemplaza revisión humana. Ninguna decisión autoriza lectura, descarga, procesamiento o interpretación de datos reales.

## Límites responsables

- sin datos reales;
- sin descarga de datos reales;
- sin lectura de datos reales;
- sin procesamiento de secuencias reales;
- sin interpretación biomédica aplicada;
- sin diagnóstico;
- sin riesgo genético individual;
- sin entrenamiento;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin conciencia;
- sin libre albedrío real;
- sin autonomía real.

## Próximo uso

Este reporte puede servir después como insumo para:

- evidence bundle;
- capabilities report;
- governance report;
- auditoría de decisiones secas.

No aprueba datos reales, no aprueba admisión real y no habilita entrenamiento.
