from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

JSON_OUTPUT = Path("results/eco_synthetic_operational_dashboard.json")
MD_OUTPUT = Path("results/eco_synthetic_operational_dashboard.md")

LIMIT = "datos sintéticos; sin entrenamiento; sin datos sensibles; sin modificación de baseline; sin recalibración; sin afirmaciones biomédicas aplicadas"
OK_STATUSES = {"passed", "green", "ok", "success"}

COMPONENTS = [
    {
        "id": "adaptive_dataset_readiness_gate",
        "label": "adaptive dataset readiness gate",
        "script": "scripts/run_eco_adaptive_dataset_readiness_gate.py",
        "output": Path("results/eco_adaptive_dataset_readiness_gate.json"),
    },

    {
        "id": "suite_report",
        "label": "synthetic demos suite report",
        "script": "scripts/run_eco_synthetic_demos_suite_report.py",
        "output": Path("results/eco_synthetic_demos_suite_report.json"),
    },
    {
        "id": "comparison_report",
        "label": "synthetic demo comparison report",
        "script": "scripts/run_eco_synthetic_demo_comparison_report.py",
        "output": Path("results/eco_synthetic_demo_comparison_report.json"),
    },
    {
        "id": "signal_matrix_report",
        "label": "synthetic signal matrix report",
        "script": "scripts/run_eco_synthetic_signal_matrix_report.py",
        "output": Path("results/eco_synthetic_signal_matrix_report.json"),
    },
    {
        "id": "adaptive_dataset_report",
        "label": "adaptive dataset operational report",
        "script": "scripts/run_eco_adaptive_dataset_report.py",
        "output": Path("results/eco_adaptive_dataset_report.json"),
    },
]


def normalize_status(payload: dict) -> str:
    raw_status = str(payload.get("status") or payload.get("estado") or "passed").lower()
    if raw_status in OK_STATUSES:
        return "passed"
    return raw_status


def run_component(component: dict) -> dict:
    result = subprocess.run([sys.executable, component["script"]], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    payload = json.loads(component["output"].read_text(encoding="utf-8"))
    status = normalize_status(payload)
    return {
        "id": component["id"],
        "label": component["label"],
        "status": status,
        "classification": payload.get("classification", "allowed"),
        "output": str(component["output"]),
    }


def build_dashboard() -> dict:
    components = [run_component(component) for component in COMPONENTS]
    passed = all(component["status"] == "passed" for component in components)
    return {
        "title": "E.C.O. synthetic operational dashboard",
        "status": "passed" if passed else "attention",
        "classification": "allowed",
        "component_count": len(components),
        "components": components,
        "limit": LIMIT,
    }


def write_outputs(dashboard: dict) -> None:
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# E.C.O. synthetic operational dashboard", ""]
    md.append("Estado: {}".format(dashboard["status"]))
    md.append("Componentes: {}".format(dashboard["component_count"]))
    md.append("")
    md.append("| Componente | Estado | Clasificación | Salida |")
    md.append("|---|---|---|---|")
    for component in dashboard["components"]:
        md.append("| {} | {} | {} | {} |".format(component["label"], component["status"], component["classification"], component["output"]))
    md.append("")
    md.append("Límite: {}.".format(dashboard["limit"]))
    MD_OUTPUT.write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> int:
    dashboard = build_dashboard()
    write_outputs(dashboard)
    print("# E.C.O. synthetic operational dashboard")
    print("Estado: {}".format(dashboard["status"]))
    print("Componentes: {}".format(dashboard["component_count"]))
    print("Salida JSON: {}".format(JSON_OUTPUT))
    print("Salida Markdown: {}".format(MD_OUTPUT))
    print("Límite: {}.".format(dashboard["limit"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
