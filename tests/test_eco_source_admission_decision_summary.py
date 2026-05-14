import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/run_eco_source_admission_decision_summary.py")
JSON_OUTPUT = Path("results/eco_source_admission_decision_summary.json")
MD_OUTPUT = Path("results/eco_source_admission_decision_summary.md")


def test_source_admission_decision_summary_runs():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: resumen de decisión de admisión de fuentes E.C.O. generado." in result.stdout
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))

    assert payload["status"] == "passed"
    assert payload["classification"] == "conditional"
    assert payload["decision"] == "keep_synthetic_documental_mode"
    assert payload["external_source_admission"] == "paused_until_explicit_review"
    assert payload["registry_source_count"] == 12
    assert payload["blocked_source_count"] == 5
    assert payload["conditional_source_count"] == 4
    assert payload["required_decision_count"] == 7
    assert payload["responsible_limit_count"] == 5
    assert payload["errors"] == []
    assert "no ingiere datos reales" in payload["limit"]
    assert "no habilita entrenamiento" in payload["limit"]
    assert "no modifica baseline" in payload["limit"]
    assert "no recalibra umbrales" in payload["limit"]
    assert "no produce afirmaciones biomédicas aplicadas" in payload["limit"]


def test_source_admission_decision_summary_markdown_is_operational():
    subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    md = MD_OUTPUT.read_text(encoding="utf-8")

    assert "E.C.O. source admission decision summary" in md
    assert "keep_synthetic_documental_mode" in md
    assert "paused_until_explicit_review" in md
    assert "Registro de decisión" in md
    assert "Registro de fuentes sensibles" in md
    assert "Sin errores" in md
