import builtins
import json
import subprocess
import sys
from pathlib import Path

from scripts.run_eco_real_biological_data_admission_dry_run import (
    ALLOWED_DECISIONS,
    build_report,
)


SCRIPT = Path("scripts/run_eco_real_biological_data_admission_dry_run.py")
DOC = Path("docs/operations/eco-real-biological-data-admission-dry-run.md")
OUTPUT_JSON = Path("results/eco_real_biological_data_admission_dry_run.json")
OUTPUT_MD = Path("results/eco_real_biological_data_admission_dry_run.md")


def _limited_manifest() -> dict:
    return {
        "source_id": "future_low_risk_manifest",
        "source_name": "Future low risk manifest",
        "source_kind": "public_non_sensitive",
        "origin": "descriptive_manifest_only",
        "license_or_permission": "licencia clara declarada",
        "sensitivity_classification": "permitido",
        "contains_identifiable_people": False,
        "contains_genetic_data": False,
        "contains_clinical_data": False,
        "allowed_use": "validación técnica limitada",
        "blocked_use": "diagnóstico, entrenamiento, interpretación clínica, uso aplicado",
        "readiness_decision": "allow",
        "public_source": True,
        "non_human_or_low_risk": True,
        "risk_level": "low",
        "no_personal_identifiers": True,
        "no_clinical_purpose": True,
        "human_review_declared": True,
        "human_decision": "permitido limitado para dry-run futuro",
        "interpretive_limits_declared": True,
        "interpretive_limits": "sin diagnóstico, sin interpretación clínica, sin riesgo genético individual",
        "rollback_declared": True,
        "rollback_plan": "detener, registrar y revertir cualquier intento",
        "audit_evidence_declared": True,
        "audit_evidence": "reporte auditable requerido",
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


def test_real_biological_data_admission_dry_run_gate_exists() -> None:
    assert SCRIPT.exists()
    assert DOC.exists()
    assert "urllib" not in SCRIPT.read_text(encoding="utf-8")
    assert "requests" not in SCRIPT.read_text(encoding="utf-8")


def test_incomplete_manifest_requires_human_review_or_pauses() -> None:
    report = build_report(
        {
            "source_id": "incomplete",
            "source_name": "Incomplete manifest",
            "source_kind": "public_non_sensitive",
            "origin": "descriptive_only",
            "sensitivity_classification": "condicional",
        }
    )

    assert report["decision"] in {"blocked", "paused", "requires_human_review", "rejected"}
    assert report["decision"] != "limited_allowed"
    evidence_states = {item["id"]: item["state"] for item in report["evidence"]}
    assert evidence_states["license_or_permission"] == "missing"
    assert evidence_states["human_decision"] == "missing"
    assert evidence_states["rollback"] == "missing"


def test_dry_run_never_reads_real_data_files(monkeypatch) -> None:
    def fail_open(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("dry-run gate must not open data files")

    monkeypatch.setattr(builtins, "open", fail_open)
    manifest = _limited_manifest()
    manifest["data_file_path"] = "/tmp/real-sequence-never-opened.fa"

    report = build_report(manifest)

    assert report["decision"] == "blocked"
    assert "data_file_path" in report["unsafe_data_reference_fields"]
    assert report["interpretation_boundary"]["opens_real_data_files"] is False


def test_dry_run_never_downloads_urls() -> None:
    manifest = _limited_manifest()
    manifest["data_url"] = "https://example.invalid/not-downloaded"

    report = build_report(manifest)

    assert report["decision"] == "blocked"
    assert "data_url" in report["unsafe_data_reference_fields"]
    assert report["interpretation_boundary"]["downloads_urls"] is False


def test_limited_allowed_requires_all_strict_criteria() -> None:
    report = build_report(_limited_manifest())

    assert report["decision"] == "limited_allowed"
    assert report["decision"] in ALLOWED_DECISIONS
    assert all(report["strict_limited_criteria"].values())
    assert report["interpretation_boundary"]["clinical_authorization"] is False


def test_dry_run_requires_minimum_evidence_and_responsible_limits() -> None:
    report = build_report(_limited_manifest())
    labels = " ".join(item["label"] for item in report["evidence"])

    for token in [
        "manifiesto de fuente",
        "clasificación de sensibilidad",
        "licencia o permiso",
        "decisión humana",
        "límites interpretativos",
        "rollback",
        "evidencia auditable",
    ]:
        assert token in labels

    limits = " ".join(report["responsible_limits"])
    for token in [
        "sin datos reales",
        "sin entrenamiento",
        "sin datos sensibles",
        "sin diagnóstico",
        "sin interpretación clínica",
        "sin riesgo genético individual",
        "sin baseline changes",
        "sin threshold recalibration",
        "sin conciencia",
        "sin libre albedrío real",
    ]:
        assert token in limits


def test_dry_run_script_writes_json_and_markdown_outputs() -> None:
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert OUTPUT_JSON.exists()
    assert OUTPUT_MD.exists()

    payload = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    markdown = OUTPUT_MD.read_text(encoding="utf-8")

    assert payload["decision"] in ALLOWED_DECISIONS
    assert payload["decision"] != "limited_allowed"
    assert payload["interpretation_boundary"]["opens_real_data_files"] is False
    assert payload["interpretation_boundary"]["downloads_urls"] is False
    assert "Evidencia mínima" in markdown
    assert "Límites responsables" in markdown
    assert "No descarga URLs ni abre archivos de datos" in markdown


def test_dry_run_artifacts_are_registered_for_cleaning() -> None:
    cleaner = Path("scripts/clean_eco_results.py").read_text(encoding="utf-8")
    clean_test = Path("tests/test_eco_clean_results_command.py").read_text(encoding="utf-8")

    assert "eco_real_biological_data_admission_dry_run.json" in cleaner
    assert "eco_real_biological_data_admission_dry_run.md" in cleaner
    assert "eco_real_biological_data_admission_dry_run.json" in clean_test
    assert "eco_real_biological_data_admission_dry_run.md" in clean_test
