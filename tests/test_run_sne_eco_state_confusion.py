import json
import subprocess
import sys


def test_run_sne_eco_state_confusion_exports_actionable_report(tmp_path):
    output_json = tmp_path / "confusion.json"
    output_md = tmp_path / "confusion.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_state_confusion.py",
            "--extended",
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "OK: análisis de rutas confundidas E.C.O. generado." in result.stdout
    assert output_json.exists()
    assert output_md.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["scenario_set"] == "extended"
    assert payload["confused_routes"]
    assert payload["suggested_focus"]
    assert "Análisis de rutas confundidas E.C.O." in markdown
    assert "Focos sugeridos" in markdown
