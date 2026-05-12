#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
OUTPUT_JSON = RESULTS_DIR / "eco_adaptive_dataset_readiness_gate.json"
OUTPUT_MD = RESULTS_DIR / "eco_adaptive_dataset_readiness_gate.md"

REQUIRED_FILES = [
    "docs/architecture/eco-adaptive-dataset-contract.md",
    "docs/architecture/eco-adaptive-dataset-example.json",
    "docs/architecture/eco-adaptive-dataset-example.md",
    "docs/operations/eco-adaptive-dataset-report-guide.md",
    "docs/operations/eco-adaptive-dataset-index.md",
    "scripts/validate_eco_adaptive_dataset_example.py",
    "scripts/run_eco_adaptive_dataset_report.py",
]

RESPONSIBLE_LIMITS = [
    "sin datos reales",
    "sin datos sensibles",
    "sin datos genéticos privados",
    "sin entrenamiento",
    "sin modificación de baseline",
    "sin recalibración de umbrales",
    "sin afirmaciones biomédicas aplicadas",
]


def build_report() -> dict:
    files = []
    missing = []

    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path
        exists = path.exists()
        files.append({"path": relative_path, "exists": exists})
        if not exists:
            missing.append(relative_path)

    status = "passed" if not missing else "failed"

    return {
        "status": status,
        "report_type": "adaptive_dataset_readiness_gate",
        "classification": "permitted",
        "required_files": files,
        "missing_files": missing,
        "ready_for_operational_review": not missing,
        "responsible_limits": RESPONSIBLE_LIMITS,
        "operational_reading": (
            "Paquete adaptativo sintético listo para revisión operativa."
            if not missing
            else "Paquete adaptativo incompleto; revisar archivos faltantes."
        ),
    }


def write_markdown(report: dict) -> str:
    lines = [
        "# E.C.O. adaptive dataset readiness gate",
        "",
        f"Estado: {report['status']}",
        f"Clasificación: {report['classification']}",
        f"Listo para revisión operativa: {report['ready_for_operational_review']}",
        "",
        "## Lectura operativa",
        "",
        report["operational_reading"],
        "",
        "## Archivos requeridos",
        "",
    ]

    for item in report["required_files"]:
        mark = "ok" if item["exists"] else "missing"
        lines.append(f"- {mark}: `{item['path']}`")

    lines.extend([
        "",
        "## Límites responsables",
        "",
    ])

    for limit in report["responsible_limits"]:
        lines.append(f"- {limit}")

    lines.extend([
        "",
        "## Uso recomendado",
        "",
        "- Usar como gate documental y operativo.",
        "- No usar como autorización para datos reales.",
        "- No usar para entrenamiento.",
        "- No usar para modificar baseline o umbrales.",
    ])

    return "\n".join(lines) + "\n"


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()

    OUTPUT_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_MD.write_text(write_markdown(report), encoding="utf-8")

    print("# E.C.O. adaptive dataset readiness gate")
    print(f"Estado: {report['status']}")
    print(f"Clasificación: {report['classification']}")
    print(f"Archivos requeridos: {len(report['required_files'])}")
    print(f"Archivos faltantes: {len(report['missing_files'])}")
    print(f"Salida JSON: {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Salida Markdown: {OUTPUT_MD.relative_to(ROOT)}")
    print("Límite: revisión sintética documental; sin datos reales; sin entrenamiento; sin baseline; sin recalibración.")

    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
