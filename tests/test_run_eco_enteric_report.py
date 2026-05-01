import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTERIC_REPORT_SCRIPT = ROOT / "scripts" / "run_eco_enteric_report.py"


def test_run_eco_enteric_report_script_generates_outputs(tmp_path):
    """El reporte entérico debe generar JSON y Markdown exportables."""
    output_json = tmp_path / "eco_enteric_system_report.json"
    output_md = tmp_path / "eco_enteric_system_report.md"

    result = subprocess.run(
        [
            sys.executable,
            str(ENTERIC_REPORT_SCRIPT),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "OK: reporte entérico exportable generado." in result.stdout
    assert output_json.exists()
    assert output_md.exists()

    report = json.loads(output_json.read_text(encoding="utf-8"))
    assert report["actual_actions"] == ["absorb", "reject", "quarantine", "discard_duplicate"]
    assert report["homeostasis"]["total_packets"] == 4
    assert report["homeostasis"]["absorbed_packets"] == 1
    assert report["homeostasis"]["quarantined_packets"] == 1
    assert report["homeostasis"]["discarded_packets"] == 2
    assert report["homeostasis"]["duplicate_packets"] == 1

    markdown = output_md.read_text(encoding="utf-8")
    assert "# E.C.O. Enteric System Report" in markdown
    assert "## Resumen homeostático" in markdown
    assert "## Lectura arquitectónica" in markdown
