#!/usr/bin/env python3
"""Trace report for the E.C.O. real biological data admission dry-run output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TRACE_ID = "eco_real_biological_data_admission_dry_run_trace_v1"
DEFAULT_INPUT_JSON = Path("results/eco_real_biological_data_admission_dry_run_report.json")
DEFAULT_OUTPUT_JSON = Path("results/eco_real_biological_data_admission_dry_run_trace_report.json")
DEFAULT_OUTPUT_MD = Path("results/eco_real_biological_data_admission_dry_run_trace_report.md")

SAFE_DECISIONS = {"blocked", "paused", "requires_human_review", "limited_allowed", "rejected"}
FALSE_FLAGS = (
    "processed_real_data",
    "downloaded_real_data",
    "read_real_data_files",
    "trained_model",
    "modified_baseline",
    "recalibrated_thresholds",
    "makes_applied_biomedical_claims",
)
TRUE_LIMITS = (
    "sin_lectura_de_datos_reales",
    "sin_descarga_de_datos_reales",
    "sin_ingestion_de_datos_reales",
    "sin_procesamiento_de_secuencias",
    "sin_entrenamiento",
    "sin_modificacion_de_baseline",
    "sin_recalibracion_de_umbrales",
    "sin_diagnostico",
    "sin_afirmaciones_biomedicas_aplicadas",
)


def load_source_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_reasons(source: dict[str, Any]) -> list[str]:
    reasons = source.get("reasons", [])
    if not isinstance(reasons, list):
        return ["El reporte fuente no entrega razones en formato lista."]
    return [str(reason) for reason in reasons]


def _safe_false_flags(source: dict[str, Any]) -> tuple[bool, list[str]]:
    unsafe: list[str] = []
    for flag in FALSE_FLAGS:
        if flag not in source:
            unsafe.append(f"Falta flag responsable: {flag}.")
        elif source.get(flag) is not False:
            unsafe.append(f"Flag responsable insegura: {flag}.")
    return not unsafe, unsafe


def _safe_true_limits(source: dict[str, Any]) -> tuple[bool, list[str]]:
    limits = source.get("responsible_limits")
    if not isinstance(limits, dict):
        return False, ["Falta responsible_limits como objeto."]

    unsafe: list[str] = []
    for limit in TRUE_LIMITS:
        if limit not in limits:
            unsafe.append(f"Falta límite responsable: {limit}.")
        elif limits.get(limit) is not True:
            unsafe.append(f"Límite responsable inseguro: {limit}.")
    return not unsafe, unsafe


def _decision_summary(decision: str) -> str:
    summaries = {
        "blocked": "Decisión seca bloqueada; no hay admisión real.",
        "paused": "Decisión seca pausada; requiere evidencia adicional.",
        "requires_human_review": "Decisión seca segura: requiere revisión humana antes de cualquier paso futuro.",
        "limited_allowed": (
            "Elegibilidad documental limitada para revisión técnica futura; no es admisión real."
        ),
        "rejected": "Decisión seca rechazada; conservar evidencia y no procesar datos reales.",
    }
    return summaries.get(decision, "Decisión seca fuera del contrato esperado.")


def _next_action(decision: str, source: dict[str, Any], trace_status: str) -> str:
    if trace_status == "failed":
        return "Corregir el reporte fuente del dry-run y volver a generar la trazabilidad."
    if decision == "limited_allowed":
        return (
            "Conservar como evidencia documental limitada; cualquier uso posterior requiere "
            "revisión humana y sprint separado."
        )
    source_action = source.get("next_action")
    if isinstance(source_action, str) and source_action.strip():
        return source_action
    return "Conservar la decisión seca y requerir revisión humana antes de cualquier avance."


def build_trace_report(source: dict[str, Any], source_path: Path) -> dict[str, Any]:
    source_status = str(source.get("status", "missing"))
    source_decision = str(source.get("decision", "missing"))
    false_flags_ok, false_flag_reasons = _safe_false_flags(source)
    true_limits_ok, true_limit_reasons = _safe_true_limits(source)
    decision_ok = source_decision in SAFE_DECISIONS
    source_status_ok = source_status == "passed"
    trace_status = "passed" if source_status_ok and decision_ok and false_flags_ok and true_limits_ok else "failed"

    trace_reasons = _source_reasons(source)
    trace_reasons.extend(false_flag_reasons)
    trace_reasons.extend(true_limit_reasons)
    if not decision_ok:
        trace_reasons.append(f"Decisión fuente fuera del contrato: {source_decision}.")
    if not source_status_ok:
        trace_reasons.append(f"Estado fuente no passed: {source_status}.")

    evidence = source.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {"source_evidence_invalid": True}
    evidence = {
        "source_evidence": evidence,
        "source_report_read_only": True,
        "source_report_path": str(source_path),
        "source_decision_preserved": source_decision,
    }

    required_human_review = bool(
        source.get("required_human_review")
        or source_decision in {"blocked", "paused", "requires_human_review", "rejected"}
    )

    return {
        "trace_id": TRACE_ID,
        "source_report_path": str(source_path),
        "source_gate_id": source.get("gate_id"),
        "source_status": source_status,
        "source_decision": source_decision,
        "trace_status": trace_status,
        "decision_summary": _decision_summary(source_decision),
        "required_human_review": required_human_review,
        "reasons": trace_reasons,
        "evidence": evidence,
        "responsible_limits": source.get("responsible_limits", {}),
        "next_action": _next_action(source_decision, source, trace_status),
        "processed_real_data": False,
        "downloaded_real_data": False,
        "read_real_data_files": False,
        "trained_model": False,
        "modified_baseline": False,
        "recalibrated_thresholds": False,
        "makes_applied_biomedical_claims": False,
        "does_not_authorize_real_admission": True,
        "does_not_replace_human_review": True,
    }


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# E.C.O. Real Biological Data Admission Dry-Run Trace Report",
        "",
        f"Source gate: `{report['source_gate_id']}`",
        f"Source report: `{report['source_report_path']}`",
        f"Decision: `{report['source_decision']}`",
        f"Trace status: `{report['trace_status']}`",
        f"Decision summary: {report['decision_summary']}",
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
            f"- Reporte fuente de solo lectura: `{report['evidence']['source_report_read_only']}`.",
            f"- Decisión fuente preservada: `{report['evidence']['source_decision_preserved']}`.",
            "",
            "## Límites responsables",
            "",
        ]
    )
    if isinstance(report["responsible_limits"], dict):
        lines.extend(f"- {key}: `{value}`" for key, value in report["responsible_limits"].items())
    else:
        lines.append("- responsible_limits no disponible en formato esperado.")
    lines.extend(
        [
            "",
            "## Acción siguiente",
            "",
            f"- {report['next_action']}",
            "",
            "## Aclaraciones responsables",
            "",
            "- No se procesaron datos reales.",
            "- No se leyeron archivos de datos reales.",
            "- No se descargaron datos reales.",
            "- No se interpretaron datos biológicos reales.",
            "- No habilita admisión real.",
            "- No reemplaza revisión humana.",
            "- No entrena modelos.",
            "- No modifica baseline ni recalibra umbrales.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(report: dict[str, Any], output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(markdown_report(report), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="E.C.O. real biological data admission dry-run trace report"
    )
    parser.add_argument("--input-json", type=Path, default=DEFAULT_INPUT_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.input_json.exists():
        print("# E.C.O. Real Biological Data Admission Dry-Run Trace Report")
        print(f"Status: failed")
        print(f"Missing input JSON: {args.input_json}")
        print("Run first: make eco-real-biological-data-admission-dry-run")
        return 1

    source = load_source_report(args.input_json)
    if not isinstance(source, dict):
        print("# E.C.O. Real Biological Data Admission Dry-Run Trace Report")
        print("Status: failed")
        print("Input JSON must contain an object report.")
        return 1

    report = build_trace_report(source, args.input_json)
    write_outputs(report, args.output_json, args.output_md)

    print("# E.C.O. Real Biological Data Admission Dry-Run Trace Report")
    print(f"Trace status: {report['trace_status']}")
    print(f"Source decision: {report['source_decision']}")
    print(f"Output JSON: {args.output_json}")
    print(f"Output Markdown: {args.output_md}")
    print("Limit: trace only; no real data was read, downloaded, processed or interpreted.")
    return 1 if report["trace_status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
