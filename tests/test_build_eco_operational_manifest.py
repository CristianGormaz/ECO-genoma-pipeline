import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCRIPT = ROOT / "scripts" / "build_eco_operational_manifest.py"


def test_build_eco_operational_manifest_from_temp_results(tmp_path):
    results = tmp_path / "results"
    results.mkdir()

    report = {
        "feature_mode": "motif_kmer",
        "kmer_k": 3,
        "feature_scaling": "minmax_train",
        "data_split": {"train": 36, "test": 24},
        "test_evaluation": {
            "accuracy": 0.9167,
            "classification_metrics": {
                "macro_avg": {"precision": 0.92, "recall": 0.91, "f1": 0.9161, "support": 24}
            },
        },
    }
    (results / "eco_classifier_baseline_v3_report.json").write_text(
        json.dumps(report, ensure_ascii=False),
        encoding="utf-8",
    )
    (results / "eco_classifier_baseline_v3_report.md").write_text(
        "# Reporte demo\n",
        encoding="utf-8",
    )

    output_json = results / "eco_operational_manifest.json"
    output_md = results / "eco_operational_manifest.md"

    result = subprocess.run(
        [
            sys.executable,
            str(MANIFEST_SCRIPT),
            "--results-dir",
            str(results),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--run-label",
            "pytest_manifest",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "E.C.O. OPERATIONAL MANIFEST" in result.stdout
    assert output_json.exists()
    assert output_md.exists()

    manifest = json.loads(output_json.read_text(encoding="utf-8"))
    assert manifest["manifest_type"] == "eco_operational_manifest"
    assert manifest["run_label"] == "pytest_manifest"
    assert manifest["artifact_count"] == 2
    assert manifest["artifacts_by_extension"] == {"json": 1, "md": 1}

    summary = manifest["report_summaries"][0]
    assert summary["path"] == "eco_classifier_baseline_v3_report.json"
    assert summary["metrics"]["feature_mode"] == "motif_kmer"
    assert summary["metrics"]["test_macro_f1"] == 0.9161

    md = output_md.read_text(encoding="utf-8")
    assert "Manifiesto operativo de corrida" in md
    assert "eco_classifier_baseline_v3_report.json" in md
