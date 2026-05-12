import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adaptive_dataset_report_script_generates_outputs():
    subprocess.run(
        [sys.executable, "scripts/run_eco_adaptive_dataset_report.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    output_json = ROOT / "results" / "eco_adaptive_dataset_report.json"
    output_md = ROOT / "results" / "eco_adaptive_dataset_report.md"

    assert output_json.exists()
    assert output_md.exists()

    report = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert report["status"] == "passed"
    assert report["classification"] == "permitted"
    assert report["synthetic_records"] >= 1
    assert "sin datos reales" in report["responsible_limits"]
    assert "sin entrenamiento" in report["responsible_limits"]
    assert "sin modificación de baseline" in report["responsible_limits"]
    assert "sin recalibración de umbrales" in report["responsible_limits"]
    assert "E.C.O. adaptive dataset operational report" in markdown


def test_makefile_exposes_adaptive_dataset_report_target():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")

    assert "eco-adaptive-dataset-report:" in makefile
    assert "scripts/run_eco_adaptive_dataset_report.py" in makefile
    assert "eco_adaptive_dataset_report.json" in makefile
