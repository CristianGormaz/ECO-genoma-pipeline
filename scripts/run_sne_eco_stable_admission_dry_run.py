from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("results/sne_eco_stable_admission_plan.json")
DEFAULT_OUTPUT_JSON = Path("results/sne_eco_stable_admission_dry_run.json")
DEFAULT_OUTPUT_MD = Path("results/sne_eco_stable_admission_dry_run.md")


def _walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


def _collect_admission_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in _walk(payload):
        if "source" in item and "admission_decision" in item:
            rows.append(item)
    return rows


def _dry_run_result(decision: str) -> tuple[str, str, bool]:
    if decision == "admit_later":
        return (
            "pending_retest",
            "document_boundary_and_repeat_observation_before_training",
            False,
        )
    if decision == "hold_for_threshold_review":
        return (
            "blocked_by_threshold_review",
            "evaluate_threshold_without_changing_rc1_baseline",
            False,
        )
    if decision == "exclude_until_policy_defined":
        return (
            "blocked_by_missing_policy",
            "define_invalid_payload_policy_before_any_training",
            False,
        )
    if decision == "keep_as_observation_control":
        return (
            "control_only",
            "keep_as_external_control_without_training",
            False,
        )
    return (
        "manual_review_required",
        "manual_review_before_any_dataset_change",
        False,
    )


def build_dry_run(payload: dict[str, Any]) -> dict[str, Any]:
    rows = _collect_admission_rows(payload)

    dry_rows = []
    for row in rows:
        decision = str(row.get("admission_decision", "manual_review_required"))
        simulated_result, dry_run_action, admission_allowed_now = _dry_run_result(decision)

        dry_rows.append(
            {
                "source": row.get("source"),
                "admission_decision": decision,
                "gate": row.get("gate"),
                "risk": row.get("risk", "unknown"),
                "simulated_result": simulated_result,
                "dry_run_action": dry_run_action,
                "admission_allowed_now": admission_allowed_now,
            }
        )

    decision_counts = Counter(row["admission_decision"] for row in dry_rows)
    risk_counts = Counter(row["risk"] for row in dry_rows)

    payload_out = {
        "report_name": "sne_eco_stable_admission_dry_run",
        "status": "yellow" if dry_rows else "green",
        "reason": (
            "Dry-run ejecutado: ninguna fila externa se admite todavía."
            if dry_rows
            else "Sin filas externas para simular."
        ),
        "metrics": {
            "external_rows_evaluated": len(dry_rows),
            "simulated_admissions_now": sum(
                1 for row in dry_rows if row["admission_allowed_now"]
            ),
            "future_candidates": decision_counts.get("admit_later", 0),
            "threshold_holds": decision_counts.get("hold_for_threshold_review", 0),
            "temporary_exclusions": decision_counts.get(
                "exclude_until_policy_defined", 0
            ),
            "observation_controls": decision_counts.get(
                "keep_as_observation_control", 0
            ),
            "manual_review_required": decision_counts.get(
                "manual_review_required", 0
            ),
            "high_risk": risk_counts.get("high", 0),
        },
        "stability_locks": {
            "stable_dataset_modified": False,
            "baseline_modified": False,
            "rules_modified": False,
            "thresholds_modified": False,
            "dry_run_only": True,
        },
        "decision_counts": dict(decision_counts),
        "risk_counts": dict(risk_counts),
        "rows": dry_rows,
        "responsible_limit": (
            "Dry-run educativo/experimental; no modifica dataset estable, baseline, "
            "reglas ni umbrales. No representa desempeño general, no modela conciencia "
            "humana y no tiene uso clínico/forense."
        ),
    }
    return payload_out


def to_markdown(payload: dict[str, Any]) -> str:
    metrics = payload["metrics"]
    locks = payload["stability_locks"]
    rows = payload["rows"]

    lines = [
        "# Dry-run de admisión estable S.N.E.-E.C.O.",
        "",
        "Simulación de admisión para evidencia externa observada después de RC1.",
        "",
        f"Estado: 🟡 `{payload['status']}`" if payload["status"] == "yellow" else f"Estado: 🟢 `{payload['status']}`",
        f"Motivo: {payload['reason']}",
        "",
        "## Métricas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Filas externas evaluadas | {metrics['external_rows_evaluated']} |",
        f"| Admisiones simuladas ahora | {metrics['simulated_admissions_now']} |",
        f"| Candidatos futuros | {metrics['future_candidates']} |",
        f"| Retenciones por umbral | {metrics['threshold_holds']} |",
        f"| Exclusiones temporales | {metrics['temporary_exclusions']} |",
        f"| Controles observacionales | {metrics['observation_controls']} |",
        f"| Revisión manual requerida | {metrics['manual_review_required']} |",
        f"| Alto riesgo | {metrics['high_risk']} |",
        "",
        "## Candados de estabilidad",
        "",
        f"- Dataset estable modificado: `{locks['stable_dataset_modified']}`",
        f"- Baseline modificado: `{locks['baseline_modified']}`",
        f"- Reglas modificadas: `{locks['rules_modified']}`",
        f"- Umbrales modificados: `{locks['thresholds_modified']}`",
        f"- Solo simulación: `{locks['dry_run_only']}`",
        "",
        "## Matriz dry-run",
        "",
        "| source | decision | gate | risk | simulated_result | admission_allowed_now | dry_run_action |",
        "|---|---|---|---|---|---|---|",
    ]

    for row in rows:
        lines.append(
            "| {source} | {decision} | {gate} | {risk} | {result} | {allowed} | {action} |".format(
                source=row.get("source"),
                decision=row.get("admission_decision"),
                gate=row.get("gate"),
                risk=row.get("risk"),
                result=row.get("simulated_result"),
                allowed=row.get("admission_allowed_now"),
                action=row.get("dry_run_action"),
            )
        )

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "Este dry-run confirma que la evidencia externa puede ser simulada sin abrir la puerta de admisión real. "
            "Ningún candidato entra todavía al dataset estable; todos permanecen en observación, retención, exclusión temporal o control.",
            "",
            "## Límite responsable",
            "",
            payload["responsible_limit"],
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    dry_run = build_dry_run(payload)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(dry_run, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.output_md.write_text(to_markdown(dry_run), encoding="utf-8")

    print("OK: dry-run de admisión estable S.N.E.-E.C.O. generado.")
    print(f"- {args.output_json.resolve()}")
    print(f"- {args.output_md.resolve()}")


if __name__ == "__main__":
    main()
