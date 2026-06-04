import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTERIC_REPORT_SCRIPT = ROOT / "scripts" / "run_eco_enteric_report.py"

def test_distributed_observability_plexus_presence(tmp_path):
    """Verifica que la observabilidad v1.2 (plexos) esté presente en el reporte."""
    output_json = tmp_path / "v1_2_report.json"
    
    result = subprocess.run(
        [
            sys.executable,
            str(ENTERIC_REPORT_SCRIPT),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    
    assert result.returncode == 0
    report = json.loads(output_json.read_text(encoding="utf-8"))
    
    # Verificar que existen escenarios extremos
    assert "extreme_scenarios" in report
    assert len(report["extreme_scenarios"]) == 2
    
    # Verificar presencia de plexos en el historial
    # Tomamos el primer registro canónico
    first_record = report["records"][0]
    history = first_record["history"]
    
    plexuses = [step.get("plexus") for step in history]
    assert "mucosa_epithelial" in plexuses
    assert "plexo_submucoso" in plexuses
    assert "plexo_mienterico" in plexuses

def test_v1_2_extreme_scenarios_content(tmp_path):
    """Verifica el contenido de los escenarios extremos de v1.2."""
    output_json = tmp_path / "v1_2_report.json"
    
    subprocess.run(
        [
            sys.executable,
            str(ENTERIC_REPORT_SCRIPT),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        check=True,
    )
    
    report = json.loads(output_json.read_text(encoding="utf-8"))
    extreme = report["extreme_scenarios"]
    
    # "Secuencia ambigua" debe estar en extreme_scenarios
    ambiguous = next(r for r in extreme if r["label"] == "Secuencia ambigua")
    assert ambiguous["decision"]["action"] == "quarantine"
    
    # "Secuencia pesada" debe estar en extreme_scenarios
    heavy = next(r for r in extreme if r["label"] == "Secuencia pesada")
    assert heavy["decision"]["action"] == "batch_absorb"
    assert "plexo_mienterico" in [h["plexus"] for h in heavy["history"]]
