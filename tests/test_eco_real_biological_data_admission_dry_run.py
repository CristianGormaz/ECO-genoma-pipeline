import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_real_biological_data_admission_dry_run.py")
DOC = Path("docs/operations/eco-real-biological-data-admission-dry-run.md")


def _manifest() -> dict:
    return {
        "source_id": "dry_run_allowed_manifest",
        "source_name": "Dry-run allowed manifest",
        "source_kind": "public_non_sensitive",
        "origin": "descriptive_manifest_only",
        "license_or_permission": "licencia clara",
        "sensitivity_classification": "permitido",
        "contains_identifiable_people": False,
        "contains_genetic_data": False,
        "contains_clinical_data": False,
        "allowed_use": "validación técnica limitada futura",
        "blocked_use": "diagnóstico, entrenamiento, interpretación clínica, uso aplicado",
        "readiness_decision": "allow",
        "human_review_declared": True,
        "human_decision": "permitido limitado solo para evidencia dry-run",
        "rollback_declared": True,
        "rollback_plan": "detener, registrar y revertir cualquier intento",
        "interpretive_limits_declared": True,
        "interpretive_limits": "sin diagnóstico, sin interpretación clínica, sin riesgo genético individual",
        "audit_evidence_declared": True,
        "audit_evidence": "reporte auditable conservado",
        "technical_validation_scope": "limited",
        "responsible_limits": {
            "ingests_real_data": False,
            "uses_sensitive_data": False,
            "trains_model": False,
            "modifies_baseline": False,
            "recalibrates_thresholds": False,
            "makes_applied_biomedical_claims": False,
        },
    }


def _run(tmp_path: Path, manifest: dict) -> tuple[subprocess.CompletedProcess[str], Path, Path]:
    manifest_path = tmp_path / "manifest.json"
    output_json = tmp_path / "report.json"
    output_md = tmp_path / "report.md"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--manifest",
            str(manifest_path),
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


def _payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_dry_run_script_and_document_exist() -> None:
    assert SCRIPT.exists()
    assert DOC.exists()


def test_dry_run_document_contract() -> None:
    text = DOC.read_text(encoding="utf-8")
    lowered = text.lower()

    required_tokens = [
        "dry-run",
        "manifiestos descriptivos",
        "no habilita datos reales",
        "no aprueba procesamiento real",
        "revisión humana",
        "blocked",
        "paused",
        "requires_human_review",
        "limited_allowed",
        "rejected",
        "sin lectura de datos reales",
        "sin descarga de datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin diagnóstico",
        "sin interpretación clínica",
        "sin afirmaciones biomédicas aplicadas",
    ]

    for token in required_tokens:
        assert token in lowered


def test_limited_allowed_manifest_generates_json_and_markdown(tmp_path: Path) -> None:
    result, output_json, output_md = _run(tmp_path, _manifest())

    assert result.returncode == 0, result.stdout + result.stderr
    assert output_json.exists()
    assert output_md.exists()

    payload = _payload(output_json)
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["gate_id"] == "eco_real_biological_data_admission_dry_run_v1"
    assert payload["status"] == "passed"
    assert payload["decision"] == "limited_allowed"
    assert payload["processed_real_data"] is False
    assert payload["downloaded_real_data"] is False
    assert payload["read_real_data_files"] is False
    assert payload["trained_model"] is False
    assert payload["modified_baseline"] is False
    assert payload["recalibrated_thresholds"] is False
    assert payload["makes_applied_biomedical_claims"] is False
    assert "E.C.O. Real Biological Data Admission Dry-Run Report" in markdown
    assert "No se procesaron datos reales" in markdown
    assert "No habilita admisión real" in markdown


def test_identifiable_people_blocks_manifest(tmp_path: Path) -> None:
    manifest = _manifest()
    manifest["contains_identifiable_people"] = True

    result, output_json, _ = _run(tmp_path, manifest)
    payload = _payload(output_json)

    assert result.returncode == 0
    assert payload["decision"] == "blocked"
    assert payload["required_human_review"] is True
    assert "identificadores personales" in " ".join(payload["reasons"])


def test_clinical_data_blocks_manifest(tmp_path: Path) -> None:
    manifest = _manifest()
    manifest["contains_clinical_data"] = True

    result, output_json, _ = _run(tmp_path, manifest)
    payload = _payload(output_json)

    assert result.returncode == 0
    assert payload["decision"] == "blocked"
    assert "datos clínicos" in " ".join(payload["reasons"])


def test_genetic_conditional_manifest_requires_human_review(tmp_path: Path) -> None:
    manifest = _manifest()
    manifest["contains_genetic_data"] = True
    manifest["sensitivity_classification"] = "condicional"

    result, output_json, _ = _run(tmp_path, manifest)
    payload = _payload(output_json)

    assert result.returncode == 0
    assert payload["decision"] == "requires_human_review"
    assert "condicional" in " ".join(payload["reasons"])


def test_missing_fields_rejects_manifest_with_controlled_exit(tmp_path: Path) -> None:
    result, output_json, _ = _run(tmp_path, {"source_id": "incomplete"})
    payload = _payload(output_json)

    assert result.returncode == 1
    assert payload["status"] == "failed"
    assert payload["decision"] == "rejected"
    assert payload["evidence"]["missing_required_fields"]
    assert "Faltan campos requeridos" in " ".join(payload["reasons"])


def test_script_does_not_use_data_download_or_dataset_libraries() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    forbidden_tokens = [
        "requests",
        "urllib.request.urlopen",
        "subprocess",
        "wget",
        "curl",
        "pandas",
        "BioPython",
        "pyfaidx",
        "pysam",
    ]

    for token in forbidden_tokens:
        assert token not in text


def test_referenced_data_path_is_not_opened(tmp_path: Path) -> None:
    manifest = _manifest()
    manifest["data_path"] = str(tmp_path / "does-not-exist.fasta")

    result, output_json, _ = _run(tmp_path, manifest)
    payload = _payload(output_json)

    assert result.returncode == 0
    assert output_json.exists()
    assert payload["decision"] == "limited_allowed"
    assert payload["read_real_data_files"] is False


def test_default_artifacts_are_registered_for_cleaning() -> None:
    cleaner = Path("scripts/clean_eco_results.py").read_text(encoding="utf-8")
    clean_test = Path("tests/test_eco_clean_results_command.py").read_text(encoding="utf-8")

    assert "eco_real_biological_data_admission_dry_run_report.json" in cleaner
    assert "eco_real_biological_data_admission_dry_run_report.md" in cleaner
    assert "eco_real_biological_data_admission_dry_run_report.json" in clean_test
    assert "eco_real_biological_data_admission_dry_run_report.md" in clean_test


def test_dry_run_gate_registered_in_operational_maps() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [
            Path("docs/operations/project-map.md"),
            Path("docs/operations/eco-current-capabilities-map.md"),
            Path("docs/operations/eco-operational-panel-index.md"),
        ]
    )

    required_tokens = [
        "real biological data admission dry-run gate",
        "manifiestos descriptivos",
        "reporte auditable",
        "no lee",
        "no descarga",
        "no procesa",
        "no interpreta datos reales",
        "no aprueba admisión real",
        "revisión humana",
    ]

    for token in required_tokens:
        assert token in combined
