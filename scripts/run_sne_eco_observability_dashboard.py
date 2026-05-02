from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFUSION_JSON = PROJECT_ROOT / "results" / "sne_eco_state_confusion_report.json"
DEFAULT_RECURRENCE_JSON = PROJECT_ROOT / "results" / "sne_eco_recurrence_audit.json"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_observability_dashboard.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_observability_dashboard.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera dashboard de observabilidad S.N.E.-E.C.O.")
    parser.add_argument("--confusion-json", type=Path, default=DEFAULT_CONFUSION_JSON)
    parser.add_argument("--recurrence-json", type=Path, default=DEFAULT_RECURRENCE_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--tests-passed", type=int, default=None)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta primero `make sne-state-confusion` "
            "y `python scripts/run_sne_eco_recurrence_audit.py`."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def build_dashboard(
    *,
    confusion_payload: dict[str, Any],
    recurrence_payload: dict[str, Any],
    tests_passed: int | None = None,
) -> dict[str, Any]:
    confused_routes = confusion_payload.get("confused_routes", []) or []
    suggested_focus = confusion_payload.get("suggested_focus", []) or []
    recurrence_rows = recurrence_payload.get("rows", []) or []
    confused_recurrence_rows = int(recurrence_payload.get("confused_recurrence_rows", 0) or 0)

    confused_count = len(confused_routes)
    recurrence_count = int(recurrence_payload.get("recurrence_rows", len(recurrence_rows)) or 0)
    default_state_routes = [
        route
        for route in confused_routes
        if isinstance(route, dict) and route.get("matched_rule") == "default_state"
    ]

    status = "green"
    status_reason = "Sin rutas confundidas ni recurrencias confundidas."
    if confused_count or confused_recurrence_rows:
        status = "red"
        status_reason = "Existen rutas confundidas o recurrencias confundidas."
    elif suggested_focus:
        status = "yellow"
        status_reason = "No hay confusión activa, pero existen focos sugeridos."

    return {
        "dashboard_name": "sne_eco_observability_dashboard",
        "status": status,
        "status_reason": status_reason,
        "tests_passed": tests_passed,
        "scenario_set": confusion_payload.get("scenario_set"),
        "test_rows": confusion_payload.get("test_rows"),
        "confused_routes": confused_count,
        "confused_recurrence_rows": confused_recurrence_rows,
        "recurrence_rows": recurrence_count,
        "default_state_confused_routes": len(default_state_routes),
        "suggested_focus": list(suggested_focus),
        "responsible_limit": (
            "Dashboard educativo/experimental; lee reportes existentes y no recalibra reglas. "
            "No representa desempeño general, no modela conciencia humana y no tiene uso clínico/forense."
        ),
    }


def to_markdown(payload: dict[str, Any]) -> str:
    status_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(str(payload["status"]), "⚪")
    tests = payload["tests_passed"] if payload["tests_passed"] is not None else "no informado"
    suggested_focus = payload.get("suggested_focus", []) or []

    lines = [
        "# Dashboard de observabilidad S.N.E.-E.C.O.",
        "",
        "Lectura consolidada de reportes existentes del pipeline adaptativo.",
        "",
        f"Estado: {status_icon} `{payload['status']}`",
        f"Motivo: {payload['status_reason']}",
        "",
        "## Métricas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Tests passing reportados | {tests} |",
        f"| Filas de prueba holdout | {payload['test_rows']} |",
        f"| Rutas confundidas | {payload['confused_routes']} |",
        f"| Rutas confundidas por default_state | {payload['default_state_confused_routes']} |",
        f"| Filas de recurrencia | {payload['recurrence_rows']} |",
        f"| Recurrencias confundidas | {payload['confused_recurrence_rows']} |",
        "",
        "## Focos sugeridos",
        "",
    ]

    if suggested_focus:
        lines.extend(f"- {item}" for item in suggested_focus)
    else:
        lines.append("- Sin focos activos.")

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "Este dashboard no ejecuta nuevas reglas ni modifica el baseline. Solo resume reportes JSON previamente generados.",
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
    confusion_payload = load_json(args.confusion_json)
    recurrence_payload = load_json(args.recurrence_json)
    payload = build_dashboard(
        confusion_payload=confusion_payload,
        recurrence_payload=recurrence_payload,
        tests_passed=args.tests_passed,
    )
    markdown = to_markdown(payload)

    write_json(args.output_json, payload)
    write_text(args.output_md, markdown)

    print(markdown)
    print("")
    print("OK: dashboard de observabilidad S.N.E.-E.C.O. generado.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
