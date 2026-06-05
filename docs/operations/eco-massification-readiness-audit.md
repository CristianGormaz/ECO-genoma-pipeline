# E.C.O. massification readiness audit

Estado: audit_only.

## Gate operativo

- No refactor todavia: make check-fast debe permanecer verde antes de tocar streaming.
- Este reporte no cambia semantica de pipeline, no mueve validadores y no introduce checkpoint real.

## Resumen

- schema_version: `eco_massification_readiness_audit_v1`
- generated_at: `2026-06-05T00:06:03.799192+00:00`
- total_findings: `17`
- critical: `1`
- high: `8`
- medium: `5`
- low: `0`
- false_positive: `1`
- intentional_demo: `2`

## Hallazgos

| severity | rule_id | path | line | summary |
|---|---|---|---|---|
| critical | read_text_full_file_ingest | src/eco_core/ingestion.py | 48 | La ingesta central lee el archivo completo en memoria antes de construir el paquete. |
  Evidencia: file_path.read_text(encoding="utf-8")
  Recomendacion: Migrar a lectura incremental o derivar a parsers streaming en un sprint separado.
| high | missing_resume_checkpoint_contract | scripts/run_eco_demo_pipeline.py | 1 | No hay contrato explicito de checkpoint/resume en los entrypoints de corrida larga auditados. |
  Evidencia: scripts/run_eco_demo_pipeline.py, scripts/run_sne_eco_state_dataset.py, scripts/run_sne_eco_sensitive_source_registry.py, scripts/run_sne_eco_empirical_train_eval_split.py
  Recomendacion: Agregar checkpoint.json, JSONL incremental y resume en un micro-sprint dedicado.
| high | streaming_candidate::parse_fasta | src/eco_bed_to_fasta.py | 71 | FASTA completo se carga en un diccionario antes de procesar regiones. |
  Evidencia: Funcion detectada: parse_fasta
  Recomendacion: Migrar a iter_fasta_records(path) en un sprint posterior.
| high | streaming_candidate::parse_bed | src/eco_bed_to_fasta.py | 153 | BED completo se carga en una lista antes de generar FASTA. |
  Evidencia: Funcion detectada: parse_bed
  Recomendacion: Migrar a iter_bed_records(path) y escribir FASTA incrementalmente.
| high | processed_packets_without_memory_policy | src/eco_core/enteric_orchestrator.py | 52 | EntericSystem conserva processed_packets sin una politica explicita de memoria o flush. |
  Evidencia: Inicializacion en linea 52; append en linea 234.
  Recomendacion: Definir modo demo vs batch, buffer acotado y exportacion incremental de trazas.
| high | feedback_materializes_all_packets | src/eco_core/feedback.py | 32 | El resumen de feedback materializa todos los paquetes antes de resumir. |
  Evidencia: packets
  Recomendacion: Construir el resumen con acumuladores incrementales.
| high | homeostasis_materializes_all_packets | src/eco_core/homeostasis.py | 54 | La snapshot homeostatica convierte todo el iterable de paquetes a lista. |
  Evidencia: packets
  Recomendacion: Aceptar iteradores y agregar contadores streaming en un sprint dedicado.
| high | streaming_candidate::parse_fasta | src/eco_motif_analysis.py | 77 | El analisis de motivos requiere todo el FASTA en memoria. |
  Evidencia: Funcion detectada: parse_fasta
  Recomendacion: Separar parser iterativo del calculo por secuencia.
| high | streaming_candidate::parse_labeled_sequences_tsv | src/eco_sequence_classifier.py | 43 | El clasificador lee todas las secuencias etiquetadas a una lista. |
  Evidencia: Funcion detectada: parse_labeled_sequences_tsv
  Recomendacion: Agregar iterador TSV y feature extraction por lotes/chunks.
| medium | streaming_candidate::bed_to_fasta | src/eco_bed_to_fasta.py | 201 | La conversion BED->FASTA devuelve una lista completa de registros. |
  Evidencia: Funcion detectada: bed_to_fasta
  Recomendacion: Permitir escritor incremental de FASTA o batch por chunks.
| medium | streaming_candidate::build_adaptive_state_rows | src/eco_core/adaptive_state_dataset.py | 91 | El dataset adaptativo se construye como lista completa de filas. |
  Evidencia: Funcion detectada: build_adaptive_state_rows
  Recomendacion: Separar recoleccion incremental y exportacion final.
| medium | adaptive_state_rows_materialized_for_rendering | src/eco_core/adaptive_state_dataset.py | 117 | El dataset adaptativo convierte filas a lista completa para renderizar. |
  Evidencia: rows
  Recomendacion: Separar construccion del dataset de la renderizacion final.
| medium | packet_trace_materializes_all_traces | src/eco_core/packet_trace.py | 110 | La exportacion de trazas exige tener la coleccion completa en memoria. |
  Evidencia: traces
  Recomendacion: Agregar un escritor incremental JSONL/Markdown en un sprint posterior.
| medium | streaming_candidate::extract_feature_map | src/eco_sequence_classifier.py | 125 | El mapa completo de features se materializa antes del uso posterior. |
  Evidencia: Funcion detectada: extract_feature_map
  Recomendacion: Permitir recorrido incremental o chunked para evaluaciones largas.
| false_positive | tests_and_docs_read_text_are_not_massification_blockers | tests/ | - | Hay lecturas completas en tests/documentacion, pero no pertenecen al flujo productivo. |
  Evidencia: tests/test_adaptive_router_final_arbitration.py:62, tests/test_adaptive_router_final_arbitration.py:105, tests/test_adaptive_state_foundation_doc.py:8, tests/test_build_eco_operational_manifest.py:74, tests/test_build_eco_operational_manifest.py:63, +426 mas
  Recomendacion: Mantenerlas fuera del alcance productivo y no tratarlas como bloqueadores de streaming.
| intentional_demo | demo_scripts_may_materialize_small_payloads | scripts/ | - | Existen demos sinteticas que materializan contenido completo por simplicidad. |
  Evidencia: scripts/export_eco_demo_markdown.py:33, scripts/review_eco_demo_report.py:32, scripts/run_eco_synthetic_demo_comparison_report.py:25, scripts/run_eco_synthetic_demos_suite_report.py:13, scripts/run_eco_synthetic_operational_dashboard.py:122, +3 mas
  Recomendacion: Documentar estas rutas como demo-only y no reutilizarlas como pipeline productivo.
| intentional_demo | streaming_candidate::run_demo_pipeline | scripts/run_eco_demo_pipeline.py | 80 | El pipeline demo materializa referencia, regiones, FASTA y paquetes por simplicidad. |
  Evidencia: Funcion detectada: run_demo_pipeline
  Recomendacion: Mantenerlo como demo-only y no reutilizarlo como base de masificacion productiva.

## Micro-sprints recomendados

- Micro-sprint 1: auditoria anti-streaming reproducible y reporte de hallazgos.
- Micro-sprint 2: centralizacion de validacion ADN/FASTA/BED.
- Micro-sprint 3: migracion de parsers a generadores.
- Micro-sprint 4: procesamiento batch por chunks e incremental writers.
- Micro-sprint 5: politica de memoria para EntericSystem.
- Micro-sprint 6: checkpoint.json + JSONL incremental + resume.
- Micro-sprint 7: limpieza final de contratos e imports auxiliares.

## Limites responsables

- No refactor todavia: primero auditar y estabilizar el baseline operativo.
- No tocar parsers FASTA/BED ni ingestion.py en este sprint de auditoria.
- No tocar EntericSystem.processed_packets ni EcoPacket en esta fase.
- No mover validadores ni crear checkpoint real todavia.
- No usar datos reales, no entrenar modelos, no modificar baseline ni recalibrar umbrales.

## Comando sugerido

`python scripts/run_eco_streaming_audit.py --output-json /tmp/eco_streaming_audit.json --output-md docs/operations/eco-massification-readiness-audit.md`
