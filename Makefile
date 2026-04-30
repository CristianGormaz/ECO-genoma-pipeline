.PHONY: install-dev test validate demo review report pipeline public-demo variant-demo clinvar-sample clinvar-html clinvar-charts preview-clinvar inspect-clinvar-json open-clinvar-html open-clinvar-charts dataset-audit classifier-baseline classifier-baseline-v2 classifier-baseline-v3 classifier-html classifier-html-v2 classifier-html-v3 classifier-compare classifier-repeated-eval classifier-sensitivity embedding-placeholder embedding-repeated-eval model-decision open-classifier-html open-classifier-html-v2 open-classifier-html-v3 open-classifier-comparison open-classifier-repeated-eval open-classifier-sensitivity open-embedding-placeholder open-embedding-repeated-eval open-model-decision portfolio-demo check clean

PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

install-dev:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

test:
	$(PY) -m pytest -q

validate:
	$(PY) scripts/run_eco_validation.py

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

portfolio-demo: check classifier-html classifier-html-v2 classifier-html-v3 classifier-repeated-eval classifier-sensitivity embedding-placeholder embedding-repeated-eval model-decision clinvar-sample clinvar-charts clinvar-html
	@echo ""
	@echo "E.C.O. PORTFOLIO DEMO READY"
	@echo "==========================="
	@echo "Reportes principales generados:"
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
	@echo "- docs/caso-estudio-portafolio-eco.md"
	@echo "- docs/guia-interpretacion-variantes-eco.md"
	@echo "- docs/uso-responsable-datos-eco.md"
	@echo "- docs/modulo-sne-eco-digestion-bioinspirada.md"
	@echo "- docs/nota-tecnica-v3-vs-v2.md"
	@echo ""
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

check: test validate demo review report pipeline variant-demo dataset-audit classifier-baseline classifier-baseline-v2 classifier-baseline-v3 classifier-compare embedding-placeholder embedding-repeated-eval model-decision

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f results/test_*.fa results/test_*.json results/test_*.csv
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
