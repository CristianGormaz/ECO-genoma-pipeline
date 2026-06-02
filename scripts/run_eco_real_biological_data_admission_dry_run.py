#!/usr/bin/env python3
"""Dry-run gate for real biological data admission manifests.

The gate evaluates only descriptive manifests. It never downloads URLs, opens
data files, parses biological sequences, trains models, changes baselines, or
recalibrates thresholds.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

OUTPUT_JSON = Path("results/eco_real_biological_data_admission_dry_run.json")
OUTPUT_MD = Path("results/eco_real_biological_data_admission_dry_run.md")

ALLOWED_DECISIONS = {
    "blocked",
    "paused",
    "requires_human_review",
    "limited_allowed",
    "rejected",
}

RESPONSIBLE_LIMITS = [
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
]

DATA_ACCESS_FIELDS = {
    "data_file",
    "data_file_path",
    "data_path",
    "data_url",
    "raw_data_path",
    "sequence_file",
    "sequence_path",
    "fasta_path",
    "bed_path",
    "vcf_path",
    "variant_file",
}

SOURCE_MANIFEST_FIELDS = ("source_id", "source_name", "source_kind", "origin")

DEFAULT_MANIFEST: dict[str, Any] = {
    "source_id": "dry_run_incomplete_manifest",
    "source_name": "Dry-run incomplete manifest",
    "source_kind": "public_non_sensitive",
    "origin": "descriptive_fixture_only",
    "sensitivity_classification": "condicional",
    "contains_identifiable_people": False,
    "contains_genetic_data": False,
    "contains_clinical_data": False,
    "allowed_use": "governance_dry_run_only",
    "blocked_use": "real_data_processing",
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


def _truthy(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() in {"true", "yes", "sí", "si"})


def _has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _evidence_item(
    evidence_id: str,
    label: str,
    passed: bool,
    explanation: str,
    fields: list[str],
) -> dict[str, Any]:
    return {
        "id": evidence_id,
        "label": label,
        "state": "passed" if passed else "missing",
        "fields": fields,
        "explanation": explanation,
    }


def _collect_data_access_fields(manifest: dict[str, Any]) -> list[str]:
    return sorted(field for field in DATA_ACCESS_FIELDS if manifest.get(field))


def evaluate_evidence(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    source_manifest_ok = all(_has_text(manifest.get(field)) for field in SOURCE_MANIFEST_FIELDS)
    sensitivity_ok = _has_text(manifest.get("sensitivity_classification"))
    license_ok = _has_text(manifest.get("license_or_permission")) and manifest.get("license_or_permission") != "unknown"
    human_review_ok = _truthy(manifest.get("human_review_declared")) and _has_text(manifest.get("human_decision"))
    limits_ok = _truthy(manifest.get("interpretive_limits_declared")) and _has_text(manifest.get("interpretive_limits"))
    rollback_ok = _truthy(manifest.get("rollback_declared")) and _has_text(manifest.get("rollback_plan"))
    audit_ok = _truthy(manifest.get("audit_evidence_declared")) and _has_text(manifest.get("audit_evidence"))

    return [
        _evidence_item(
            "source_manifest",
            "manifiesto de fuente",
            source_manifest_ok,
            "Debe describir fuente, origen y tipo sin apuntar a contenido a procesar.",
            list(SOURCE_MANIFEST_FIELDS),
        ),
        _evidence_item(
            "sensitivity_classification",
            "clasificación de sensibilidad",
            sensitivity_ok,
            "Debe declarar sensibilidad antes de cualquier evaluación posterior.",
            ["sensitivity_classification"],
        ),
        _evidence_item(
            "license_or_permission",
            "licencia o permiso",
            license_ok,
            "Debe existir licencia o permiso claro; unknown no basta.",
            ["license_or_permission"],
        ),
        _evidence_item(
            "human_decision",
            "decisión humana",
            human_review_ok,
            "Debe existir revisión humana declarada y decisión humana trazable.",
            ["human_review_declared", "human_decision"],
        ),
        _evidence_item(
            "interpretive_limits",
            "límites interpretativos",
            limits_ok,
            "Debe declarar límites interpretativos sin finalidad clínica.",
            ["interpretive_limits_declared", "interpretive_limits"],
        ),
        _evidence_item(
            "rollback",
            "rollback",
            rollback_ok,
            "Debe declarar rollback antes de cualquier validación limitada futura.",
            ["rollback_declared", "rollback_plan"],
        ),
        _evidence_item(
            "audit_evidence",
            "evidencia auditable",
            audit_ok,
            "Debe conservar evidencia auditable de la decisión.",
            ["audit_evidence_declared", "audit_evidence"],
        ),
    ]


def _strict_limited_criteria(manifest: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, bool]:
    return {
        "public_source": _truthy(manifest.get("public_source")) or manifest.get("source_kind") in {"public_aggregate", "public_non_sensitive"},
        "non_human_or_low_risk": _truthy(manifest.get("non_human_or_low_risk")) or manifest.get("risk_level") == "low",
        "clear_license": any(item["id"] == "license_or_permission" and item["state"] == "passed" for item in evidence),
        "no_personal_identifiers": not _truthy(manifest.get("contains_identifiable_people")) and _truthy(manifest.get("no_personal_identifiers")),
        "no_clinical_purpose": not _truthy(manifest.get("contains_clinical_data")) and _truthy(manifest.get("no_clinical_purpose")),
        "human_review": any(item["id"] == "human_decision" and item["state"] == "passed" for item in evidence),
        "rollback": any(item["id"] == "rollback" and item["state"] == "passed" for item in evidence),
        "interpretive_limits": any(item["id"] == "interpretive_limits" and item["state"] == "passed" for item in evidence),
        "technical_validation_limited": manifest.get("technical_validation_scope") == "limited",
        "audit_evidence": any(item["id"] == "audit_evidence" and item["state"] == "passed" for item in evidence),
    }


def decide_manifest(manifest: dict[str, Any], evidence: list[dict[str, Any]]) -> tuple[str, str, dict[str, bool], list[str]]:
    unsafe_data_references = _collect_data_access_fields(manifest)
    if unsafe_data_references:
        return (
            "blocked",
            "El manifiesto intenta declarar rutas o URLs de datos; v1 solo acepta descripción de intención.",
            _strict_limited_criteria(manifest, evidence),
            unsafe_data_references,
        )

    if _truthy(manifest.get("contains_identifiable_people")) or _truthy(manifest.get("personal_identifiers_present")):
        return (
            "blocked",
            "El manifiesto declara identificadores personales o personas identificables.",
            _strict_limited_criteria(manifest, evidence),
            unsafe_data_references,
        )

    if _truthy(manifest.get("contains_clinical_data")) or manifest.get("intended_use") == "clinical":
        return (
            "blocked",
            "El manifiesto declara datos o finalidad clínica.",
            _strict_limited_criteria(manifest, evidence),
            unsafe_data_references,
        )

    if manifest.get("readiness_decision") == "block" or manifest.get("sensitivity_classification") in {"bloqueado", "high", "sensitive"}:
        return (
            "blocked",
            "El manifiesto se declara bloqueado o de sensibilidad alta.",
            _strict_limited_criteria(manifest, evidence),
            unsafe_data_references,
        )

    missing = [item["id"] for item in evidence if item["state"] != "passed"]
    if "source_manifest" in missing:
        return (
            "rejected",
            "Falta manifiesto de fuente mínimo; no hay base auditable para continuar.",
            _strict_limited_criteria(manifest, evidence),
            unsafe_data_references,
        )

    if "human_decision" in missing:
        return (
            "requires_human_review",
            "Falta revisión humana declarada; no se puede avanzar.",
            _strict_limited_criteria(manifest, evidence),
            unsafe_data_references,
        )

    if missing:
        return (
            "paused",
            f"Falta evidencia crítica: {', '.join(missing)}.",
            _strict_limited_criteria(manifest, evidence),
            unsafe_data_references,
        )

    strict_criteria = _strict_limited_criteria(manifest, evidence)
    if all(strict_criteria.values()):
        return (
            "limited_allowed",
            "El manifiesto cumple criterios mínimos para validación técnica limitada futura; no autoriza procesamiento clínico ni uso general.",
            strict_criteria,
            unsafe_data_references,
        )

    return (
        "requires_human_review",
        "La evidencia existe, pero no cumple todos los criterios estrictos para permitido limitado.",
        strict_criteria,
        unsafe_data_references,
    )


def build_report(manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    if manifest is None:
        manifest = dict(DEFAULT_MANIFEST)
    if not isinstance(manifest, dict):
        return {
            "title": "E.C.O. real biological data admission dry-run gate",
            "status": "blocked",
            "decision": "rejected",
            "decision_reason": "El manifiesto debe ser un objeto JSON descriptivo.",
            "allowed_decisions": sorted(ALLOWED_DECISIONS),
            "evidence": [],
            "strict_limited_criteria": {},
            "unsafe_data_reference_fields": [],
            "responsible_limits": RESPONSIBLE_LIMITS,
            "interpretation_boundary": _interpretation_boundary(),
        }

    evidence = evaluate_evidence(manifest)
    decision, reason, strict_criteria, unsafe_data_references = decide_manifest(manifest, evidence)
    status = "passed" if decision == "limited_allowed" else "attention" if decision in {"paused", "requires_human_review"} else "blocked"

    return {
        "title": "E.C.O. real biological data admission dry-run gate",
        "status": status,
        "decision": decision,
        "decision_reason": reason,
        "allowed_decisions": sorted(ALLOWED_DECISIONS),
        "manifest_summary": {
            "source_id": manifest.get("source_id"),
            "source_name": manifest.get("source_name"),
            "source_kind": manifest.get("source_kind"),
            "sensitivity_classification": manifest.get("sensitivity_classification"),
            "readiness_decision": manifest.get("readiness_decision"),
        },
        "evidence": evidence,
        "strict_limited_criteria": strict_criteria,
        "unsafe_data_reference_fields": unsafe_data_references,
        "responsible_limits": RESPONSIBLE_LIMITS,
        "interpretation_boundary": _interpretation_boundary(),
    }


def _interpretation_boundary() -> dict[str, bool]:
    return {
        "accepts_descriptive_manifest_only": True,
        "opens_real_data_files": False,
        "downloads_urls": False,
        "parses_sequences": False,
        "interprets_variants": False,
        "trains_model": False,
        "modifies_baseline": False,
        "recalibrates_thresholds": False,
        "clinical_authorization": False,
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# E.C.O. real biological data admission dry-run gate",
        "",
        f"Estado: `{report['status']}`",
        f"Decisión: `{report['decision']}`",
        f"Razón: {report['decision_reason']}",
        "",
        "## Evidencia mínima",
        "",
        "| Evidencia | Estado | Campos |",
        "|---|---|---|",
    ]
    for item in report["evidence"]:
        lines.append(f"| {item['label']} | `{item['state']}` | `{', '.join(item['fields'])}` |")

    lines.extend(["", "## Criterios de permitido limitado", ""])
    for key, value in report["strict_limited_criteria"].items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Campos de acceso a datos rechazados", ""])
    if report["unsafe_data_reference_fields"]:
        lines.extend(f"- `{field}`" for field in report["unsafe_data_reference_fields"])
    else:
        lines.append("- Ninguno.")

    lines.extend(["", "## Decisiones permitidas", ""])
    for decision in report["allowed_decisions"]:
        lines.append(f"- `{decision}`")

    lines.extend(["", "## Límites responsables", ""])
    for limit in report["responsible_limits"]:
        lines.append(f"- {limit}")

    lines.extend(
        [
            "",
            "## Frontera de interpretación",
            "",
            "- Evalúa manifiestos descriptivos, no datos reales.",
            "- No descarga URLs ni abre archivos de datos.",
            "- `limited_allowed` solo describe una validación técnica limitada futura; no autoriza uso clínico.",
            "",
        ]
    )
    return "\n".join(lines)


def _load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_outputs(report: dict[str, Any], output_json: Path = OUTPUT_JSON, output_md: Path = OUTPUT_MD) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(to_markdown(report), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="E.C.O. real biological data admission dry-run gate")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Ruta a un manifiesto descriptivo JSON. No debe apuntar a datos reales.",
    )
    parser.add_argument("--output-json", type=Path, default=OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=OUTPUT_MD)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = _load_manifest(args.manifest) if args.manifest else None
    report = build_report(manifest)

    write_outputs(report, output_json=args.output_json, output_md=args.output_md)

    print("# E.C.O. real biological data admission dry-run gate")
    print(f"Estado: {report['status']}")
    print(f"Decisión: {report['decision']}")
    print(f"Salida JSON: {args.output_json}")
    print(f"Salida Markdown: {args.output_md}")
    print("Límite: dry-run documental; sin datos reales, descarga, entrenamiento, baseline ni umbrales.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
