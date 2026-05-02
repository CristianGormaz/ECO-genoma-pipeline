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

from scripts.run_sne_eco_external_evidence_review import build_evidence_review, load_probe  # noqa: E402

DEFAULT_REVIEW_JSON = PROJECT_ROOT / "results" / "sne_eco_external_evidence_review.json"
DEFAULT_PROBE_JSON = PROJECT_ROOT / "results" / "sne_eco_external_scenario_probe.json"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_external_evidence_policy.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_external_evidence_policy.md"

RESPONSIBLE_LIMIT = (
    "Política educativa/experimental para evidencia externa; define decisiones de gobernanza "
    "sin modificar dataset estable, baseline, reglas ni umbrales. No representa desempeño general, "
    "no modela conciencia humana y no tiene uso clínico/forense."
)

POLICY_BY_CATEGORY: dict[str, dict[str, str]] = {
    "expected_external_alignment": {
        "policy_decision": "observe_as_control",
        "dataset_action": "do_not_train_yet",
        "risk_level": "low",
        "rationale": "La ruta externa coincide con el baseline y puede conservarse como control observacional.",
    },
    "external_context_boundary": {
        "policy_decision": "document_boundary",
        "dataset_action": "candidate_for_future_stable_scenario",
        "risk_level": "medium",
        "rationale": "La diferencia parece explicarse por frontera de contexto externo; documentar antes de entrenar.",
    },
    "expected_defensive_tension": {
        "policy_decision": "observe_threshold_candidate",
        "dataset_action": "candidate_for_threshold_review",
        "risk_level": "medium",
        "rationale": "Existe tensión defensiva esperable; revisar umbrales solo en sprint experimental futuro.",
    },
    "expected_invalid_payload_tension": {
        "policy_decision": "exclude_until_policy_defined",
        "dataset_action": "keep_out_of_stable_dataset",
        "risk_level": "medium",
        "rationale": "Payload inválido externo; no incorporarlo como estable sin política específica de invalidez.",
    },
    "coverage_gap_high_priority": {
        "policy_decision": "block_until_reviewed",
        "dataset_action": "do_not_include_until_coverage_review",
        "risk_level": "high",
        "rationale": "La ruta cayó en default_state; priorizar revisión antes de cualquier incorporación.",
    },
    "external_evidence_to_review": {
        "policy_decision": "manual_review",
        "dataset_action": "do_not_train_yet",
        "risk_level": "medium",
        "rationale": "Ruta externa sin clasificación suficiente; requiere revisión manual.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Define política para evidencia externa S.N.E.-E.C.O.")
    parser.add_argument("--review-json", type=Path, default=DEFAULT_REVIEW_JSON)
    parser.add_argument("--probe-json", type=Path, default=DEFAULT_PROBE_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--rebuild-review", action="store_true")
    return parser.parse_args()


def load_review(path: Path, *, probe_path: Path = DEFAULT_PROBE_JSON, rebuild_review: bool = False) -> dict[str, Any]:
    if rebuild_review or not path.exists():
        probe_payload = load_probe(probe_path, rebuild_probe=not probe_path.exists())
        return build_evidence_review(probe_payload)
    return json.loads(path.read_text(encoding="utf-8"))


def apply_policy(row: dict[str, Any]) -> dict[str, Any]:
    category = str(row.get("category", "external_evidence_to_review"))
    policy = POLICY_BY_CATEGORY.get(category, POLICY_BY_CATEGORY["external_evidence_to_review"])

    return {
        "source": row["source"],
        "category": category,
        "observed_state": row.get("observed_state"),
        "predicted_state": row.get("predicted_state"),
        "policy_decision": policy["policy_decision"],
        "dataset_action": policy["dataset_action"],
        "risk_level": policy["risk_level"],
        "rationale": policy["rationale"],
    }


def build_evidence_policy(review_payload: dict[str, Any]) -> dict[str, Any]:
    policy_rows = [apply_policy(row) for row in review_payload.get("rows", [])]
    decision_counts = Counter(row["policy_decision"] for row in policy_rows)
    dataset_action_counts = Counter(row["dataset_action"] for row in policy_rows)
    risk_counts = Counter(row["risk_level"] for row in policy_rows)

    high_risk_rows = [row for row in policy_rows if row["risk_level"] == "high"]
    future_candidates = [
        row
        for row in policy_rows
        if row["dataset_action"] in {"candidate_for_future_stable_scenario", "candidate_for_threshold_review"}
    ]
    excluded_rows = [row for row in policy_rows if row["dataset_action"] == "keep_out_of_stable_dataset"]

    status = "green"
    status_reason = "Política generada sin evidencia externa de alto riesgo."
    if future_candidates or excluded_rows:
        status = "yellow"
        status_reason = "Existen candidatos o exclusiones temporales; revisar antes de incorporar al dataset estable."
    if high_risk_rows:
        status = "red"
        status_reason = "Existe evidencia externa de alto riesgo; bloquear incorporación hasta revisión de cobertura."

    return {
        "policy_name": "sne_eco_external_evidence_policy",
        "source_review": review_payload.get("review_name", "sne_eco_external_evidence_review"),
        "external_rows": len(policy_rows),
        "future_candidate_rows": len(future_candidates),
        "excluded_rows": len(excluded_rows),
        "high_risk_rows": len(high_risk_rows),
        "status": status,
        "status_reason": status_reason,
        "decision_counts": dict(decision_counts),
        "dataset_action_counts": dict(dataset_action_counts),
        "risk_counts": dict(risk_counts),
        "rows": policy_rows,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def to_markdown(payload: dict[str, Any]) -> str:
    status_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(str(payload["status"]), "⚪")
    lines = [
        "# Política de evidencia externa S.N.E.-E.C.O.",
        "",
        "Política de decisión para evidencia externa observada después de RC1.",
        "",
        f"Estado: {status_icon} `{payload['status']}`",
        f"Motivo: {payload['status_reason']}",
        "",
        "## Métricas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Filas externas evaluadas | {payload['external_rows']} |",
        f"| Candidatos futuros | {payload['future_candidate_rows']} |",
        f"| Exclusiones temporales | {payload['excluded_rows']} |",
        f"| Alto riesgo | {payload['high_risk_rows']} |",
        "",
        "## Decisiones de política",
        "",
        "| Decisión | Conteo |",
        "|---|---:|",
    ]
    for decision, count in sorted(payload["decision_counts"].items()):
        lines.append(f"| {decision} | {count} |")

    lines.extend([
        "",
        "## Acciones sobre dataset",
        "",
        "| Acción | Conteo |",
        "|---|---:|",
    ])
    for action, count in sorted(payload["dataset_action_counts"].items()):
        lines.append(f"| {action} | {count} |")

    lines.extend([
        "",
        "## Matriz de política",
        "",
        "| source | category | decision | dataset_action | risk |",
        "|---|---|---|---|---|",
    ])
    for row in payload["rows"]:
        lines.append(
            "| "
            f"{row['source']} | "
            f"{row['category']} | "
            f"{row['policy_decision']} | "
            f"{row['dataset_action']} | "
            f"{row['risk_level']} |"
        )

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "Esta política no decide entrenar todavía. Ordena la evidencia externa para que un sprint futuro pueda decidir con trazabilidad qué se documenta, qué se observa, qué se excluye y qué puede convertirse en escenario estable.",
            "",
            "## Límite responsable",
            "",
            str(payload["responsible_limit"]),
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    review_payload = load_review(args.review_json, probe_path=args.probe_json, rebuild_review=args.rebuild_review)
    payload = build_evidence_policy(review_payload)
    markdown = to_markdown(payload)

    write_json(args.output_json, payload)
    write_text(args.output_md, markdown)

    print(markdown)
    print("")
    print("OK: política de evidencia externa S.N.E.-E.C.O. generada.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
