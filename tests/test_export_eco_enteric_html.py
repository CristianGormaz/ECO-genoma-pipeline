import subprocess
import sys
from pathlib import Path


def test_export_eco_enteric_html_generates_static_html(tmp_path):
    output_json = tmp_path / "eco_enteric_system_report.json"
    output_md = tmp_path / "eco_enteric_system_report.md"
    output_html = tmp_path / "eco_enteric_system_report.html"

    report_result = subprocess.run(
        [
            sys.executable,
            "scripts/run_eco_enteric_report.py",
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert report_result.returncode == 0
    assert output_json.exists()

    html_result = subprocess.run(
        [
            sys.executable,
            "scripts/export_eco_enteric_html.py",
            "--input-json",
            str(output_json),
            "--output-html",
            str(output_html),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert html_result.returncode == 0
    assert "Estado: OK, HTML del sistema entérico generado." in html_result.stdout
    assert output_html.exists()

    html = output_html.read_text(encoding="utf-8")
    assert "E.C.O. - Sistema Entérico Integrado" in html
    assert "Secuencia válida" in html
    assert "discard_duplicate" in html
    assert "Resumen homeostático" in html
