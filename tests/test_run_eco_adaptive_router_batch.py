import json
import subprocess
import sys
from pathlib import Path


def test_run_eco_adaptive_router_batch_exports_reports(tmp_path: Path):
    output_json = tmp_path / "batch_report.json"
    output_md = tmp_path / "batch_report.md"
    output_html = tmp_path / "batch_report.html"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_eco_adaptive_router_batch.py",
            "--batch-input",
            "examples/demo_adaptive_router_batch.tsv",
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
    assert "Homeostasis: atencion" in result.stdout
    assert output_json.exists()
    assert output_md.exists()
    assert output_html.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    summary = payload["summary"]
    homeostasis = summary["homeostasis"]

    assert summary["total_sequences"] == 3
    assert summary["processed_sequences"] == 2
    assert summary["rejected_sequences"] == 1
    assert summary["contradiction_count"] >= 1
    assert summary["high_caution_count"] >= 1
    assert "baseline_v3" in summary["route_counts"]
    assert "none" in summary["route_counts"]
    assert homeostasis["state"] == "atencion"
    assert homeostasis["risk_score"] > 0
    assert homeostasis["rejection_rate"] > 0
    assert "barrera_inmune_activa" in homeostasis["triggers"]
    assert "contradiccion_entre_rutas" in homeostasis["triggers"]
    assert "cautela_alta" in homeostasis["triggers"]
    assert len(payload["results"]) == 3

    rejected = [item for item in payload["results"] if item["status"] == "rejected"]
    assert len(rejected) == 1
    assert rejected[0]["enteric_reflex"]["reflex_name"] == "reflejo_inmune_de_rechazo"

    markdown = output_md.read_text(encoding="utf-8")
    assert "# E.C.O. - Inferencia por lote con router adaptativo" in markdown
    assert "## Resumen del lote" in markdown
    assert "## Homeostasis del lote" in markdown
    assert "## Detalle" in markdown

    html = output_html.read_text(encoding="utf-8")
    assert "E.C.O. — Inferencia por lote" in html
    assert "Homeostasis del lote" in html
    assert "Detalle del lote" in html
