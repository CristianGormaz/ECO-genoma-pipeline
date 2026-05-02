import json
import subprocess
import sys
from pathlib import Path


def test_admission_governance_command_exports_report(tmp_path):
    output_json = tmp_path / "governance.json"
    output_md = tmp_path / "governance.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_admission_governance_command.py",
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
    assert output_json.exists()
    assert output_md.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["baseline"] == "sne-eco-v1.0-rc1"
    assert payload["status"] == "yellow"
    assert payload["stability_locks"]["stable_dataset_modified"] is False
    assert payload["stability_locks"]["baseline_modified"] is False
    assert payload["stability_locks"]["rules_modified"] is False
    assert payload["stability_locks"]["thresholds_modified"] is False
    assert payload["stability_locks"]["dry_run_only"] is True

    assert "Admission Governance Command" in markdown
    assert "No representa desempeño general" in markdown
