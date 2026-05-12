#!/usr/bin/env python3
from __future__ import annotations

import json
import unicodedata
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

LIMIT_KEYS = {
    "sin datos reales": "no_real_data",
    "sin datos sensibles": "no_sensitive_data",
    "sin datos genéticos privados": "no_private_genetic_data",
    "sin entrenamiento": "no_training",
    "sin modificación de baseline": "no_baseline_change",
    "sin recalibración de umbrales": "no_threshold_recalibration",
    "sin afirmaciones biomédicas aplicadas": "no_biomedical_claims",
}

LIMIT_ALIASES = {
    "sin datos reales": ["sin datos reales", "no contiene datos reales"],
    "sin datos sensibles": ["sin datos sensibles", "no contiene datos sensibles"],
    "sin datos genéticos privados": [
        "sin datos genéticos privados",
        "sin datos geneticos privados",
        "no contiene datos genéticos privados",
        "no contiene datos geneticos privados",
    ],
    "sin entrenamiento": ["sin entrenamiento", "no entrena modelos", "sin entrenar modelos"],
    "sin modificación de baseline": [
        "sin modificación de baseline",
        "sin modificacion de baseline",
        "no modifica baseline",
    ],
    "sin recalibración de umbrales": [
        "sin recalibración de umbrales",
        "sin recalibracion de umbrales",
        "no recalibra umbrales",
    ],
    "sin afirmaciones biomédicas aplicadas": [
        "sin afirmaciones biomédicas aplicadas",
        "sin afirmaciones biomedicas aplicadas",
        "no genera afirmaciones biomédicas aplicadas",
        "no genera afirmaciones biomedicas aplicadas",
    ],
}

ALLOWED_CLASSIFICATIONS = {"permitido", "permitted", "allowed"}


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"ERROR: no existe {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("ERROR: el ejemplo adaptativo debe usar raíz JSON objeto")
    if not data:
        raise SystemExit("ERROR: el ejemplo adaptativo no puede estar vacío")
    return data


def _load_markdown(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"ERROR: no existe {path}")
    markdown = path.read_text(encoding="utf-8")
    if not markdown.strip():
        raise SystemExit("ERROR: el Markdown adaptativo no puede estar vacío")
    return markdown


def _extract_records(data: dict) -> list:
    for key in ("records", "items", "examples", "dataset"):
        value = data.get(key)
        if isinstance(value, list):
            if not value:
                raise SystemExit("ERROR: el ejemplo adaptativo no contiene registros")
            return value
    raise SystemExit("ERROR: el ejemplo adaptativo no contiene lista de registros")


def _normalize_classification(data: dict) -> str:
    raw = str(data.get("classification", "")).strip().lower()
    normalized = _normalize_text(raw)
    if normalized not in ALLOWED_CLASSIFICATIONS:
        raise SystemExit(f"ERROR: clasificación adaptativa no permitida: {raw or 'vacía'}")
    return "permitted"


def _detect_source_limits(data: dict) -> list[str]:
    limits = data.get("limits")
    if not isinstance(limits, dict):
        raise SystemExit("ERROR: el ejemplo adaptativo no declara limits como objeto")

    detected = []
    missing = []
    for label, key in LIMIT_KEYS.items():
        if limits.get(key) is True:
            detected.append(label)
        else:
            missing.append(key)

    if missing:
        raise SystemExit("ERROR: faltan límites responsables activos en JSON: " + ", ".join(missing))

    return detected


def _detect_declared_limits(markdown: str) -> list[str]:
    lowered = _normalize_text(markdown)
    detected = []

    for limit, aliases in LIMIT_ALIASES.items():
        if any(_normalize_text(alias) in lowered for alias in aliases):
            detected.append(limit)

    missing = [limit for limit in RESPONSIBLE_LIMITS if limit not in detected]
    if missing:
        raise SystemExit("ERROR: faltan límites responsables declarados en Markdown: " + ", ".join(missing))

    return detected


def build_report() -> dict:
    data = _load_json(SOURCE_JSON)
    markdown = _load_markdown(SOURCE_MD)
    records = _extract_records(data)
    classification = _normalize_classification(data)
    source_limits = _detect_source_limits(data)
    declared_limits = _detect_declared_limits(markdown)

    return {
        "status": "passed",
        "report_type": "adaptive_dataset_operational_report",
        "classification": classification,
        "source_json": str(SOURCE_JSON.relative_to(ROOT)),
        "source_markdown": str(SOURCE_MD.relative_to(ROOT)),
        "synthetic_records": len(records),
        "json_root_type": "object",
        "source_responsible_limits": source_limits,
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
        report["operational_reading"],
        "",
        "## Límites responsables detectados en fuente",
        "",
    ]
    lines.extend(f"- {limit}" for limit in report["source_responsible_limits"])
    lines.extend([
        "",
        "## Límites responsables declarados en Markdown",
        "",
    ])
    lines.extend(f"- {limit}" for limit in report["declared_responsible_limits"])
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
    print(f"Límites JSON: {len(report['source_responsible_limits'])}")
    print(f"Límites Markdown: {len(report['declared_responsible_limits'])}")
    print(f"Salida JSON: {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Salida Markdown: {OUTPUT_MD.relative_to(ROOT)}")
    print("Límite: reporte sintético documental; sin datos reales; sin entrenamiento; sin baseline; sin recalibración.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
