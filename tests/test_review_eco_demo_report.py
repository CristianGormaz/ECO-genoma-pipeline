import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = ROOT / "scripts" / "run_eco_demo_pipeline.py"
REVIEW_SCRIPT = ROOT / "scripts" / "review_eco_demo_report.py"


def test_review_eco_demo_report_succeeds_after_demo(tmp_path):
    """El lector humano debe revisar correctamente un JSON generado por la demo."""
    output_fasta = tmp_path / "demo.fa"
    output_json = tmp_path / "demo_report.json"

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

    review = subprocess.run(
        [sys.executable, str(REVIEW_SCRIPT), "--input", str(output_json)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert review.returncode == 0, review.stderr
    assert "E.C.O. REPORT REVIEW" in review.stdout
    assert "Resumen digestivo" in review.stdout
    assert "Detalle por región" in review.stdout
    assert "OK: el reporte muestra digestión informacional completa y sin rechazos." in review.stdout
