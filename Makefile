.PHONY: install-dev test validate sne-validation sne-state-dataset sne-state-baseline sne-state-holdout sne-state-coverage sne-state-confusion enteric-report enteric-html open-enteric-html demo review report pipeline public-demo variant-demo clinvar-sample clinvar-html clinvar-charts preview-clinvar inspect-clinvar-json open-clinvar-html open-clinvar-charts dataset-audit classifier-baseline classifier-baseline-v2 classifier-baseline-v3 classifier-html classifier-html-v2 classifier-html-v3 classifier-compare classifier-repeated-eval classifier-sensitivity embedding-placeholder embedding-repeated-eval model-decision open-classifier-html open-classifier-html-v2 open-classifier-html-v3 open-classifier-comparison open-classifier-repeated-eval open-classifier-sensitivity open-embedding-placeholder open-embedding-repeated-eval open-model-decision portfolio-demo check clean embedding-semireal open-embedding-semireal embedding-semireal-repeated-eval open-embedding-semireal-repeated-eval difficulty-eval open-difficulty-eval hybrid-router-eval open-hybrid-router-eval confidence-router-eval open-confidence-router-eval confidence-router-calibrated-eval open-confidence-router-calibrated-eval adaptive-router-predict-demo open-adaptive-router-predict-demo adaptive-router-predict open-adaptive-router-predict adaptive-router-batch open-adaptive-router-batch sne-recurrence-audit sne-observability-dashboard sne-neurogastro-context sne-neurogastro-summary sne-neurogastro-pipeline

PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

SEQUENCE ?=
SEQUENCE_ID ?= custom_adaptive_router
THRESHOLD ?= 0.20
EMBEDDING_K ?= 4
DIMENSIONS ?= 128
INPUT ?= examples/eco_labeled_sequences.tsv
ADAPTIVE_OUTPUT_PREFIX ?= eco_adaptive_router_prediction_custom
BATCH_INPUT ?= examples/demo_adaptive_router_batch.tsv
BATCH_OUTPUT_PREFIX ?= eco_adaptive_router_batch_report

install-dev:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

test:
	$(PY) -m pytest -q

validate:
	$(PY) scripts/run_eco_validation.py

sne-validation:
	$(PY) scripts/run_sne_eco_validation.py --output-md results/sne_eco_validation_report.md --output-json results/sne_eco_validation_report.json

sne-state-dataset:
	$(PY) scripts/run_sne_eco_state_dataset.py --output-json results/sne_eco_state_dataset.json --output-tsv results/sne_eco_state_dataset.tsv

sne-state-baseline:
	$(PY) scripts/run_sne_eco_state_baseline.py --output-json results/sne_eco_state_baseline_report.json --output-md results/sne_eco_state_baseline_report.md

sne-state-holdout:
	$(PY) scripts/run_sne_eco_state_holdout.py --output-json results/sne_eco_state_holdout_report.json --output-md results/sne_eco_state_holdout_report.md

sne-state-coverage:
	$(PY) scripts/run_sne_eco_state_coverage.py --extended --output-json results/sne_eco_state_coverage_report.json --output-md results/sne_eco_state_coverage_report.md

sne-state-confusion:
	$(PY) scripts/run_sne_eco_state_confusion.py --extended --output-json results/sne_eco_state_confusion_report.json --output-md results/sne_eco_state_confusion_report.md

sne-recurrence-audit:
	$(PY) scripts/run_sne_eco_recurrence_audit.py

sne-observability-dashboard: sne-state-confusion sne-recurrence-audit
	$(PY) scripts/run_sne_eco_observability_dashboard.py

sne-neurogastro-context: sne-state-dataset sne-observability-dashboard
	$(PY) scripts/run_sne_eco_neurogastro_context_report.py

sne-neurogastro-summary: sne-neurogastro-context
	$(PY) scripts/run_sne_eco_neurogastro_pipeline_summary.py

sne-neurogastro-pipeline: sne-neurogastro-summary
	@echo ""
	@echo "S.N.E.-E.C.O. neurogastro pipeline ready"
	@echo "========================================"
	@echo "Reportes generados:"
	@echo "- results/sne_eco_state_dataset.json"
	@echo "- results/sne_eco_state_dataset.tsv"
	@echo "- results/sne_eco_state_confusion_report.json"
	@echo "- results/sne_eco_state_confusion_report.md"
	@echo "- results/sne_eco_recurrence_audit.json"
	@echo "- results/sne_eco_recurrence_audit.md"
	@echo "- results/sne_eco_observability_dashboard.json"
	@echo "- results/sne_eco_observability_dashboard.md"
	@echo "- results/sne_eco_neurogastro_context_report.json"
	@echo "- results/sne_eco_neurogastro_context_report.md"
	@echo "- results/sne_eco_neurogastro_pipeline_summary.json"
	@echo "- results/sne_eco_neurogastro_pipeline_summary.md"

enteric-report:
	$(PY) scripts/run_eco_enteric_report.py

enteric-html: enteric-report
	$(PY) scripts/export_eco_enteric_html.py

open-enteric-html:
	@xdg-open results/eco_enteric_system_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML entérico. Revisa: results/eco_enteric_system_report.html"

demo:
	$(PY) scripts/run_eco_demo_pipeline.py

review:
	$(PY) scripts/review_eco_demo_report.py

report:
	$(PY) scripts/export_eco_demo_markdown.py

pipeline:
	$(PY) scripts/run_eco_pipeline.py --bed examples/demo_regions.bed --reference examples/tiny_reference.fa --output-dir results --prefix eco_custom_demo

public-demo:
	$(PY) scripts/run_eco_public_chrM_report.py

variant-demo:
	$(PY) scripts/run_eco_variant_demo.py

clinvar-sample:
	$(PY) scripts/run_eco_clinvar_sample_report.py

clinvar-charts:
	$(PY) scripts/export_eco_clinvar_charts.py

clinvar-html:
	$(PY) scripts/export_eco_variant_html.py

dataset-audit:
	$(PY) scripts/audit_eco_labeled_dataset.py

classifier-baseline:
	$(PY) scripts/run_eco_classifier_baseline.py --feature-mode motif --output-json results/eco_classifier_baseline_report.json --output-md results/eco_classifier_baseline_report.md

classifier-baseline-v2:
	$(PY) scripts/run_eco_classifier_baseline.py --feature-mode motif_kmer --kmer-k 2 --normalize-features --output-json results/eco_classifier_baseline_v2_report.json --output-md results/eco_classifier_baseline_v2_report.md

classifier-baseline-v3:
	$(PY) scripts/run_eco_classifier_baseline.py --feature-mode motif_kmer --kmer-k 3 --normalize-features --output-json results/eco_classifier_baseline_v3_report.json --output-md results/eco_classifier_baseline_v3_report.md

classifier-html:
	$(PY) scripts/export_eco_classifier_html.py --input-json results/eco_classifier_baseline_report.json --output-html results/eco_classifier_baseline_report.html

classifier-html-v2:
	$(PY) scripts/export_eco_classifier_html.py --input-json results/eco_classifier_baseline_v2_report.json --output-html results/eco_classifier_baseline_v2_report.html

classifier-html-v3:
	$(PY) scripts/export_eco_classifier_html.py --input-json results/eco_classifier_baseline_v3_report.json --output-html results/eco_classifier_baseline_v3_report.html

classifier-compare:
	$(PY) scripts/compare_eco_classifier_baselines.py

classifier-repeated-eval:
	$(PY) scripts/run_eco_classifier_repeated_eval.py

classifier-sensitivity:
	$(PY) scripts/run_eco_classifier_sensitivity.py

embedding-placeholder:
	$(PY) scripts/run_eco_embedding_placeholder.py

embedding-repeated-eval:
	$(PY) scripts/run_eco_embedding_repeated_eval.py

model-decision: classifier-compare classifier-repeated-eval embedding-repeated-eval
	$(PY) scripts/run_eco_model_decision_report.py

preview-clinvar:
	@sed -n '1,180p' results/eco_clinvar_sample_report.md

inspect-clinvar-json:
	@$(PY) -m json.tool results/eco_clinvar_sample_report.json | head -80

open-clinvar-html:
	@xdg-open results/eco_clinvar_sample_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_clinvar_sample_report.html"

open-clinvar-charts:
	@xdg-open results/eco_clinvar_sample_charts/index.html >/dev/null 2>&1 || echo "No se pudo abrir el índice. Revisa: results/eco_clinvar_sample_charts/index.html"

open-classifier-html:
	@xdg-open results/eco_classifier_baseline_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_classifier_baseline_report.html"

open-classifier-html-v2:
	@xdg-open results/eco_classifier_baseline_v2_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_classifier_baseline_v2_report.html"

open-classifier-html-v3:
	@xdg-open results/eco_classifier_baseline_v3_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_classifier_baseline_v3_report.html"

open-classifier-comparison:
	@xdg-open results/eco_classifier_comparison_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_classifier_comparison_report.html"

open-classifier-repeated-eval:
	@xdg-open results/eco_classifier_repeated_eval_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_classifier_repeated_eval_report.html"

open-classifier-sensitivity:
	@xdg-open results/eco_classifier_sensitivity_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_classifier_sensitivity_report.html"

open-embedding-placeholder:
	@xdg-open results/eco_embedding_placeholder_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_embedding_placeholder_report.html"

open-embedding-repeated-eval:
	@xdg-open results/eco_embedding_repeated_eval_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_embedding_repeated_eval_report.html"

open-model-decision:
	@xdg-open results/eco_model_decision_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_model_decision_report.html"

portfolio-demo: check sne-validation sne-state-dataset sne-state-baseline sne-state-holdout sne-state-coverage sne-state-confusion enteric-html adaptive-router-batch classifier-html classifier-html-v2 classifier-html-v3 classifier-repeated-eval classifier-sensitivity embedding-placeholder embedding-repeated-eval model-decision clinvar-sample clinvar-charts clinvar-html
	@echo ""
	@echo "E.C.O. PORTFOLIO DEMO READY"
	@echo "==========================="
	@echo "Reportes principales generados:"
	@echo "- results/sne_eco_validation_report.md"
	@echo "- results/sne_eco_validation_report.json"
	@echo "- results/sne_eco_state_dataset.json"
	@echo "- results/sne_eco_state_dataset.tsv"
	@echo "- results/sne_eco_state_baseline_report.json"
	@echo "- results/sne_eco_state_baseline_report.md"
	@echo "- results/sne_eco_state_holdout_report.json"
	@echo "- results/sne_eco_state_holdout_report.md"
	@echo "- results/sne_eco_state_coverage_report.json"
	@echo "- results/sne_eco_state_coverage_report.md"
	@echo "- results/sne_eco_state_confusion_report.json"
	@echo "- results/sne_eco_state_confusion_report.md"
	@echo "- results/eco_enteric_system_report.md"
	@echo "- results/eco_enteric_system_report.html"
	@echo "- results/eco_adaptive_router_prediction_demo.md"
	@echo "- results/eco_adaptive_router_prediction_demo.html"
	@echo "- results/eco_adaptive_router_batch_report.md"
	@echo "- results/eco_adaptive_router_batch_report.html"
	@echo "- results/eco_demo_pipeline_report.md"
	@echo "- results/eco_custom_demo_report.md"
	@echo "- results/eco_variant_demo_report.md"
	@echo "- results/eco_dataset_audit_report.md"
	@echo "- results/eco_classifier_baseline_report.md"
	@echo "- results/eco_classifier_baseline_report.html"
	@echo "- results/eco_classifier_baseline_v2_report.md"
	@echo "- results/eco_classifier_baseline_v2_report.html"
	@echo "- results/eco_classifier_baseline_v3_report.md"
	@echo "- results/eco_classifier_baseline_v3_report.html"
	@echo "- results/eco_classifier_comparison_report.md"
	@echo "- results/eco_classifier_comparison_report.html"
	@echo "- results/eco_classifier_repeated_eval_report.md"
	@echo "- results/eco_classifier_repeated_eval_report.html"
	@echo "- results/eco_classifier_sensitivity_report.md"
	@echo "- results/eco_classifier_sensitivity_report.html"
	@echo "- results/eco_embedding_placeholder_report.md"
	@echo "- results/eco_embedding_placeholder_report.html"
	@echo "- results/eco_embedding_repeated_eval_report.md"
	@echo "- results/eco_embedding_repeated_eval_report.html"
	@echo "- results/eco_model_decision_report.md"
	@echo "- results/eco_model_decision_report.html"
	@echo "- results/eco_clinvar_sample_report.md"
	@echo "- results/eco_clinvar_sample_report.html"
	@echo "- results/eco_clinvar_sample_charts/index.html"
	@echo ""
	@echo "Documentos de apoyo:"
	@echo "- docs/sne-eco-v1-indice-demo.md"
	@echo "- docs/guia-validacion-sne-eco.md"
	@echo "- docs/guia-dataset-adaptativo-eco.md"
	@echo "- docs/guia-baseline-adaptativo-eco.md"
	@echo "- docs/guia-evaluacion-holdout-eco.md"
	@echo "- docs/guia-diagnostico-cobertura-eco.md"
	@echo "- docs/guia-rutas-confundidas-eco.md"
	@echo "- docs/caso-estudio-portafolio-eco.md"
	@echo "- docs/guia-reporte-enterico-eco.md"
	@echo "- docs/guia-router-adaptativo-eco.md"
	@echo "- docs/guia-router-adaptativo-batch-eco.md"
	@echo "- docs/guia-interpretacion-variantes-eco.md"
	@echo "- docs/uso-responsable-datos-eco.md"
	@echo "- docs/modulo-sne-eco-digestion-bioinspirada.md"
	@echo "- docs/nota-tecnica-v3-vs-v2.md"
	@echo ""
	@echo "Validar S.N.E.-E.C.O.: make sne-validation"
	@echo "Generar dataset adaptativo: make sne-state-dataset"
	@echo "Generar baseline adaptativo: make sne-state-baseline"
	@echo "Evaluar holdout adaptativo: make sne-state-holdout"
	@echo "Diagnosticar cobertura adaptativa: make sne-state-coverage"
	@echo "Analizar rutas confundidas: make sne-state-confusion"
	@echo "Abrir HTML entérico: make open-enteric-html"
	@echo "Abrir predicción adaptativa: make open-adaptive-router-predict-demo"
	@echo "Abrir batch adaptativo: make open-adaptive-router-batch"
	@echo "Vista rápida Markdown: make preview-clinvar"
	@echo "Inspección JSON: make inspect-clinvar-json"
	@echo "Abrir HTML ClinVar: make open-clinvar-html"
	@echo "Abrir gráficos ClinVar: make open-clinvar-charts"
	@echo "Abrir HTML clasificador v1: make open-classifier-html"
	@echo "Abrir HTML clasificador v2: make open-classifier-html-v2"
	@echo "Abrir HTML clasificador v3: make open-classifier-html-v3"
	@echo "Abrir comparación clasificadores: make open-classifier-comparison"
	@echo "Abrir evaluación repetida: make open-classifier-repeated-eval"
	@echo "Abrir sensibilidad del clasificador: make open-classifier-sensitivity"
	@echo "Abrir embedding placeholder: make open-embedding-placeholder"
	@echo "Abrir evaluación repetida embedding: make open-embedding-repeated-eval"
	@echo "Abrir decisión de modelos: make open-model-decision"

check: test validate enteric-report demo review report pipeline variant-demo dataset-audit classifier-baseline classifier-baseline-v2 classifier-baseline-v3 classifier-compare embedding-placeholder embedding-repeated-eval model-decision adaptive-router-predict-demo adaptive-router-batch

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f results/test_*.fa results/test_*.json results/test_*.csv
	rm -f results/sne_eco_validation_report.json results/sne_eco_validation_report.md
	rm -f results/sne_eco_state_dataset.json results/sne_eco_state_dataset.tsv
	rm -f results/sne_eco_state_baseline_report.json results/sne_eco_state_baseline_report.md
	rm -f results/sne_eco_state_holdout_report.json results/sne_eco_state_holdout_report.md
	rm -f results/sne_eco_state_coverage_report.json results/sne_eco_state_coverage_report.md
	rm -f results/sne_eco_state_confusion_report.json results/sne_eco_state_confusion_report.md
	rm -f results/eco_enteric_system_report.json results/eco_enteric_system_report.md results/eco_enteric_system_report.html
	rm -f results/eco_adaptive_router_prediction_demo.json results/eco_adaptive_router_prediction_demo.md results/eco_adaptive_router_prediction_demo.html
	rm -f results/eco_adaptive_router_prediction_custom.json results/eco_adaptive_router_prediction_custom.md results/eco_adaptive_router_prediction_custom.html
	rm -f results/eco_adaptive_router_batch_report.json results/eco_adaptive_router_batch_report.md results/eco_adaptive_router_batch_report.html
	rm -f results/eco_demo_pipeline.fa results/eco_demo_pipeline_report.json results/eco_demo_pipeline_report.md
	rm -f results/eco_custom_demo.fa results/eco_custom_demo_report.json results/eco_custom_demo_report.md
	rm -f results/eco_public_chrM.fa results/eco_public_chrM_report.json results/eco_public_chrM_interpretive_report.md
	rm -f results/eco_variant_demo_report.json results/eco_variant_demo_report.md
	rm -f results/eco_dataset_audit_report.json results/eco_dataset_audit_report.md
	rm -f results/eco_classifier_baseline_report.json results/eco_classifier_baseline_report.md results/eco_classifier_baseline_report.html
	rm -f results/eco_classifier_baseline_v2_report.json results/eco_classifier_baseline_v2_report.md results/eco_classifier_baseline_v2_report.html
	rm -f results/eco_classifier_baseline_v3_report.json results/eco_classifier_baseline_v3_report.md results/eco_classifier_baseline_v3_report.html
	rm -f results/eco_classifier_comparison_report.md results/eco_classifier_comparison_report.html
	rm -f results/eco_classifier_repeated_eval_report.json results/eco_classifier_repeated_eval_report.md results/eco_classifier_repeated_eval_report.html
	rm -f results/eco_classifier_sensitivity_report.json results/eco_classifier_sensitivity_report.md results/eco_classifier_sensitivity_report.html
	rm -f results/eco_embedding_placeholder_report.json results/eco_embedding_placeholder_report.md results/eco_embedding_placeholder_report.html
	rm -f results/eco_embedding_repeated_eval_report.json results/eco_embedding_repeated_eval_report.md results/eco_embedding_repeated_eval_report.html
	rm -f results/eco_model_decision_report.md results/eco_model_decision_report.html
	rm -f results/eco_clinvar_sample.tsv results/eco_clinvar_sample_report.json results/eco_clinvar_sample_report.md results/eco_clinvar_sample_report.html
	rm -rf results/eco_clinvar_sample_charts

embedding-semireal:
	$(PY) scripts/run_eco_embedding_semireal.py --embedding-k 4 --dimensions 128 --output-json results/eco_embedding_semireal_report.json --output-md results/eco_embedding_semireal_report.md --output-html results/eco_embedding_semireal_report.html

open-embedding-semireal:
	@xdg-open results/eco_embedding_semireal_report.html >/dev/null 2>&1 || echo "No se pudo abrir: results/eco_embedding_semireal_report.html"

embedding-semireal-repeated-eval:
	$(PY) scripts/run_eco_embedding_semireal_repeated_eval.py --embedding-k 4 --dimensions 128 --output-json results/eco_embedding_semireal_repeated_eval_report.json --output-md results/eco_embedding_semireal_repeated_eval_report.md --output-html results/eco_embedding_semireal_repeated_eval_report.html

open-embedding-semireal-repeated-eval:
	@xdg-open results/eco_embedding_semireal_repeated_eval_report.html >/dev/null 2>&1 || echo "No se pudo abrir: results/eco_embedding_semireal_repeated_eval_report.html"

difficulty-eval:
	$(PY) scripts/run_eco_difficulty_eval.py --repeats 50 --embedding-k 4 --dimensions 128 --output-json results/eco_difficulty_eval_report.json --output-md results/eco_difficulty_eval_report.md --output-html results/eco_difficulty_eval_report.html

open-difficulty-eval:
	@xdg-open results/eco_difficulty_eval_report.html >/dev/null 2>&1 || true

hybrid-router-eval:
	$(PY) scripts/run_eco_hybrid_router_eval.py --repeats 50 --embedding-k 4 --dimensions 128 --output-json results/eco_hybrid_router_eval_report.json --output-md results/eco_hybrid_router_eval_report.md --output-html results/eco_hybrid_router_eval_report.html

open-hybrid-router-eval:
	@xdg-open results/eco_hybrid_router_eval_report.html >/dev/null 2>&1 || true

confidence-router-eval:
	$(PY) scripts/run_eco_confidence_router_eval.py --repeats 50 --embedding-k 4 --dimensions 128 --output-json results/eco_confidence_router_eval_report.json --output-md results/eco_confidence_router_eval_report.md --output-html results/eco_confidence_router_eval_report.html

open-confidence-router-eval:
	@xdg-open results/eco_confidence_router_eval_report.html >/dev/null 2>&1 || true

confidence-router-calibrated-eval:
	$(PY) scripts/run_eco_confidence_router_calibrated_eval.py --repeats 50 --embedding-k 4 --dimensions 128 --output-json results/eco_confidence_router_calibrated_eval_report.json --output-md results/eco_confidence_router_calibrated_eval_report.md --output-html results/eco_confidence_router_calibrated_eval_report.html

open-confidence-router-calibrated-eval:
	@xdg-open results/eco_confidence_router_calibrated_eval_report.html >/dev/null 2>&1 || true

adaptive-router-predict-demo:
	$(PY) scripts/run_eco_adaptive_router_predict.py --sequence ACGTCCAATGGTATAAAGGCGGGCGGAATAAAGTAC --sequence-id demo_adaptive_router --threshold 0.20 --embedding-k 4 --dimensions 128 --output-json results/eco_adaptive_router_prediction_demo.json --output-md results/eco_adaptive_router_prediction_demo.md --output-html results/eco_adaptive_router_prediction_demo.html

open-adaptive-router-predict-demo:
	@xdg-open results/eco_adaptive_router_prediction_demo.html >/dev/null 2>&1 || true

adaptive-router-predict:
	@if [ -z "$(SEQUENCE)" ]; then \
		echo "Uso: make adaptive-router-predict SEQUENCE=ACGT..."; \
		echo "Opcional: SEQUENCE_ID=mi_secuencia THRESHOLD=0.20 EMBEDDING_K=4 DIMENSIONS=128"; \
		echo "Salida: results/$(ADAPTIVE_OUTPUT_PREFIX).json/.md/.html"; \
		exit 1; \
	fi
	$(PY) scripts/run_eco_adaptive_router_predict.py --sequence "$(SEQUENCE)" --sequence-id "$(SEQUENCE_ID)" --input "$(INPUT)" --threshold "$(THRESHOLD)" --embedding-k "$(EMBEDDING_K)" --dimensions "$(DIMENSIONS)" --output-json results/$(ADAPTIVE_OUTPUT_PREFIX).json --output-md results/$(ADAPTIVE_OUTPUT_PREFIX).md --output-html results/$(ADAPTIVE_OUTPUT_PREFIX).html

open-adaptive-router-predict:
	@xdg-open results/$(ADAPTIVE_OUTPUT_PREFIX).html >/dev/null 2>&1 || echo "No se pudo abrir: results/$(ADAPTIVE_OUTPUT_PREFIX).html"

adaptive-router-batch:
	$(PY) scripts/run_eco_adaptive_router_batch.py --batch-input "$(BATCH_INPUT)" --training-input "$(INPUT)" --threshold "$(THRESHOLD)" --embedding-k "$(EMBEDDING_K)" --dimensions "$(DIMENSIONS)" --output-json results/$(BATCH_OUTPUT_PREFIX).json --output-md results/$(BATCH_OUTPUT_PREFIX).md --output-html results/$(BATCH_OUTPUT_PREFIX).html

open-adaptive-router-batch:
	@xdg-open results/$(BATCH_OUTPUT_PREFIX).html >/dev/null 2>&1 || echo "No se pudo abrir: results/$(BATCH_OUTPUT_PREFIX).html"
