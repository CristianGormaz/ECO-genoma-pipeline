import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = ROOT / "scripts" / "run_eco_demo_pipeline.py"
EXPORT_SCRIPT = ROOT / "scripts" / "export_eco_demo_markdown.py"


def test_export_eco_demo_markdown_succeeds(tmp_path):
    """El exportador debe convertir el JSON integrado en Markdown legible."""
    output_fasta = tmp_path / "demo.fa"
    output_json = tmp_path / "demo_report.json"
    output_md = tmp_path / "demo_report.md"

    demo = subprocess.run(
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
    assert demo.returncode == 0, demo.stderr

    export = subprocess.run(
        [
            sys.executable,
            str(EXPORT_SCRIPT),
            "--input",
            str(output_json),
            "--output",
            str(output_md),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert export.returncode == 0, export.stderr
    assert output_md.exists()

    markdown = output_md.read_text(encoding="utf-8")
    assert "# Reporte demo E.C.O." in markdown
    assert "## Resumen ejecutivo" in markdown
    assert "## Detalle por región" in markdown
    assert "CAAT_box" in markdown
    assert "TATA_box_canonica" in markdown
    assert "GC_box" in markdown
    assert "OK: digestión informacional completa y sin rechazos." in markdown
