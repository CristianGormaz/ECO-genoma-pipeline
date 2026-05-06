from __future__ import annotations

import json
from pathlib import Path


REGISTRY = Path("docs/architecture/eco-synthetic-demo-registry.json")
JSON_OUTPUT = Path("results/eco_synthetic_demos_suite_report.json")
MD_OUTPUT = Path("results/eco_synthetic_demos_suite_report.md")


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def build_report(registry: dict) -> dict:
    demos = registry.get("demos", [])
    return {
        "title": "E.C.O. synthetic demos suite report",
        "classification": registry.get("classification"),
        "data_policy": registry.get("data_policy"),
        "training": registry.get("training"),
        "sensitive_data": registry.get("sensitive_data"),
        "baseline_changed": registry.get("baseline_changed"),
        "threshold_recalibrated": registry.get("threshold_recalibrated"),
        "summary": {
            "registered_demos": len(demos),
            "demo_ids": [demo["id"] for demo in demos],
        },
        "demos": demos,
        "limits": [
            "No usa datos sensibles.",
            "No entrena modelos.",
            "No modifica baseline.",
            "No recalibra umbrales.",
            "No hace afirmaciones biomédicas aplicadas.",
        ],
    }


def write_markdown(report: dict) -> None:
    lines = [
        "# E.C.O. synthetic demos suite report",
        "",
        "Estado: operativo",
        "Clasificación: permitido",
        "",
        "## Resumen",
        "",
        f"- Demos registradas: {report['summary']['registered_demos']}",
        f"- Política de datos: {report['data_policy']}",
        f"- Entrenamiento: {report['training']}",
        f"- Datos sensibles: {report['sensitive_data']}",
        "",
        "## Demos",
        "",
    ]
    for demo in report["demos"]:
        lines.extend([
            f"### {demo['name']}",
            "",
            f"- ID: `{demo['id']}`",
            f"- Runner: `{demo['runner']}`",
            f"- JSON: `{demo['json_output']}`",
            f"- Markdown: `{demo['markdown_output']}`",
            "",
        ])
    lines.extend([
        "## Límite responsable",
        "",
        "- Datos sintéticos solamente.",
        "- Sin entrenamiento de modelos.",
        "- Sin datos sensibles.",
        "- Sin modificación de baseline.",
        "- Sin recalibración de umbrales.",
        "- Sin afirmaciones biomédicas aplicadas.",
    ])
    MD_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    registry = load_registry()
    report = build_report(registry)
    JSON_OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(report)
    print("# E.C.O. synthetic demos suite report")
    print("Estado: passed")
    print("Demos registradas: " + str(report["summary"]["registered_demos"]))
    print("Salida JSON: " + str(JSON_OUTPUT))
    print("Salida Markdown: " + str(MD_OUTPUT))
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin recalibración.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
