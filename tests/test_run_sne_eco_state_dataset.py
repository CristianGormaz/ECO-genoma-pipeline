import csv
import json
import subprocess
import sys


def test_run_sne_eco_state_dataset_exports_json_and_tsv(tmp_path):
    output_json = tmp_path / "sne_eco_state_dataset.json"
    output_tsv = tmp_path / "sne_eco_state_dataset.tsv"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_state_dataset.py",
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
    assert "OK: dataset adaptativo S.N.E.-E.C.O. generado." in result.stdout
    assert output_json.exists()
    assert output_tsv.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["status"] == "ok"
    assert payload["row_count"] == 4
    assert len(payload["rows"]) == 4
    assert payload["rows"][0]["state_before"] == "idle"
    assert "no modela conciencia humana" in payload["responsible_limit"]

    with output_tsv.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    assert len(rows) == 4
    assert "state_before" in rows[0]
    assert "state_after" in rows[0]
    assert "immune_load_after" in rows[0]
