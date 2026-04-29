.PHONY: install-dev test validate demo review report pipeline public-demo variant-demo clinvar-sample clinvar-html clinvar-charts preview-clinvar inspect-clinvar-json open-clinvar-html open-clinvar-charts portfolio-demo check clean

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

preview-clinvar:
	@sed -n '1,180p' results/eco_clinvar_sample_report.md

inspect-clinvar-json:
	@$(PY) -m json.tool results/eco_clinvar_sample_report.json | head -80

open-clinvar-html:
	@xdg-open results/eco_clinvar_sample_report.html >/dev/null 2>&1 || echo "No se pudo abrir el HTML. Revisa: results/eco_clinvar_sample_report.html"

open-clinvar-charts:
	@xdg-open results/eco_clinvar_sample_charts/index.html >/dev/null 2>&1 || echo "No se pudo abrir el índice. Revisa: results/eco_clinvar_sample_charts/index.html"

portfolio-demo: check clinvar-sample clinvar-charts clinvar-html
	@echo ""
	@echo "E.C.O. PORTFOLIO DEMO READY"
	@echo "==========================="
	@echo "Reportes principales generados:"
	@echo "- results/eco_demo_pipeline_report.md"
	@echo "- results/eco_custom_demo_report.md"
	@echo "- results/eco_variant_demo_report.md"
	@echo "- results/eco_clinvar_sample_report.md"
	@echo "- results/eco_clinvar_sample_report.html"
	@echo "- results/eco_clinvar_sample_charts/index.html"
	@echo ""
	@echo "Documentos de apoyo:"
	@echo "- docs/caso-estudio-portafolio-eco.md"
	@echo "- docs/guia-interpretacion-variantes-eco.md"
	@echo "- docs/uso-responsable-datos-eco.md"
	@echo "- docs/modulo-sne-eco-digestion-bioinspirada.md"
	@echo ""
	@echo "Vista rápida Markdown: make preview-clinvar"
	@echo "Inspección JSON: make inspect-clinvar-json"
	@echo "Abrir HTML: make open-clinvar-html"
	@echo "Abrir gráficos: make open-clinvar-charts"

check: test validate demo review report pipeline variant-demo

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f results/test_*.fa results/test_*.json results/test_*.csv
	rm -f results/eco_demo_pipeline.fa results/eco_demo_pipeline_report.json results/eco_demo_pipeline_report.md
	rm -f results/eco_custom_demo.fa results/eco_custom_demo_report.json results/eco_custom_demo_report.md
	rm -f results/eco_public_chrM.fa results/eco_public_chrM_report.json results/eco_public_chrM_interpretive_report.md
	rm -f results/eco_variant_demo_report.json results/eco_variant_demo_report.md
	rm -f results/eco_clinvar_sample.tsv results/eco_clinvar_sample_report.json results/eco_clinvar_sample_report.md results/eco_clinvar_sample_report.html
	rm -rf results/eco_clinvar_sample_charts
