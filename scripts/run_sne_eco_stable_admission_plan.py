from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_POLICY_JSON = PROJECT_ROOT / "results" / "sne_eco_external_evidence_policy.json"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_stable_admission_plan.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_stable_admission_plan.md"

RESPONSIBLE_LIMIT = (
    "Plan educativo/experimental de admisión; no modifica dataset estable, baseline, "
    "reglas ni umbrales. No representa desempeño general, no modela conciencia humana "
    "y no tiene uso clínico/forense."
)

ADMISSION_RULES: dict[str, dict[str, str]] = {
    "candidate_for_future_stable_scenario": {
        "admission_decision": "admit_later",
        "gate": "requires_repeated_external_observation",
        "next_action": "document_boundary_and_retest_before_training",
        "risk": "medium",
    },
    "candidate_for_threshold_review": {
        "admission_decision": "hold_for_threshold_review",
        "gate": "requires_threshold_review",
        "next_action": "evaluate_without_changing_rc1_baseline",
        "risk": "medium",
    },
    "keep_out_of_stable_dataset": {
        "admission_decision": "exclude_until_policy_defined",
        "gate": "requires_explicit_invalid_payload_policy",
        "next_action": "define_exclusion_or_safety_policy_first",
        "risk": "medium",
    },
    "do_not_train_yet": {
        "admission_decision": "keep_as_observation_control",
        "gate": "control_only",
        "next_action": "keep_external_control_without_training",
        "risk": "low",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _policy_rows(policy_payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = policy_payload.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError("policy payload must include a list field named 'rows'")
    return rows


def classify_row(row: dict[str, Any]) -> dict[str, Any]:
    dataset_action = str(row.get("dataset_action", "manual_review_required"))
    policy_decision = str(row.get("policy_decision", row.get("decision", "manual_review")))
    source = str(row.get("source", "unknown"))
    category = str(row.get("category", "unknown"))

    if policy_decision == "block_until_reviewed" or row.get("risk") == "high":
        rule = {
            "admission_decision": "manual_review_required",
            "gate": "blocked_by_high_risk_or_default_state",
            "next_action": "manual_review_before_any_dataset_change",
            "risk": "high",
        }
    else:
        rule = ADMISSION_RULES.get(
            dataset_action,
            {
                "admission_decision": "manual_review_required",
                "gate": "unknown_dataset_action",
                "next_action": "manual_review_before_any_dataset_change",
                "risk": "high",
            },
        )

    return {
        "source": source,
        "category": category,
        "policy_decision": policy_decision,
        "dataset_action": dataset_action,
        "admission_decision": rule["admission_decision"],
        "gate": rule["gate"],
        "next_action": rule["next_action"],
        "risk": rule["risk"],
    }


def build_stable_admission_plan(policy_payload: dict[str, Any]) -> dict[str, Any]:
    classified_rows = [classify_row(row) for row in _policy_rows(policy_payload)]

    decision_counts = Counter(row["admission_decision"] for row in classified_rows)
    risk_counts = Counter(row["risk"] for row in classified_rows)

    manual_review_rows = decision_counts.get("manual_review_required", 0)
    excluded_rows = decision_counts.get("exclude_until_policy_defined", 0)
    held_rows = decision_counts.get("hold_for_threshold_review", 0)
    admit_later_rows = decision_counts.get("admit_later", 0)
    control_rows = decision_counts.get("keep_as_observation_control", 0)

    if manual_review_rows:
        status = "red"
        reason = "Existen filas de alto riesgo o acción desconocida; bloquear admisión estable."
    elif excluded_rows or held_rows or admit_later_rows:
        status = "yellow"
        reason = "Existen candidatos, retenciones o exclusiones; admitir solo con revisión futura."
    else:
        status = "green"
        reason = "Solo existen controles observacionales sin admisión pendiente."

    return {
        "plan_name": "sne_eco_stable_admission_plan",
        "source_policy": policy_payload.get("policy_name", "sne_eco_external_evidence_policy"),
        "status": status,
        "reason": reason,
        "external_rows": len(classified_rows),
        "admit_later_rows": admit_later_rows,
        "held_for_threshold_review_rows": held_rows,
        "excluded_rows": excluded_rows,
        "observation_control_rows": control_rows,
        "manual_review_rows": manual_review_rows,
        "decision_counts": dict(sorted(decision_counts.items())),
        "risk_counts": dict(sorted(risk_counts.items())),
        "rows": classified_rows,
        "admission_locked": True,
        "stable_dataset_modified": False,
        "baseline_modified": False,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def _status_icon(status: str) -> str:
    return {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(status, "⚪")


def _count_table(title: str, counts: dict[str, int]) -> list[str]:
    lines = [f"## {title}", "", "| Tipo | Conteo |", "|---|---:|"]
    if counts:
        for key, value in sorted(counts.items()):
            lines.append(f"| {key} | {value} |")
    else:
        lines.append("| Sin registros | 0 |")
    lines.append("")
    return lines


def to_markdown(plan: dict[str, Any]) -> str:
    status = str(plan["status"])
    lines: list[str] = [
        "# Plan de admisión estable S.N.E.-E.C.O.",
        "",
        "Aduana de admisión para evidencia externa observada después de RC1.",
        "",
        f"Estado: {_status_icon(status)} `{status}`",
        f"Motivo: {plan['reason']}",
        "",
        "## Métricas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Filas externas evaluadas | {plan['external_rows']} |",
        f"| Admitir más adelante | {plan['admit_later_rows']} |",
        f"| Retener para revisión de umbral | {plan['held_for_threshold_review_rows']} |",
        f"| Excluir hasta política definida | {plan['excluded_rows']} |",
        f"| Controles observacionales | {plan['observation_control_rows']} |",
        f"| Revisión manual | {plan['manual_review_rows']} |",
        "",
    ]

    lines.extend(_count_table("Decisiones de admisión", plan.get("decision_counts", {})))
    lines.extend(_count_table("Riesgo", plan.get("risk_counts", {})))

    lines.extend(
        [
            "## Matriz de admisión",
            "",
            "| source | dataset_action | admission_decision | gate | next_action | risk |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in plan.get("rows", []):
        lines.append(
            "| {source} | {dataset_action} | {admission_decision} | {gate} | {next_action} | {risk} |".format(
                **row
            )
        )

    lines.extend(
        [
            "",
            "## Candados de estabilidad",
            "",
            f"- Dataset estable modificado: `{plan['stable_dataset_modified']}`",
            f"- Baseline modificado: `{plan['baseline_modified']}`",
            f"- Admisión bloqueada hasta sprint futuro: `{plan['admission_locked']}`",
            "",
            "## Lectura operativa",
            "",
            "Este plan no incorpora todavía escenarios externos al dataset estable. Define una aduana: qué puede aspirar a entrar más adelante, qué queda retenido, qué se excluye temporalmente y qué se conserva como control observacional.",
            "",
            "## Límite responsable",
            "",
            str(plan["responsible_limit"]),
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(plan: dict[str, Any], output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(to_markdown(plan), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera plan de admisión estable S.N.E.-E.C.O. desde política externa.")
    parser.add_argument("--policy-json", type=Path, default=DEFAULT_POLICY_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    policy_payload = load_json(args.policy_json)
    plan = build_stable_admission_plan(policy_payload)
    write_outputs(plan, args.output_json, args.output_md)
    print("OK: plan de admisión estable S.N.E.-E.C.O. generado.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
