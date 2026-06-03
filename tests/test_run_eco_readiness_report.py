from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT_PATH = Path("scripts/run_eco_readiness_report.py")


def test_run_eco_readiness_report_outputs_required_terms():
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    required_terms = [
        "E.C.O. READINESS REPORT",
        "readiness report sintético",
        "no verifica el estado actual de git",
        "no ejecuta pytest",
        "no debe interpretarse como prueba de que el repo está green",
        "ejecutar make eco-status",
        "ejecutar pytest",
        "ejecutar make eco-check-clean",
        "límites responsables",
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
        "decisión operativa",
        "modo recuperación",
    ]

    for term in required_terms:
        assert term in result.stdout

    assert "eco-status green" not in result.stdout
    assert "pytest passing" not in result.stdout
