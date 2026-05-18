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
        "eco-status green",
        "pytest passing",
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
