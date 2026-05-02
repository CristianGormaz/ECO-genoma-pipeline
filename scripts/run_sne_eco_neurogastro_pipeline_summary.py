from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DASHBOARD_JSON = PROJECT_ROOT / "results" / "sne_eco_observability_dashboard.json"
DEFAULT_NEURO_JSON = PROJECT_ROOT / "results" / "sne_eco_neurogastro_context_report.json"
DEFAULT_RECURRENCE_JSON = PROJECT_ROOT / "results" / "sne_eco_recurrence_audit.json"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_neurogastro_pipeline_summary.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_neurogastro_pipeline_summary.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera resumen ejecutivo del pipeline neurogastrocomputacional S.N.E.-E.C.O."
    )
    parser.add_argument("--dashboard-json", type=Path, default=DEFAULT_DASHBOARD_JSON)
    parser.add_argument("--neurogastro-json", type=Path, default=DEFAULT_NEURO_JSON)
    parser.add_argument("--recurrence-json", type=Path, default=DEFAULT_RECURRENCE_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta primero `make sne-neurogastro-pipeline`."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def build_summary(
    *,
    dashboard_payload: dict[str, Any],
    neurogastro_payload: dict[str, Any],
    recurrence_payload: dict[str, Any],
) -> dict[str, Any]:
    neuro_metrics = neurogastro_payload.get("metrics", {}) or {}
    ux = neurogastro_payload.get("ux_reading", {}) or {}
    status = str(neurogastro_payload.get("status", "watch"))
    confused_routes = int(dashboard_payload.get("confused_routes", 0) or 0)
    confused_recurrences = int(
        dashboard_payload.get(
            "confused_recurrence_rows",
            recurrence_payload.get("confused_recurrence_rows", 0),
        )
        or 0
    )

    if confused_routes or confused_recurrences:
        cause = "existen rutas o recurrencias confundidas que requieren revisión dirigida"
        action = "documentar foco, comparar contra RC1 y evitar recalibrar sin evidencia"
    elif status == "attention":
        cause = "hay tensión interna por señales defensivas, aunque sin confusión de rutas"
        action = ux.get(
            "suggested_action",
            "auditar defensa, barrera y límites responsables",
        )
    elif status == "watch":
        cause = "el flujo está operativo, pero mantiene señales de vigilancia"
        action = ux.get(
            "suggested_action",
            "observar antes de modificar reglas",
        )
    else:
        cause = "no se observan tensiones relevantes en rutas ni recurrencias"
        action = ux.get(
            "suggested_action",
            "mantener observación y registrar métricas",
        )

    return {
        "report_name": "sne_eco_neurogastro_pipeline_summary",
        "status": status,
        "dashboard_status": dashboard_payload.get("status"),
        "cause": cause,
        "suggested_action": action,
        "metrics": {
            "rows_evaluated": int(neuro_metrics.get("rows_evaluated", 0) or 0),
            "confused_routes": confused_routes,
            "confused_recurrence_rows": confused_recurrences,
            "default_state_confused_routes": int(
                dashboard_payload.get("default_state_confused_routes", 0) or 0
            ),
            "recurrence_rows": int(recurrence_payload.get("recurrence_rows", 0) or 0),
        },
        "stability_locks": {
            "stable_dataset_modified": False,
            "baseline_modified": False,
            "rules_modified": False,
            "thresholds_modified": False,
            "summary_only": True,
        },
        "responsible_limit": neurogastro_payload.get(
            "responsible_limit",
            "Resumen técnico/educativo; interpretar como lectura del pipeline, no como conclusión externa.",
        ),
    }


def to_markdown(payload: dict[str, Any]) -> str:
    icon = {"stable": "🟢", "watch": "🟡", "attention": "🔴"}.get(
        str(payload["status"]), "⚪"
    )
    metrics = payload["metrics"]
    locks = payload["stability_locks"]

    lines = [
        "# Resumen ejecutivo neurogastrocomputacional S.N.E.-E.C.O.",
        "",
        f"Estado general: {icon} `{payload['status']}`",
        f"Estado del dashboard: `{payload['dashboard_status']}`",
        "",
        "## Lectura rápida",
        "",
        f"- Causa principal: {payload['cause']}",
        f"- Acción sugerida: {payload['suggested_action']}",
        "",
        "## Métricas clave",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Filas evaluadas | {metrics['rows_evaluated']} |",
        f"| Rutas confundidas | {metrics['confused_routes']} |",
        f"| Recurrencias confundidas | {metrics['confused_recurrence_rows']} |",
        f"| Confusión por default_state | {metrics['default_state_confused_routes']} |",
        f"| Filas de recurrencia | {metrics['recurrence_rows']} |",
        "",
        "## Candados",
        "",
        f"- Dataset estable modificado: `{locks['stable_dataset_modified']}`",
        f"- Baseline modificado: `{locks['baseline_modified']}`",
        f"- Reglas modificadas: `{locks['rules_modified']}`",
        f"- Umbrales modificados: `{locks['thresholds_modified']}`",
        f"- Solo resumen: `{locks['summary_only']}`",
        "",
        "## Límite responsable",
        "",
        str(payload["responsible_limit"]),
    ]
    return "\n".join(lines) + "\n"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    payload = build_summary(
        dashboard_payload=load_json(args.dashboard_json),
        neurogastro_payload=load_json(args.neurogastro_json),
        recurrence_payload=load_json(args.recurrence_json),
    )
    markdown = to_markdown(payload)

    write_json(args.output_json, payload)
    write_text(args.output_md, markdown)

    print(markdown)
    print("OK: resumen ejecutivo neurogastrocomputacional S.N.E.-E.C.O. generado.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
