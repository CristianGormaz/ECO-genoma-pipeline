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

from scripts.run_sne_eco_external_scenario_probe import build_external_probe  # noqa: E402

DEFAULT_PROBE_JSON = PROJECT_ROOT / "results" / "sne_eco_external_scenario_probe.json"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_external_evidence_review.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_external_evidence_review.md"

RESPONSIBLE_LIMIT = (
    "Revisión educativa/experimental de evidencia externa; clasifica diferencias observadas "
    "sin modificar dataset estable, baseline, reglas ni umbrales. No representa desempeño general, "
    "no modela conciencia humana y no tiene uso clínico/forense."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clasifica evidencia externa S.N.E.-E.C.O.")
    parser.add_argument("--probe-json", type=Path, default=DEFAULT_PROBE_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--rebuild-probe", action="store_true")
    return parser.parse_args()


def load_probe(path: Path, *, rebuild_probe: bool = False) -> dict[str, Any]:
    if rebuild_probe or not path.exists():
        return build_external_probe()
    return json.loads(path.read_text(encoding="utf-8"))


def classify_row(row: dict[str, Any]) -> dict[str, Any]:
    source = str(row["source"])
    observed = str(row["observed_state"])
    predicted = str(row["predicted_state"])
    decision = str(row["final_decision"])
    defense = str(row["defense"])
    correct = bool(row["correct"])
    matched_rule = str(row["matched_rule"])

    if correct:
        category = "expected_external_alignment"
        action = "keep_as_observed_external_control"
        rationale = "La ruta externa coincide con la predicción del baseline y puede conservarse como control observacional."
    elif matched_rule == "default_state":
        category = "coverage_gap_high_priority"
        action = "review_before_any_stable_inclusion"
        rationale = "La ruta externa cayó en default_state; requiere revisión de cobertura antes de cualquier incorporación."
    elif decision == "absorb" and predicted == "stable" and observed == "watch":
        category = "external_context_boundary"
        action = "document_as_external_boundary"
        rationale = "El baseline reconoce familia absorbible estable, pero el contexto externo sostiene vigilancia por novedad."
    elif decision == "quarantine" and predicted == "attention" and observed == "watch":
        category = "expected_defensive_tension"
        action = "review_threshold_before_training"
        rationale = "La defensa sugiere atención, pero el estado observado conserva vigilancia; puede representar tensión defensiva externa."
    elif decision == "reject" and predicted == "attention" and observed == "watch":
        category = "expected_invalid_payload_tension"
        action = "keep_out_of_stable_dataset_until_policy_defined"
        rationale = "Payload inválido externo: no conviene entrenarlo todavía como ruta estable sin política explícita."
    else:
        category = "external_evidence_to_review"
        action = "manual_review_required"
        rationale = "Diferencia externa no clasificada por las reglas de revisión actuales."

    return {
        "source": source,
        "observed_state": observed,
        "predicted_state": predicted,
        "matched_rule": matched_rule,
        "final_decision": decision,
        "defense": defense,
        "correct": correct,
        "category": category,
        "recommended_action": action,
        "rationale": rationale,
    }


def build_evidence_review(probe_payload: dict[str, Any]) -> dict[str, Any]:
    reviewed_rows = [classify_row(row) for row in probe_payload.get("rows", [])]
    category_counts = Counter(row["category"] for row in reviewed_rows)
    action_counts = Counter(row["recommended_action"] for row in reviewed_rows)

    confused_rows = [row for row in reviewed_rows if not row["correct"]]
    default_state_rows = [row for row in reviewed_rows if row["matched_rule"] == "default_state"]
    candidate_rows = [
        row
        for row in reviewed_rows
        if row["category"] in {"external_context_boundary", "expected_defensive_tension"}
    ]

    status = "green"
    status_reason = "Evidencia externa revisada sin default_state ni riesgo inmediato."
    if confused_rows:
        status = "yellow"
        status_reason = "Existen diferencias externas clasificadas; revisar antes de incorporar al dataset estable."
    if default_state_rows:
        status = "red"
        status_reason = "Existe evidencia externa con default_state; priorizar revisión de cobertura."

    return {
        "review_name": "sne_eco_external_evidence_review",
        "source_probe": probe_payload.get("probe_name", "sne_eco_external_scenario_probe"),
        "external_rows": len(reviewed_rows),
        "external_differences": len(confused_rows),
        "default_state_rows": len(default_state_rows),
        "candidate_rows_for_future_review": len(candidate_rows),
        "status": status,
        "status_reason": status_reason,
        "category_counts": dict(category_counts),
        "action_counts": dict(action_counts),
        "rows": reviewed_rows,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def to_markdown(payload: dict[str, Any]) -> str:
    status_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(str(payload["status"]), "⚪")
    lines = [
        "# Revisión de evidencia externa S.N.E.-E.C.O.",
        "",
        "Clasificación de diferencias externas detectadas por la sonda observacional.",
        "",
        f"Estado: {status_icon} `{payload['status']}`",
        f"Motivo: {payload['status_reason']}",
        "",
        "## Métricas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Escenarios externos revisados | {payload['external_rows']} |",
        f"| Diferencias externas | {payload['external_differences']} |",
        f"| Rutas default_state | {payload['default_state_rows']} |",
        f"| Candidatos a revisión futura | {payload['candidate_rows_for_future_review']} |",
        "",
        "## Categorías",
        "",
        "| Categoría | Conteo |",
        "|---|---:|",
    ]
    for category, count in sorted(payload["category_counts"].items()):
        lines.append(f"| {category} | {count} |")

    lines.extend(
        [
            "",
            "## Matriz de revisión",
            "",
            "| source | observed | predicted | category | action |",
            "|---|---|---|---|---|",
        ]
    )
    for row in payload["rows"]:
        lines.append(
            "| "
            f"{row['source']} | "
            f"{row['observed_state']} | "
            f"{row['predicted_state']} | "
            f"{row['category']} | "
            f"{row['recommended_action']} |"
        )

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "Las diferencias externas no invalidan RC1. Esta revisión separa frontera esperable, tensión defensiva, payload inválido y candidatos a evaluación futura.",
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
    probe_payload = load_probe(args.probe_json, rebuild_probe=args.rebuild_probe)
    payload = build_evidence_review(probe_payload)
    markdown = to_markdown(payload)

    write_json(args.output_json, payload)
    write_text(args.output_md, markdown)

    print(markdown)
    print("")
    print("OK: revisión de evidencia externa S.N.E.-E.C.O. generada.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
