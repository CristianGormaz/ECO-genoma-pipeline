import json
import subprocess
import sys
from pathlib import Path


def test_run_eco_adaptive_router_batch_exports_reports(tmp_path: Path):
    batch_input = tmp_path / "batch.tsv"
    batch_input.write_text(
        "sequence_id\tsequence\tdescription\n"
        "seq_a\tACGTCCAATGGTATAAAGGCGGGCGGAATAAAGTAC\tvalid demo\n"
        "seq_b\tTTTTACACACACGTTTACACACACGTTTACACACAC\tvalid repetitive\n"
        "seq_bad\tACGTXYZ\tinvalid demo\n",
        encoding="utf-8",
    )

    output_json = tmp_path / "batch_report.json"
    output_md = tmp_path / "batch_report.md"
    output_html = tmp_path / "batch_report.html"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_eco_adaptive_router_batch.py",
            "--batch-input",
            str(batch_input),
            "--threshold",
            "0.20",
            "--embedding-k",
            "4",
            "--dimensions",
            "128",
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--output-html",
            str(output_html),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "Estado: OK, inferencia por lote generada." in result.stdout
    assert output_json.exists()
    assert output_md.exists()
    assert output_html.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["summary"]["total_sequences"] == 3
    assert payload["summary"]["processed_sequences"] == 2
    assert payload["summary"]["rejected_sequences"] == 1
    assert len(payload["results"]) == 3
    assert any(item["status"] == "rejected" for item in payload["results"])
    assert any(item["status"] == "processed" for item in payload["results"])
    assert "route_counts" in payload["summary"]
    assert "caution_counts" in payload["summary"]

    markdown = output_md.read_text(encoding="utf-8")
    assert "# E.C.O. - Inferencia por lote con router adaptativo" in markdown
    assert "## Resumen del lote" in markdown
    assert "## Detalle" in markdown

    html = output_html.read_text(encoding="utf-8")
    assert "E.C.O. — Inferencia por lote" in html
    assert "Detalle del lote" in html
