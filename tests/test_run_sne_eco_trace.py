import json
import subprocess
import sys


def test_run_sne_eco_trace_script_exports_packet_trace_artifacts(tmp_path):
    output_json = tmp_path / "sne_eco_packet_trace.json"
    output_md = tmp_path / "sne_eco_packet_trace.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_sne_eco_trace.py",
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
    assert "OK: trazabilidad digestiva S.N.E.-E.C.O. generada." in result.stdout

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["status"] == "ok"
    assert payload["processed_packets"] == 4
    assert len(payload["traces"]) == 4
    assert payload["traces"][0]["packet_id"]
    assert "Ruta digestiva S.N.E.-E.C.O." in markdown
    assert "valid_sequence" in markdown
    assert "duplicate_sequence" in markdown
