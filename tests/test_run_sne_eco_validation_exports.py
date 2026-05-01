import json
import subprocess
import sys


def test_run_sne_eco_validation_script_exports_markdown_and_json(tmp_path):
    output_md = tmp_path / "sne_eco_validation_report.md"
    output_json = tmp_path / "sne_eco_validation_report.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_validation.py",
            "--output-md",
            str(output_md),
            "--output-json",
            str(output_json),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_md.exists()
    assert output_json.exists()

    markdown = output_md.read_text(encoding="utf-8")
    payload = json.loads(output_json.read_text(encoding="utf-8"))

    assert "S.N.E.-E.C.O. VALIDATION REPORT" in markdown
    assert "OK: S.N.E.-E.C.O. integrado funcionando." in markdown
    assert payload["status"] == "ok"
    assert payload["processed_packets"] == 4
    assert payload["state"] == "watch"
    assert payload["homeostasis"]["total_packets"] == 4
    assert "bioinformático educativo" in payload["ethical_limit"]
