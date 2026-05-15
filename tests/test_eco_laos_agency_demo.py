from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_laos_agency_demo_outputs_and_contract() -> None:
    script = Path("scripts/run_eco_laos_agency_demo.py")
    result_json = Path("results/eco_laos_agency_demo.json")
    result_md = Path("results/eco_laos_agency_demo.md")

    completed = subprocess.run([sys.executable, str(script)], check=True, capture_output=True, text=True)
    assert completed.returncode == 0

    assert result_json.exists(), "Debe generar JSON de resultados"
    assert result_md.exists(), "Debe generar Markdown de resultados"

    payload = json.loads(result_json.read_text(encoding="utf-8"))
    markdown = result_md.read_text(encoding="utf-8")

    assert payload.get("status") == "passed"
    assert payload.get("classification") == "permitido"

    scenarios = payload.get("scenarios", [])
    assert len(scenarios) == 3

    for scenario in scenarios:
        score = scenario.get("laos_score")
        assert isinstance(score, (int, float))
        assert 0 <= score <= 1

    payload_text = json.dumps(payload, ensure_ascii=False).lower()
    markdown_text = markdown.lower()

    for required in [
        "laos",
        "agencia simulada",
        "no libre albedrío real",
        "no conciencia",
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
    ]:
        assert required in payload_text

    for heading in [
        "# e.c.o. laos synthetic agency demo",
        "## estado",
        "## marco de límites responsables",
        "## escenarios sintéticos",
    ]:
        assert heading in markdown_text
