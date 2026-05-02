from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_JSON = PROJECT_ROOT / "results" / "sne_eco_state_dataset.json"
DEFAULT_OBSERVABILITY_JSON = PROJECT_ROOT / "results" / "sne_eco_observability_dashboard.json"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_neurogastro_context_report.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_neurogastro_context_report.md"

RESPONSIBLE_LIMIT = (
    "Reporte educativo/experimental de arquitectura bioinspirada. "
    "Describe calidad de datos, rutas informacionales y estados internos del pipeline E.C.O.; "
    "no diagnostica enfermedades, no reemplaza evaluación médica, no modela conciencia humana "
    "y no tiene uso clínico/forense."
)

STATE_INTERPRETATIONS = {
    "stable": {
        "ux_label": "estable",
        "bioinspired_reading": "homeostasis informacional conservada",
        "plain_language": "el flujo puede seguir sin intervención especial",
        "suggested_action": "mantener observación y registrar métricas",
    },
    "watch": {
        "ux_label": "vigilancia",
        "bioinspired_reading": "aumento de señales que ameritan monitoreo",
        "plain_language": "el flujo sigue funcionando, pero conviene mirar de cerca",
        "suggested_action": "revisar ambigüedad, recurrencia o retención antes de escalar",
    },
    "attention": {
        "ux_label": "atención",
        "bioinspired_reading": "activación defensiva o tensión del flujo",
        "plain_language": "el sistema detectó condiciones que requieren revisión prioritaria",
        "suggested_action": "auditar defensa, barrera, rutas confundidas y límites responsables",
    },
}

NEUROGASTRO_CORRESPONDENCES = [
    {
        "concept": "interocepción",
        "eco_translation": "lectura interna del estado del pipeline",
        "observable_fields": ["state_before", "state_after", "immune_load_after", "quarantine_ratio_after"],
        "operational_use": "resumir cómo queda el sistema después de procesar cada paquete",
    },
    {
        "concept": "señal aferente",
        "eco_translation": "fila de transición que sube información hacia el reporte",
        "observable_fields": ["source", "defense_category", "motility_action", "final_decision"],
        "operational_use": "convertir señales locales en lectura comunicable",
    },
    {
        "concept": "predicción/error",
        "eco_translation": "diferencia entre ruta esperada y ruta observada",
        "observable_fields": ["confused_routes", "default_state_confused_routes", "suggested_focus"],
        "operational_use": "identificar focos de ajuste sin modificar el baseline estable",
    },
    {
        "concept": "homeostasis/allostasis",
        "eco_translation": "estado estable, vigilancia o atención según presión informacional",
        "observable_fields": ["stable", "watch", "attention"],
        "operational_use": "decidir si el flujo se mantiene, se vigila o se audita",
    },
    {
        "concept": "motilidad",
        "eco_translation": "movimiento operativo del paquete dentro del sistema",
        "observable_fields": ["motility_action", "final_decision"],
        "operational_use": "explicar si un dato avanza, se retiene, se rechaza o queda en revisión",
    },
    {
        "concept": "microbiota/memoria",
        "eco_translation": "registro de recurrencias y familiaridad informacional",
        "observable_fields": ["microbiota_seen_count", "recurrence_ratio_after"],
        "operational_use": "separar novedad, repetición útil y redundancia",
    },
    {
        "concept": "defensa/inmunidad informacional",
        "eco_translation": "detección de invalidez, ambigüedad o riesgo técnico",
        "observable_fields": ["defense_category", "defense_severity", "barrier_status"],
        "operational_use": "bloquear lectura clínica indebida y proteger estabilidad del pipeline",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera reporte neurogastrocomputacional seguro para S.N.E.-E.C.O."
    )
    parser.add_argument("--state-json", type=Path, default=DEFAULT_STATE_JSON)
    parser.add_argument("--observability-json", type=Path, default=DEFAULT_OBSERVABILITY_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser.parse_args()


def load_required_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta primero `make sne-state-dataset` "
            "o entrega una ruta con `--state-json`."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _count_rows(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(Counter(str(row.get(field, "unknown")) for row in rows))


def _overall_state(*, state_after_counts: dict[str, int], observability_payload: dict[str, Any]) -> str:
    dashboard_status = str(observability_payload.get("status", "")).lower()
    if dashboard_status == "red" or state_after_counts.get("attention", 0) > 0:
        return "attention"
    if dashboard_status == "yellow" or state_after_counts.get("watch", 0) > 0:
        return "watch"
    return "stable"


def _transition_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    transitions = Counter()
    for row in rows:
        before = str(row.get("state_before", "unknown"))
        after = str(row.get("state_after", "unknown"))
        transitions[f"{before}->{after}"] += 1
    return dict(transitions)


def _build_ux_reading(overall_state: str, metrics: dict[str, Any]) -> dict[str, str]:
    state_info = STATE_INTERPRETATIONS.get(overall_state, STATE_INTERPRETATIONS["watch"])
    attention_rows = metrics["state_after_counts"].get("attention", 0)
    watch_rows = metrics["state_after_counts"].get("watch", 0)
    confused_routes = metrics.get("confused_routes", 0)

    if attention_rows or confused_routes:
        cause = "hay señales de atención o confusión que justifican auditoría prioritaria"
    elif watch_rows:
        cause = "aparecen señales de vigilancia que conviene observar antes de cambiar reglas"
    else:
        cause = "las transiciones observadas no muestran tensión relevante del flujo"

    return {
        "state": state_info["ux_label"],
        "cause": cause,
        "suggested_action": state_info["suggested_action"],
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def build_neurogastro_context_report(
    *,
    state_payload: dict[str, Any],
    observability_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    observability = observability_payload or {}
    rows = list(state_payload.get("rows", []) or [])
    state_before_counts = _count_rows(rows, "state_before")
    state_after_counts = _count_rows(rows, "state_after")
    final_decision_counts = _count_rows(rows, "final_decision")
    defense_counts = _count_rows(rows, "defense_category")
    motility_counts = _count_rows(rows, "motility_action")
    overall_state = _overall_state(
        state_after_counts=state_after_counts,
        observability_payload=observability,
    )

    metrics = {
        "rows_evaluated": len(rows),
        "scenario_set": state_payload.get("scenario_set"),
        "state_before_counts": state_before_counts,
        "state_after_counts": state_after_counts,
        "state_transitions": _transition_counts(rows),
        "final_decision_counts": final_decision_counts,
        "defense_category_counts": defense_counts,
        "motility_action_counts": motility_counts,
        "confused_routes": int(observability.get("confused_routes", 0) or 0),
        "confused_recurrence_rows": int(observability.get("confused_recurrence_rows", 0) or 0),
        "default_state_confused_routes": int(observability.get("default_state_confused_routes", 0) or 0),
    }

    return {
        "report_name": "sne_eco_neurogastro_context_report",
        "status": overall_state,
        "status_reason": STATE_INTERPRETATIONS[overall_state]["bioinspired_reading"],
        "metrics": metrics,
        "state_interpretations": STATE_INTERPRETATIONS,
        "neurogastro_correspondences": NEUROGASTRO_CORRESPONDENCES,
        "ux_reading": _build_ux_reading(overall_state, metrics),
        "stability_locks": {
            "stable_dataset_modified": False,
            "baseline_modified": False,
            "rules_modified": False,
            "thresholds_modified": False,
            "report_only": True,
        },
        "claim_boundaries": {
            "clinical_diagnosis": False,
            "medical_advice": False,
            "human_consciousness_model": False,
            "forensic_use": False,
            "bioinspired_architecture": True,
        },
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def to_markdown(payload: dict[str, Any]) -> str:
    metrics = payload["metrics"]
    locks = payload["stability_locks"]
    ux = payload["ux_reading"]
    status_icon = {"stable": "🟢", "watch": "🟡", "attention": "🔴"}.get(
        str(payload["status"]), "⚪"
    )

    lines = [
        "# Reporte neurogastrocomputacional S.N.E.-E.C.O.",
        "",
        "Puente explicativo entre arquitectura entérica bioinspirada y métricas auditables del pipeline.",
        "",
        f"Estado: {status_icon} `{payload['status']}`",
        f"Motivo: {payload['status_reason']}",
        "",
        "## Lectura UX conversacional",
        "",
        f"- Estado: {ux['state']}",
        f"- Causa: {ux['cause']}",
        f"- Acción sugerida: {ux['suggested_action']}",
        f"- Límite: {ux['responsible_limit']}",
        "",
        "## Métricas observadas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Filas evaluadas | {metrics['rows_evaluated']} |",
        f"| Rutas confundidas | {metrics['confused_routes']} |",
        f"| Recurrencias confundidas | {metrics['confused_recurrence_rows']} |",
        f"| Confusión por default_state | {metrics['default_state_confused_routes']} |",
        "",
        "## Estados interpretables",
        "",
        "| Estado | Lectura bioinspirada | Lenguaje simple | Acción |",
        "|---|---|---|---|",
    ]

    for state, info in payload["state_interpretations"].items():
        lines.append(
            f"| `{state}` | {info['bioinspired_reading']} | "
            f"{info['plain_language']} | {info['suggested_action']} |"
        )

    lines.extend(
        [
            "",
            "## Correspondencias neurogastrocomputacionales",
            "",
            "| Concepto | Traducción E.C.O. | Campos observables | Uso operativo |",
            "|---|---|---|---|",
        ]
    )

    for item in payload["neurogastro_correspondences"]:
        fields = ", ".join(f"`{field}`" for field in item["observable_fields"])
        lines.append(
            f"| {item['concept']} | {item['eco_translation']} | {fields} | {item['operational_use']} |"
        )

    lines.extend(
        [
            "",
            "## Candados de estabilidad",
            "",
            f"- Dataset estable modificado: `{locks['stable_dataset_modified']}`",
            f"- Baseline modificado: `{locks['baseline_modified']}`",
            f"- Reglas modificadas: `{locks['rules_modified']}`",
            f"- Umbrales modificados: `{locks['thresholds_modified']}`",
            f"- Solo reporte: `{locks['report_only']}`",
            "",
            "## Límite responsable",
            "",
            payload["responsible_limit"],
        ]
    )
    return "\n".join(lines) + "\n"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    state_payload = load_required_json(args.state_json)
    observability_payload = load_optional_json(args.observability_json)
    payload = build_neurogastro_context_report(
        state_payload=state_payload,
        observability_payload=observability_payload,
    )
    markdown = to_markdown(payload)

    write_json(args.output_json, payload)
    write_text(args.output_md, markdown)

    print(markdown)
    print("OK: reporte neurogastrocomputacional S.N.E.-E.C.O. generado.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
