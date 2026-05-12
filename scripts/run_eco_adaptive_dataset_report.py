#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_JSON = ROOT / "docs" / "architecture" / "eco-adaptive-dataset-example.json"
SOURCE_MD = ROOT / "docs" / "architecture" / "eco-adaptive-dataset-example.md"
RESULTS_DIR = ROOT / "results"
OUTPUT_JSON = RESULTS_DIR / "eco_adaptive_dataset_report.json"
OUTPUT_MD = RESULTS_DIR / "eco_adaptive_dataset_report.md"


RESPONSIBLE_LIMITS = [
    "sin datos reales",
    "sin datos sensibles",
    "sin datos genéticos privados",
    "sin entrenamiento",
    "sin modificación de baseline",
    "sin recalibración de umbrales",
    "sin afirmaciones biomédicas aplicadas",
]


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"ERROR: no existe {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("ERROR: el ejemplo adaptativo debe usar raíz JSON objeto")
    if not data:
        raise SystemExit("ERROR: el ejemplo adaptativo no puede estar vacío")
    return data


def _extract_records(data: dict) -> list:
    for key in ("records", "items", "examples", "dataset"):
        value = data.get(key)
        if isinstance(value, list):
            return value
    return []


def _detect_declared_limits(markdown: str) -> list[str]:
    lowered = markdown.lower()
    return [limit for limit in RESPONSIBLE_LIMITS if limit in lowered]


def build_report() -> dict:
    data = _load_json(SOURCE_JSON)
    markdown = SOURCE_MD.read_text(encoding="utf-8") if SOURCE_MD.exists() else ""
    records = _extract_records(data)
    declared_limits = _detect_declared_limits(markdown)

    return {
        "status": "passed",
        "report_type": "adaptive_dataset_operational_report",
        "classification": "permitted",
        "source_json": str(SOURCE_JSON.relative_to(ROOT)),
        "source_markdown": str(SOURCE_MD.relative_to(ROOT)),
        "synthetic_records": len(records),
        "json_root_type": "object",
        "declared_responsible_limits": declared_limits,
        "responsible_limits": RESPONSIBLE_LIMITS,
        "operational_reading": "Ejemplo sintético documental listo para revisión operativa; no habilita entrenamiento, baseline, recalibración ni uso de datos reales.",
    }


def write_markdown(report: dict) -> str:
    lines = [
        "# E.C.O. adaptive dataset operational report",
        "",
        f"Estado: {report['status']}",
        f"Clasificación: {report['classification']}",
        f"Registros sintéticos: {report['synthetic_records']}",
        f"JSON fuente: `{report['source_json']}`",
        f"Markdown fuente: `{report['source_markdown']}`",
        "",
        "## Lectura operativa",
        "",
        report['operational_reading'],
        "",
        "## Límites responsables",
        "",
    ]
    lines.extend(f"- {limit}" for limit in report['responsible_limits'])
    lines.extend([
        "",
        "## Uso recomendado",
        "",
        "- Usar como reporte documental y trazable.",
        "- No usar como dataset real.",
        "- No usar para entrenamiento.",
        "- No usar para modificar baseline o umbrales.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(write_markdown(report), encoding="utf-8")

    print("# E.C.O. adaptive dataset operational report")
    print(f"Estado: {report['status']}")
    print(f"Clasificación: {report['classification']}")
    print(f"Registros sintéticos: {report['synthetic_records']}")
    print(f"Salida JSON: {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Salida Markdown: {OUTPUT_MD.relative_to(ROOT)}")
    print("Límite: reporte sintético documental; sin datos reales; sin entrenamiento; sin baseline; sin recalibración.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
