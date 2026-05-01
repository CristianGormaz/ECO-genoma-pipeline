import json
import subprocess
import sys


def test_state_dataset_script_exports_extended_scenarios(tmp_path):
    output_json = tmp_path / "extended_dataset.json"
    output_tsv = tmp_path / "extended_dataset.tsv"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_state_dataset.py",
            "--extended",
            "--output-json",
            str(output_json),
            "--output-tsv",
            str(output_tsv),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["scenario_set"] == "extended"
    assert payload["row_count"] >= 12
    assert output_tsv.exists()


def test_state_holdout_script_exports_extended_scenarios(tmp_path):
    output_json = tmp_path / "extended_holdout.json"
    output_md = tmp_path / "extended_holdout.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_state_holdout.py",
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
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["scenario_set"] == "extended"
    assert payload["test_rows"] >= 6
    assert "confusion_matrix" in payload
    assert output_md.exists()
