from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DASHBOARD_JSON = PROJECT_ROOT / "results" / "sne_eco_observability_dashboard.json"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_compare_against_rc1.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_compare_against_rc1.md"

RC1_BASELINE = {
    "tag": "sne-eco-v1.0-rc1",
    "tests_passed": 153,
    "confused_routes": 0,
    "confused_recurrence_rows": 0,
    "default_state_confused_routes": 0,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compara el estado S.N.E.-E.C.O. actual contra RC1.")
    parser.add_argument("--dashboard-json", type=Path, default=DEFAULT_DASHBOARD_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--baseline-tag", default=RC1_BASELINE["tag"])
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta primero `python scripts/run_sne_eco_observability_dashboard.py`."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _as_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    return int(value)


def build_comparison(*, dashboard_payload: dict[str, Any], baseline_tag: str = RC1_BASELINE["tag"]) -> dict[str, Any]:
    current = {
        "tests_passed": _as_int(dashboard_payload.get("tests_passed"), default=0),
        "confused_routes": _as_int(dashboard_payload.get("confused_routes"), default=0),
        "confused_recurrence_rows": _as_int(dashboard_payload.get("confused_recurrence_rows"), default=0),
        "default_state_confused_routes": _as_int(dashboard_payload.get("default_state_confused_routes"), default=0),
        "dashboard_status": dashboard_payload.get("status"),
    }

    baseline = dict(RC1_BASELINE)
    baseline["tag"] = baseline_tag

    deltas = {
        "tests_passed": current["tests_passed"] - baseline["tests_passed"],
        "confused_routes": current["confused_routes"] - baseline["confused_routes"],
        "confused_recurrence_rows": current["confused_recurrence_rows"] - baseline["confused_recurrence_rows"],
        "default_state_confused_routes": current["default_state_confused_routes"] - baseline["default_state_confused_routes"],
    }

    regressions: list[str] = []
    if current["tests_passed"] < baseline["tests_passed"]:
        regressions.append("tests_passed_below_rc1")
    if current["confused_routes"] > baseline["confused_routes"]:
        regressions.append("confused_routes_increased")
    if current["confused_recurrence_rows"] > baseline["confused_recurrence_rows"]:
        regressions.append("confused_recurrence_rows_increased")
    if current["default_state_confused_routes"] > baseline["default_state_confused_routes"]:
        regressions.append("default_state_confused_routes_increased")
    if current["dashboard_status"] == "red":
        regressions.append("dashboard_red")

    status = "green" if not regressions else "red"
    if current["dashboard_status"] == "yellow" and not regressions:
        status = "yellow"

    return {
        "comparison_name": "sne_eco_compare_against_rc1",
        "baseline": baseline,
        "current": current,
        "deltas": deltas,
        "status": status,
        "regressions": regressions,
        "responsible_limit": (
            "Comparación educativa/experimental contra RC1; no ejecuta nuevas reglas, "
            "no recalibra el baseline y no representa desempeño general, clínico ni forense."
        ),
    }


def to_markdown(payload: dict[str, Any]) -> str:
    status_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(str(payload["status"]), "⚪")
    baseline = payload["baseline"]
    current = payload["current"]
    deltas = payload["deltas"]
    regressions = payload.get("regressions", []) or []

    lines = [
        "# Comparación S.N.E.-E.C.O. contra RC1",
        "",
        f"Baseline: `{baseline['tag']}`",
        f"Estado: {status_icon} `{payload['status']}`",
        "",
        "## Métricas comparadas",
        "",
        "| Métrica | RC1 | Actual | Delta |",
        "|---|---:|---:|---:|",
        f"| Tests passing | {baseline['tests_passed']} | {current['tests_passed']} | {deltas['tests_passed']} |",
        f"| Rutas confundidas | {baseline['confused_routes']} | {current['confused_routes']} | {deltas['confused_routes']} |",
        f"| Recurrencias confundidas | {baseline['confused_recurrence_rows']} | {current['confused_recurrence_rows']} | {deltas['confused_recurrence_rows']} |",
        f"| Rutas default_state confundidas | {baseline['default_state_confused_routes']} | {current['default_state_confused_routes']} | {deltas['default_state_confused_routes']} |",
        "",
        "## Regresiones detectadas",
        "",
    ]

    if regressions:
        lines.extend(f"- {item}" for item in regressions)
    else:
        lines.append("- Sin regresiones respecto a RC1.")

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "Esta comparación usa el dashboard actual como entrada y contrasta sus métricas contra la línea base RC1 congelada.",
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
    dashboard_payload = load_json(args.dashboard_json)
    payload = build_comparison(dashboard_payload=dashboard_payload, baseline_tag=args.baseline_tag)
    markdown = to_markdown(payload)

    write_json(args.output_json, payload)
    write_text(args.output_md, markdown)

    print(markdown)
    print("")
    print("OK: comparación S.N.E.-E.C.O. contra RC1 generada.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
