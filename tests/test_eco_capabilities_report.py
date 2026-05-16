from __future__ import annotations

import json
import subprocess
from pathlib import Path


SCRIPT = Path("scripts/run_eco_capabilities_report.py")
OUTPUT_JSON = Path("results/eco_capabilities_report.json")
OUTPUT_MD = Path("results/eco_capabilities_report.md")


def test_eco_capabilities_report_script_generates_expected_outputs() -> None:
    assert SCRIPT.exists(), "Debe existir scripts/run_eco_capabilities_report.py"

    run = subprocess.run(
        ["python3", str(SCRIPT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0, run.stderr

    assert OUTPUT_JSON.exists(), "Debe generarse results/eco_capabilities_report.json"
    assert OUTPUT_MD.exists(), "Debe generarse results/eco_capabilities_report.md"

    payload = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    markdown = OUTPUT_MD.read_text(encoding="utf-8").lower()
    payload_text = json.dumps(payload, ensure_ascii=False).lower()

    assert payload["status"] == "passed"
    assert payload["classification"] == "permitido"
    assert "pytest passing" in payload_text
    assert "dashboard sintético operativo con 7 componentes" in payload_text
    assert "governance panel" in payload_text
    assert "snapshot post-governance" in payload_text
    assert "checklist de liberación" in payload_text
    assert "mapa de capacidades actuales" in payload_text
    assert "laos governance gate" in payload_text
    assert "capacidad operativa sintética" in payload_text
    assert "compuerta de gobernanza" in payload_text
    assert "pausar" in payload_text
    assert "revisión humana" in payload_text
    assert "avanzar con control" in payload_text
    assert "sin libre albedrío real" in payload_text
    assert "sin conciencia" in payload_text
    assert "laos governance gate" in markdown
    assert "compuerta de gobernanza" in markdown
    assert "límites responsables" in markdown
    assert "qué no hace todavía e.c.o." in markdown

    required_limits = [
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "sin libre albedrío real",
        "sin conciencia",
    ]
    limits_text = " ".join(payload["responsible_limits"]).lower()
    for expected in required_limits:
        assert expected in limits_text
