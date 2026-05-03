from __future__ import annotations

import json
from pathlib import Path


BASELINE_PATH = Path("baselines/sne-eco-v1.1-snapshot.json")
DASHBOARD_PATH = Path("results/sne_eco_observability_dashboard.json")
OUTPUT_JSON = Path("results/sne_eco_compare_against_v1_1.json")
OUTPUT_MD = Path("results/sne_eco_compare_against_v1_1.md")


RESPONSIBLE_LIMIT = (
    "Comparación educativa/experimental contra baseline v1.1; "
    "no ejecuta nuevas reglas, no recalibra umbrales, no modifica el baseline "
    "y no tiene uso clínico, diagnóstico, forense ni modela conciencia humana."
)


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"ERROR: no existe el archivo requerido: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def find_int(data: dict, keys: list[str], default: int = 0) -> int:
    for key in keys:
        value = data.get(key)
        if isinstance(value, int):
            return value

    metrics = data.get("metrics", {})
    if isinstance(metrics, dict):
        for key in keys:
            value = metrics.get(key)
            if isinstance(value, int):
                return value

    return default


def build_comparison() -> dict:
    baseline = load_json(BASELINE_PATH)
    dashboard = load_json(DASHBOARD_PATH)

    current_confused = find_int(
        dashboard,
        ["confused_routes", "rutas_confundidas"],
    )
    current_recurrence_confused = find_int(
        dashboard,
        ["recurrence_confused", "confused_recurrences", "recurrencias_confundidas"],
    )
    current_default_confused = find_int(
        dashboard,
        ["default_state_confused", "default_state_confused_routes"],
    )

    baseline_confused = find_int(baseline, ["confused_routes"])
    baseline_recurrence_confused = find_int(baseline, ["recurrence_confused"])
    baseline_default_confused = find_int(baseline, ["default_state_confused"])

    regressions = []

    if current_confused > baseline_confused:
        regressions.append("confused_routes_increased")

    if current_recurrence_confused > baseline_recurrence_confused:
        regressions.append("recurrence_confused_increased")

    if current_default_confused > baseline_default_confused:
        regressions.append("default_state_confused_increased")

    status = "green" if not regressions else "attention"

    return {
        "baseline": baseline.get("version", "sne-eco-v1.1"),
        "status": status,
        "current": {
            "confused_routes": current_confused,
            "recurrence_confused": current_recurrence_confused,
            "default_state_confused": current_default_confused,
        },
        "baseline_metrics": {
            "confused_routes": baseline_confused,
            "recurrence_confused": baseline_recurrence_confused,
            "default_state_confused": baseline_default_confused,
        },
        "regressions": regressions,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def to_markdown(report: dict) -> str:
    icon = "🟢" if report["status"] == "green" else "🔴"

    lines = [
        "# Comparación S.N.E.-E.C.O. contra baseline v1.1",
        "",
        f"Baseline: `{report['baseline']}`",
        f"Estado: {icon} `{report['status']}`",
        "",
        "## Métricas comparadas",
        "",
        "| Métrica | Baseline v1.1 | Actual |",
        "|---|---:|---:|",
    ]

    for key in ["confused_routes", "recurrence_confused", "default_state_confused"]:
        lines.append(
            f"| `{key}` | {report['baseline_metrics'][key]} | {report['current'][key]} |"
        )

    lines.extend(
        [
            "",
            "## Regresiones detectadas",
            "",
        ]
    )

    if report["regressions"]:
        for item in report["regressions"]:
            lines.append(f"- {item}")
    else:
        lines.append("- Sin regresiones respecto a baseline v1.1.")

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "Esta comparación permite revisar si el estado actual mantiene la estabilidad congelada en v1.1.",
            "",
            "## Límite responsable",
            "",
            report["responsible_limit"],
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    report = build_comparison()

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    print(to_markdown(report))
    print("OK: comparación contra baseline v1.1 generada.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
