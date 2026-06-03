import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_real_biological_data_admission_dry_run_trace_report.py")
DOC = Path("docs/operations/eco-real-biological-data-admission-dry-run-trace-report.md")
MAKEFILE = Path("Makefile")
CLEANER = Path("scripts/clean_eco_results.py")

RESULT_JSON = Path("results/eco_real_biological_data_admission_dry_run_trace_report.json")
RESULT_MD = Path("results/eco_real_biological_data_admission_dry_run_trace_report.md")


def _fixture(decision: str = "requires_human_review") -> dict:
    return {
        "gate_id": "eco_real_biological_data_admission_dry_run_v1",
        "status": "passed",
        "decision": decision,
        "processed_real_data": False,
        "downloaded_real_data": False,
        "read_real_data_files": False,
        "trained_model": False,
        "modified_baseline": False,
        "recalibrated_thresholds": False,
        "makes_applied_biomedical_claims": False,
        "reasons": ["readiness_decision solicita review."],
        "required_human_review": True,
        "responsible_limits": {
            "sin_lectura_de_datos_reales": True,
            "sin_descarga_de_datos_reales": True,
            "sin_ingestion_de_datos_reales": True,
            "sin_procesamiento_de_secuencias": True,
            "sin_entrenamiento": True,
            "sin_modificacion_de_baseline": True,
            "sin_recalibracion_de_umbrales": True,
            "sin_diagnostico": True,
            "sin_interpretacion_clinica": True,
            "sin_riesgo_genetico_individual": True,
            "sin_afirmaciones_biomedicas_aplicadas": True,
            "sin_autonomia_real": True,
            "sin_conciencia": True,
            "sin_libre_albedrio_real": True,
        },
        "evidence": {
            "manifest_only": True,
            "unsafe_responsible_limits": [],
        },
        "next_action": "Enviar a revisión humana; no procesar datos reales.",
    }


def _run_trace(tmp_path: Path, report: dict, output_json: Path | None = None, output_md: Path | None = None):
    input_json = tmp_path / "dry_run_report.json"
    output_json = output_json or tmp_path / "trace_report.json"
    output_md = output_md or tmp_path / "trace_report.md"
    input_json.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input-json",
            str(input_json),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result, output_json, output_md


def test_trace_report_script_document_and_makefile_contract_exist():
    assert SCRIPT.exists()
    assert DOC.exists()

    makefile = MAKEFILE.read_text(encoding="utf-8")
    assert "eco-real-biological-data-admission-dry-run-trace-report" in makefile
    assert "scripts/run_eco_real_biological_data_admission_dry_run_trace_report.py" in makefile
    assert "$(PY) scripts/run_eco_real_biological_data_admission_dry_run_trace_report.py" in makefile


def test_trace_report_document_contract():
    text = DOC.read_text(encoding="utf-8")
    lowered = text.lower()

    required_tokens = [
        "Dry-Run Trace Report",
        "make eco-real-biological-data-admission-dry-run",
        "make eco-real-biological-data-admission-dry-run-trace-report",
        "no habilita datos reales",
        "no aprueba admisión real",
        "revisión humana",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
    ]

    for token in required_tokens:
        assert token in text
    assert "sin datos reales" in lowered
    assert "sin interpretación biomédica aplicada" in lowered


def test_trace_report_generates_json_and_markdown_from_safe_fixture(tmp_path: Path):
    result, output_json, output_md = _run_trace(tmp_path, _fixture())

    assert result.returncode == 0, result.stdout + result.stderr
    assert output_json.exists()
    assert output_md.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["trace_id"] == "eco_real_biological_data_admission_dry_run_trace_v1"
    assert payload["trace_status"] == "passed"
    assert payload["source_decision"] == "requires_human_review"
    assert payload["processed_real_data"] is False
    assert payload["downloaded_real_data"] is False
    assert payload["read_real_data_files"] is False
    assert payload["trained_model"] is False
    assert payload["modified_baseline"] is False
    assert payload["recalibrated_thresholds"] is False
    assert payload["makes_applied_biomedical_claims"] is False
    assert payload["does_not_authorize_real_admission"] is True
    assert payload["does_not_replace_human_review"] is True
    assert "E.C.O. Real Biological Data Admission Dry-Run Trace Report" in markdown
    assert "Decision: `requires_human_review`" in markdown
    assert "No se procesaron datos reales" in markdown
    assert "No habilita admisión real" in markdown
    assert "revisión humana" in markdown


def test_trace_report_preserves_fixture_decision(tmp_path: Path):
    result, output_json, _ = _run_trace(tmp_path, _fixture(decision="paused"))
    payload = json.loads(output_json.read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert payload["trace_status"] == "passed"
    assert payload["source_decision"] == "paused"


def test_trace_report_script_does_not_use_download_or_dataset_libraries():
    text = SCRIPT.read_text(encoding="utf-8")
    forbidden_tokens = [
        "requests",
        "urllib.request.urlopen",
        "wget",
        "curl",
        "pandas",
        "BioPython",
        "pyfaidx",
        "pysam",
    ]

    for token in forbidden_tokens:
        assert token not in text


def test_trace_report_default_missing_input_fails_without_outputs(tmp_path: Path):
    missing_input = tmp_path / "missing.json"
    output_json = tmp_path / "should_not_exist.json"
    output_md = tmp_path / "should_not_exist.md"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input-json",
            str(missing_input),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "make eco-real-biological-data-admission-dry-run" in result.stdout
    assert not output_json.exists()
    assert not output_md.exists()


def test_trace_report_artifacts_are_cleaned(tmp_path: Path):
    result, output_json, output_md = _run_trace(tmp_path, _fixture(), RESULT_JSON, RESULT_MD)

    assert result.returncode == 0, result.stdout + result.stderr
    assert output_json.exists()
    assert output_md.exists()
    assert "eco_real_biological_data_admission_dry_run_trace_report.json" in CLEANER.read_text(
        encoding="utf-8"
    )
    assert "eco_real_biological_data_admission_dry_run_trace_report.md" in CLEANER.read_text(
        encoding="utf-8"
    )

    clean = subprocess.run(
        [sys.executable, str(CLEANER)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert clean.returncode == 0, clean.stdout + clean.stderr
    assert not output_json.exists()
    assert not output_md.exists()
