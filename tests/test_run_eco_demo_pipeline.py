import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = ROOT / "scripts" / "run_eco_demo_pipeline.py"


def test_run_eco_demo_pipeline_succeeds(tmp_path):
    """La demo integrada debe producir FASTA, JSON y terminar OK."""
    output_fasta = tmp_path / "demo.fa"
    output_json = tmp_path / "demo_report.json"

    result = subprocess.run(
        [
            sys.executable,
            str(DEMO_SCRIPT),
            "--output-fasta",
            str(output_fasta),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "E.C.O. DEMO PIPELINE REPORT" in result.stdout
    assert "Estado: OK, intestino informacional demo funcionando." in result.stdout
    assert output_fasta.exists()
    assert output_json.exists()

    report = json.loads(output_json.read_text(encoding="utf-8"))
    assert report["summary"]["regions_processed"] == 4
    assert report["summary"]["total_motif_hits"] == 4
    assert report["summary"]["feedback"]["accepted_packets"] == 4
    assert report["summary"]["feedback"]["rejected_packets"] == 0
    assert report["summary"]["feedback"]["absorbed_packets"] == 4
