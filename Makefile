.PHONY: install-dev test validate demo check clean

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

check: test validate demo

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f results/test_*.fa results/test_*.json results/test_*.csv
	rm -f results/eco_demo_pipeline.fa results/eco_demo_pipeline_report.json
