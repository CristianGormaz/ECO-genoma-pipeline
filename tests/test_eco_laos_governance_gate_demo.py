from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_laos_governance_gate_demo.py")
DOC = Path("docs/operations/eco-laos-governance-gate.md")
MAKEFILE = Path("Makefile")
CLEANER = Path("scripts/clean_eco_results.py")
JSON_OUTPUT = Path("results/eco_laos_governance_gate_demo.json")
MD_OUTPUT = Path("results/eco_laos_governance_gate_demo.md")


def test_laos_governance_gate_demo_outputs_contract() -> None:
    completed = subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, text=True)

    assert "LAOS governance gate demo generado" in completed.stdout
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    markdown = MD_OUTPUT.read_text(encoding="utf-8")
    payload_text = json.dumps(payload, ensure_ascii=False).lower()
    markdown_text = markdown.lower()

    assert payload["status"] == "passed"
    assert payload["classification"] == "permitido"
    assert payload["scope"] == "documental_sintetico"
    assert payload["gate"]["autonomy_activation"] is False

    recommendations = {scenario["recommendation"] for scenario in payload["scenarios"]}
    assert recommendations == {"pausar", "revision humana", "avanzar con control"}
    assert {scenario["validation_state"] for scenario in payload["scenarios"]} == {"failed", "attention", "passed"}

    for scenario in payload["scenarios"]:
        assert 0 <= scenario["laos_score"] <= 1

    for required in [
        "sin libre albedrio real",
        "sin conciencia",
        "sin datos reales",
        "sin entrenamiento",
        "sin modificacion de baseline",
        "sin recalibracion de umbrales",
        "pausar",
        "revision humana",
        "avanzar con control",
    ]:
        assert required in payload_text
        assert required in markdown_text


def test_laos_governance_gate_document_and_makefile_contract() -> None:
    doc_text = DOC.read_text(encoding="utf-8").lower()
    makefile = MAKEFILE.read_text(encoding="utf-8")
    cleaner = CLEANER.read_text(encoding="utf-8")

    assert "laos governance gate" in doc_text
    assert "no activa autonomia real" in doc_text
    assert "sin libre albedrio real" in doc_text
    assert "sin conciencia" in doc_text

    assert ".PHONY: eco-laos-governance-gate-demo" in makefile
    assert "eco-laos-governance-gate-demo:" in makefile
    assert "scripts/run_eco_laos_governance_gate_demo.py" in makefile
    assert "$(MAKE) eco-laos-governance-gate-demo" not in makefile

    assert JSON_OUTPUT.as_posix() in cleaner
    assert MD_OUTPUT.as_posix() in cleaner
