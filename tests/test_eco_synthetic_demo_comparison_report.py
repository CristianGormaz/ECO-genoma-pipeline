import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_synthetic_demo_comparison_report.py")
MAKEFILE = Path("Makefile")
README = Path("README.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
COMPARISON_DOC = Path("docs/architecture/eco-synthetic-demo-comparison.md")
JSON_OUTPUT = Path("results/eco_synthetic_demo_comparison_report.json")
MD_OUTPUT = Path("results/eco_synthetic_demo_comparison_report.md")


def test_synthetic_demo_comparison_report_runs():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["demo_count"] >= 4
    assert payload["classification"] == "allowed"

    names = " ".join(demo["name"].lower() for demo in payload["demos"])
    assert "minimal" in names
    assert "signal" in names
    assert "waste" in names
    assert "absorption" in names

    md = MD_OUTPUT.read_text(encoding="utf-8")
    assert "Patrón mínimo" in md
    assert "Lectura operativa" in md
    assert "Límite" in md


def test_makefile_mentions_comparison_report_command():
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: eco-synthetic-demo-comparison-report" in text
    assert "eco-synthetic-demo-comparison-report:" in text
    assert "scripts/run_eco_synthetic_demo_comparison_report.py" in text
    assert "$(MAKE) eco-synthetic-demo-comparison-report" in text
    assert "eco_synthetic_demo_comparison_report.json" in text


def test_docs_mention_comparison_report_command():
    readme = README.read_text(encoding="utf-8")
    project_map = PROJECT_MAP.read_text(encoding="utf-8")
    comparison = COMPARISON_DOC.read_text(encoding="utf-8")

    assert "make eco-synthetic-demo-comparison-report" in readme
    assert "make eco-synthetic-demo-comparison-report" in project_map
    assert "make eco-synthetic-demo-comparison-report" in comparison
