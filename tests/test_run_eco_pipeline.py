import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIPELINE_SCRIPT = ROOT / "scripts" / "run_eco_pipeline.py"


def test_run_eco_pipeline_with_custom_paths_succeeds(tmp_path):
    """El pipeline parametrizable debe aceptar BED/FASTA propios y generar salidas."""
    result = subprocess.run(
        [
            sys.executable,
            str(PIPELINE_SCRIPT),
            "--bed",
            str(ROOT / "examples" / "demo_regions.bed"),
            "--reference",
            str(ROOT / "examples" / "tiny_reference.fa"),
            "--output-dir",
            str(tmp_path),
            "--prefix",
            "custom_demo",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "E.C.O. PARAMETRIZABLE PIPELINE REPORT" in result.stdout
    assert "Estado: OK, pipeline parametrizable E.C.O. funcionando." in result.stdout

    output_fasta = tmp_path / "custom_demo.fa"
    output_json = tmp_path / "custom_demo_report.json"
    output_markdown = tmp_path / "custom_demo_report.md"

    assert output_fasta.exists()
    assert output_json.exists()
    assert output_markdown.exists()

    report = json.loads(output_json.read_text(encoding="utf-8"))
    assert report["summary"]["regions_processed"] == 4
    assert report["summary"]["total_motif_hits"] == 4
    assert report["summary"]["feedback"]["rejected_packets"] == 0

    markdown = output_markdown.read_text(encoding="utf-8")
    assert "# Reporte demo E.C.O." in markdown
    assert "OK: digestión informacional completa y sin rechazos." in markdown
