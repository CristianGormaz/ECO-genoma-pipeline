import json
import subprocess
import sys


def test_run_sne_eco_state_baseline_exports_json_and_markdown(tmp_path):
    output_json = tmp_path / "sne_eco_state_baseline.json"
    output_md = tmp_path / "sne_eco_state_baseline.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_state_baseline.py",
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
    assert "OK: baseline adaptativo E.C.O. v0 generado." in result.stdout
    assert output_json.exists()
    assert output_md.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["model_name"] == "adaptive_state_baseline_v0"
    assert payload["training_rows"] == 4
    assert payload["accuracy_demo"] == 1.0
    assert "no representa desempeño general" in payload["responsible_limit"]
    assert "Baseline adaptativo E.C.O. v0" in markdown
    assert "Accuracy demostrativa" in markdown
