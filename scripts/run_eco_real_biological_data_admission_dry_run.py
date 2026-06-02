#!/usr/bin/env python3
"""Dry-run gate for real biological data admission manifests.

This script evaluates only descriptive JSON manifests. It does not read,
download, parse, train, change baselines, recalibrate thresholds, or make
applied biomedical claims.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "architecture" / "eco-real-data-source-manifest-schema.json"
DEFAULT_OUTPUT_JSON = Path("results/eco_real_biological_data_admission_dry_run_report.json")
DEFAULT_OUTPUT_MD = Path("results/eco_real_biological_data_admission_dry_run_report.md")

GATE_ID = "eco_real_biological_data_admission_dry_run_v1"
DECISIONS = {"blocked", "paused", "requires_human_review", "limited_allowed", "rejected"}

UNSAFE_RESPONSIBLE_LIMITS = (
    "ingests_real_data",
    "uses_sensitive_data",
    "trains_model",
    "modifies_baseline",
    "recalibrates_thresholds",
    "makes_applied_biomedical_claims",
)

TOP_LEVEL_FALSE_FLAGS = {
    "processed_real_data": False,
    "downloaded_real_data": False,
    "read_real_data_files": False,
    "trained_model": False,
    "modified_baseline": False,
    "recalibrated_thresholds": False,
    "makes_applied_biomedical_claims": False,
}

DEFAULT_MANIFEST: dict[str, Any] = {
    "source_id": "dry_run_default_manifest",
    "source_name": "Dry-run default manifest",
    "source_kind": "public_non_sensitive",
    "origin": "descriptive_manifest_only",
    "license_or_permission": "dry-run fixture permission",
    "sensitivity_classification": "condicional",
    "contains_identifiable_people": False,
    "contains_genetic_data": False,
    "contains_clinical_data": False,
    "allowed_use": "governance dry-run only",
    "blocked_use": "real data processing",
    "readiness_decision": "review",
    "responsible_limits": {
        "ingests_real_data": False,
        "uses_sensitive_data": False,
        "trains_model": False,
        "modifies_baseline": False,
        "recalibrates_thresholds": False,
        "makes_applied_biomedical_claims": False,
    },
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema() -> dict[str, Any]:
    return _load_json(SCHEMA_PATH)


def _is_true(value: Any) -> bool:
    return value is True


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _required_fields(schema: dict[str, Any]) -> list[str]:
    return list(schema.get("required_fields", []))


def _missing_required_fields(schema: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    return sorted(field for field in _required_fields(schema) if field not in manifest)


def _invalid_allowed_values(schema: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    invalid: list[str] = []
    allowed_values = schema.get("allowed_values", {})
    for field in ("source_kind", "sensitivity_classification", "readiness_decision"):
        value = manifest.get(field)
        allowed = allowed_values.get(field, [])
        if field in manifest and value not in allowed:
            invalid.append(f"{field}={value}")
    return invalid


def _invalid_boolean_fields(manifest: dict[str, Any]) -> list[str]:
    invalid: list[str] = []
    for field in ("contains_identifiable_people", "contains_genetic_data", "contains_clinical_data"):
        if field in manifest and not isinstance(manifest[field], bool):
            invalid.append(field)
    return invalid


def _unsafe_responsible_limits(manifest: dict[str, Any]) -> list[str]:
    limits = manifest.get("responsible_limits", {})
    if not isinstance(limits, dict):
        return list(UNSAFE_RESPONSIBLE_LIMITS)
    return [key for key in UNSAFE_RESPONSIBLE_LIMITS if limits.get(key) is True]


def _evidence(manifest: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    missing = _missing_required_fields(schema, manifest)
    invalid_values = _invalid_allowed_values(schema, manifest)
    invalid_booleans = _invalid_boolean_fields(manifest)
    unsafe_limits = _unsafe_responsible_limits(manifest)
    human_review_declared = _is_true(manifest.get("human_review_declared"))
    rollback_declared = _is_true(manifest.get("rollback_declared"))
    interpretive_limits_declared = _is_true(manifest.get("interpretive_limits_declared"))
    audit_evidence_declared = _is_true(manifest.get("audit_evidence_declared"))

    return {
        "schema_path": str(SCHEMA_PATH.relative_to(ROOT)),
        "required_fields_present": not missing,
        "missing_required_fields": missing,
        "invalid_allowed_values": invalid_values,
        "invalid_boolean_fields": invalid_booleans,
        "unsafe_responsible_limits": unsafe_limits,
        "human_review_declared": human_review_declared,
        "human_decision_present": _nonempty_text(manifest.get("human_decision")),
        "rollback_declared": rollback_declared,
        "rollback_plan_present": _nonempty_text(manifest.get("rollback_plan")),
        "interpretive_limits_declared": interpretive_limits_declared,
        "interpretive_limits_present": _nonempty_text(manifest.get("interpretive_limits")),
        "audit_evidence_declared": audit_evidence_declared,
        "audit_evidence_present": _nonempty_text(manifest.get("audit_evidence")),
        "manifest_only": True,
    }


def _has_human_review(evidence: dict[str, Any]) -> bool:
    return bool(evidence["human_review_declared"] and evidence["human_decision_present"])


def _has_rollback(evidence: dict[str, Any]) -> bool:
    return bool(evidence["rollback_declared"] and evidence["rollback_plan_present"])


def _has_interpretive_limits(evidence: dict[str, Any]) -> bool:
    return bool(evidence["interpretive_limits_declared"] and evidence["interpretive_limits_present"])


def _has_audit_evidence(evidence: dict[str, Any]) -> bool:
    return bool(evidence["audit_evidence_declared"] and evidence["audit_evidence_present"])


def _limited_allowed_criteria(manifest: dict[str, Any], evidence: dict[str, Any]) -> dict[str, bool]:
    return {
        "public_or_non_sensitive_source": manifest.get("source_kind") in {"public_aggregate", "public_non_sensitive"},
        "readiness_allows": manifest.get("readiness_decision") == "allow",
        "sensitivity_permitted": manifest.get("sensitivity_classification") == "permitido",
        "no_identifiable_people": manifest.get("contains_identifiable_people") is False,
        "no_clinical_data": manifest.get("contains_clinical_data") is False,
        "no_genetic_data": manifest.get("contains_genetic_data") is False,
        "safe_responsible_limits": not evidence["unsafe_responsible_limits"],
        "human_review_declared": _has_human_review(evidence),
        "rollback_declared": _has_rollback(evidence),
        "interpretive_limits_declared": _has_interpretive_limits(evidence),
        "audit_evidence_declared": _has_audit_evidence(evidence),
        "technical_validation_limited": manifest.get("technical_validation_scope") == "limited",
    }


def _decision(manifest: dict[str, Any], evidence: dict[str, Any]) -> tuple[str, list[str], str]:
    reasons: list[str] = []

    if evidence["missing_required_fields"]:
        reasons.append(f"Faltan campos requeridos del schema: {', '.join(evidence['missing_required_fields'])}.")
        return "rejected", reasons, "Completar manifiesto descriptivo antes de cualquier revisión."

    if evidence["invalid_allowed_values"]:
        reasons.append(f"Valores fuera del schema: {', '.join(evidence['invalid_allowed_values'])}.")
        return "rejected", reasons, "Corregir valores del manifiesto descriptivo."

    if evidence["invalid_boolean_fields"]:
        reasons.append(f"Campos booleanos inválidos: {', '.join(evidence['invalid_boolean_fields'])}.")
        return "rejected", reasons, "Corregir tipos booleanos del manifiesto."

    if manifest.get("readiness_decision") == "block":
        reasons.append("readiness_decision declara block.")
        return "blocked", reasons, "Mantener bloqueado; no procesar datos reales."

    if manifest.get("sensitivity_classification") == "bloqueado":
        reasons.append("sensitivity_classification declara bloqueado.")
        return "blocked", reasons, "Mantener bloqueado; no procesar datos reales."

    if manifest.get("source_kind") in {"private", "sensitive"}:
        reasons.append("source_kind privado o sensible no es admisible en dry-run v1.")
        return "blocked", reasons, "Rechazar intento o rediseñar manifiesto sin datos sensibles."

    if manifest.get("contains_identifiable_people") is True:
        reasons.append("El manifiesto declara personas identificables o identificadores personales.")
        return "blocked", reasons, "Bloquear y exigir revisión humana antes de cualquier acción futura."

    if manifest.get("contains_clinical_data") is True:
        reasons.append("El manifiesto declara datos clínicos.")
        return "blocked", reasons, "Bloquear por frontera clínica; no procesar datos reales."

    if evidence["unsafe_responsible_limits"]:
        reasons.append(f"Límites responsables inseguros: {', '.join(evidence['unsafe_responsible_limits'])}.")
        return "blocked", reasons, "Bloquear hasta restaurar límites responsables seguros."

    if manifest.get("readiness_decision") == "review":
        reasons.append("readiness_decision solicita review.")
        return "requires_human_review", reasons, "Enviar a revisión humana; no procesar datos reales."

    if manifest.get("sensitivity_classification") == "condicional":
        reasons.append("sensitivity_classification condicional requiere revisión humana.")
        return "requires_human_review", reasons, "Enviar a revisión humana; no procesar datos reales."

    if manifest.get("contains_genetic_data") is True:
        reasons.append("El manifiesto declara datos genéticos y requiere revisión humana.")
        return "requires_human_review", reasons, "Revisión humana obligatoria antes de cualquier fase futura."

    if not _has_human_review(evidence):
        reasons.append("Falta revisión humana declarada o decisión humana.")
        return "requires_human_review", reasons, "Registrar revisión humana antes de avanzar."

    paused_reasons: list[str] = []
    if not _has_rollback(evidence):
        paused_reasons.append("rollback")
    if not _has_interpretive_limits(evidence):
        paused_reasons.append("límites interpretativos")
    if not _has_audit_evidence(evidence):
        paused_reasons.append("evidencia auditable")
    if paused_reasons:
        reasons.append(f"Falta evidencia crítica: {', '.join(paused_reasons)}.")
        return "paused", reasons, "Pausar hasta completar evidencia mínima."

    criteria = _limited_allowed_criteria(manifest, evidence)
    if all(criteria.values()):
        reasons.append("Manifiesto descriptivo elegible para revisión técnica limitada futura.")
        reasons.append("limited_allowed no autoriza leer, descargar, procesar ni interpretar datos reales.")
        return "limited_allowed", reasons, "Conservar reporte como evidencia previa; cualquier avance requiere sprint separado."

    failed_criteria = sorted(key for key, value in criteria.items() if not value)
    reasons.append(f"No cumple criterios estrictos de limited_allowed: {', '.join(failed_criteria)}.")
    return "paused", reasons, "Pausar y completar criterios antes de una revisión futura."


def evaluate_manifest(manifest: dict[str, Any], manifest_path: str) -> dict[str, Any]:
    schema = _schema()
    evidence = _evidence(manifest, schema)
    decision, reasons, next_action = _decision(manifest, evidence)
    criteria = _limited_allowed_criteria(manifest, evidence)
    status = "failed" if decision == "rejected" else "passed"

    report: dict[str, Any] = {
        "gate_id": GATE_ID,
        "status": status,
        "decision": decision,
        "manifest_path": manifest_path,
        **TOP_LEVEL_FALSE_FLAGS,
        "reasons": reasons,
        "required_human_review": decision in {"blocked", "paused", "requires_human_review", "rejected"},
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
        "evidence": evidence,
        "limited_allowed_criteria": criteria,
        "next_action": next_action,
    }

    if decision not in DECISIONS:
        report["status"] = "failed"
        report["decision"] = "rejected"
        report["reasons"].append("Decisión interna fuera del contrato permitido.")
    return report


def markdown_report(report: dict[str, Any]) -> str:
    evidence = report["evidence"]
    limits = report["responsible_limits"]
    lines = [
        "# E.C.O. Real Biological Data Admission Dry-Run Report",
        "",
        f"Gate ID: `{report['gate_id']}`",
        f"Status: `{report['status']}`",
        f"Decision: `{report['decision']}`",
        f"Manifest path: `{report['manifest_path']}`",
        "",
        "## Razones",
        "",
    ]
    lines.extend(f"- {reason}" for reason in report["reasons"])
    lines.extend(
        [
            "",
            "## Evidencia",
            "",
            f"- Schema: `{evidence['schema_path']}`.",
            f"- Campos requeridos presentes: `{evidence['required_fields_present']}`.",
            f"- Campos faltantes: `{', '.join(evidence['missing_required_fields']) or 'ninguno'}`.",
            f"- Revisión humana declarada: `{evidence['human_review_declared']}`.",
            f"- Rollback declarado: `{evidence['rollback_declared']}`.",
            f"- Límites interpretativos declarados: `{evidence['interpretive_limits_declared']}`.",
            f"- Evidencia auditable declarada: `{evidence['audit_evidence_declared']}`.",
            "",
            "## Límites responsables",
            "",
        ]
    )
    lines.extend(f"- {key}: `{value}`" for key, value in limits.items())
    lines.extend(
        [
            "",
            "## Frontera operacional",
            "",
            "- No se procesaron datos reales.",
            "- No se leyeron archivos de datos reales.",
            "- No se descargaron datos reales.",
            "- No se procesaron secuencias genéticas ni genómicas.",
            "- No se interpretaron datos biológicos.",
            "- No habilita admisión real.",
            "- No aprueba procesamiento real.",
            "- Cualquier avance posterior requiere revisión humana y sprint separado.",
            "",
            f"Next action: {report['next_action']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(report: dict[str, Any], output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(markdown_report(report), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="E.C.O. real biological data admission dry-run gate")
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest_path = str(args.manifest) if args.manifest else "builtin:default_descriptive_manifest"
    manifest = _load_json(args.manifest) if args.manifest else dict(DEFAULT_MANIFEST)

    if not isinstance(manifest, dict):
        report = {
            "gate_id": GATE_ID,
            "status": "failed",
            "decision": "rejected",
            "manifest_path": manifest_path,
            **TOP_LEVEL_FALSE_FLAGS,
            "reasons": ["El manifiesto debe ser un objeto JSON descriptivo."],
            "required_human_review": True,
            "responsible_limits": {},
            "evidence": {"schema_path": str(SCHEMA_PATH.relative_to(ROOT)), "manifest_only": True},
            "limited_allowed_criteria": {},
            "next_action": "Corregir manifiesto descriptivo.",
        }
    else:
        report = evaluate_manifest(manifest, manifest_path)

    write_report(report, args.output_json, args.output_md)

    print("# E.C.O. Real Biological Data Admission Dry-Run Gate")
    print(f"Status: {report['status']}")
    print(f"Decision: {report['decision']}")
    print(f"Output JSON: {args.output_json}")
    print(f"Output Markdown: {args.output_md}")
    print("Limit: dry-run only; no real data was read, downloaded, processed, interpreted, or used for training.")
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
