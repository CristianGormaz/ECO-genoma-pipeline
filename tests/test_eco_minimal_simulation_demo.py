import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/run_eco_minimal_simulation.py")
MAKEFILE = Path("Makefile")
DOC = Path("docs/architecture/eco-minimal-simulation-demo.md")
RESULT_JSON = Path("results/eco_minimal_simulation_demo.json")
RESULT_MD = Path("results/eco_minimal_simulation_demo.md")

def run_demo():
    return subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

def test_minimal_simulation_assets_exist():
    assert SCRIPT.exists()
    assert DOC.exists()

def test_makefile_exposes_minimal_simulation_command():
    text = MAKEFILE.read_text(encoding="utf-8")
    assert "eco-minimal-simulation-demo:" in text
    assert "scripts/run_eco_minimal_simulation.py" in text

def test_minimal_simulation_runs_and_writes_outputs():
    result = run_demo()
    assert result.returncode == 0
    assert "E.C.O. minimal simulation demo" in result.stdout
    assert RESULT_JSON.exists()
    assert RESULT_MD.exists()
    data = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    assert data["summary"]["classification"] == "allowed"
    assert data["summary"]["data_policy"] == "synthetic_only"
    assert data["summary"]["training"] is False
    assert len(data["trace"]) == 5

def test_minimal_simulation_declares_responsible_limits():
    run_demo()
    text = RESULT_MD.read_text(encoding="utf-8")
    assert "datos sintéticos" in text
    assert "No entrena modelos" in text or "no entrena modelos" in text
    assert "no hace afirmaciones biomédicas aplicadas" in text
