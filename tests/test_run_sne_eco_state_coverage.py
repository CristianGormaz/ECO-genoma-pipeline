import json
import subprocess
import sys


def test_run_sne_eco_state_coverage_exports_extended_diagnostics(tmp_path):
    output_json = tmp_path / "coverage.json"
    output_md = tmp_path / "coverage.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_state_coverage.py",
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
    assert "OK: diagnóstico de cobertura adaptativa E.C.O. generado." in result.stdout
    assert output_json.exists()
    assert output_md.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["scenario_set"] == "extended"
    assert payload["row_count"] >= 12
    assert "accuracy_holdout" in payload
    assert "macro_f1_holdout" in payload
    assert "coverage_warnings" in payload
    assert "Diagnóstico de cobertura adaptativa E.C.O." in markdown
    assert "Advertencias accionables" in markdown
