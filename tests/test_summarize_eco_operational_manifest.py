import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_SCRIPT = ROOT / "scripts" / "summarize_eco_operational_manifest.py"


def test_summarize_eco_operational_manifest_generates_brief(tmp_path):
    manifest = {
        "manifest_type": "eco_operational_manifest",
        "schema_version": "0.1",
        "run_label": "pytest_status",
        "generated_at": "2026-04-30T23:47:17+00:00",
        "status": "ok",
        "artifact_count": 84,
        "artifacts_by_extension": {"json": 25, "md": 27, "html": 21},
        "missing_expected_core_artifacts": [],
        "report_summaries": [
            {
                "path": "eco_classifier_baseline_v3_report.json",
                "metrics": {
                    "feature_mode": "motif_kmer",
                    "test_macro_f1": 0.9161,
                },
            },
            {
                "path": "eco_embedding_repeated_eval_report.json",
                "metrics": {"operational_decision": "empate_tecnico_con_v3"},
            },
            {
                "path": "eco_variant_demo_report.json",
                "metrics": {"variants_processed": 5},
            },
        ],
    }

    manifest_path = tmp_path / "manifest.json"
    output_md = tmp_path / "brief.md"
    output_html = tmp_path / "brief.html"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SUMMARY_SCRIPT),
            "--manifest",
            str(manifest_path),
            "--output-md",
            str(output_md),
            "--output-html",
            str(output_html),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "E.C.O. STATUS BRIEF" in result.stdout
    assert output_md.exists()
    assert output_html.exists()

    md = output_md.read_text(encoding="utf-8")
    assert "Resumen conversacional de estado" in md
    assert "E.C.O. está en estado `ok`" in md
    assert "84 artefactos" in md
    assert "sin piezas esperadas pendientes" in md
    assert "macro F1=0.9161" in md
    assert "empate_tecnico_con_v3" in md
    assert "No entrega diagnóstico médico" in md

    html = output_html.read_text(encoding="utf-8")
    assert "<!doctype html>" in html
    assert "Resumen conversacional de estado" in html
