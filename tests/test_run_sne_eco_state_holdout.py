import json
import subprocess
import sys


def test_run_sne_eco_state_holdout_exports_json_and_markdown(tmp_path):
    output_json = tmp_path / "sne_eco_state_holdout_report.json"
    output_md = tmp_path / "sne_eco_state_holdout_report.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_state_holdout.py",
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
    assert "OK: evaluación holdout adaptativa E.C.O. v0 generada." in result.stdout
    assert output_json.exists()
    assert output_md.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["model_name"] == "adaptive_state_baseline_v0_holdout"
    assert payload["training_rows"] == 2
    assert payload["test_rows"] == 2
    assert "confusion_matrix" in payload
    assert "no representa desempeño general" in payload["responsible_limit"]
    assert "Matriz de confusión" in markdown
    assert "Accuracy holdout" in markdown
