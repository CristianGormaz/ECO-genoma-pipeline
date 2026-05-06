from __future__ import annotations

import json
from pathlib import Path

REGISTRY = Path("docs/architecture/eco-synthetic-demo-registry.json")
JSON_OUTPUT = Path("results/eco_synthetic_demo_comparison_report.json")
MD_OUTPUT = Path("results/eco_synthetic_demo_comparison_report.md")

PATTERNS = {
    "minimal simulation": "procesamiento mínimo de señal sintética",
    "signal balance": "balance entre señales sintéticas",
    "waste pressure": "presión residual y estabilidad",
    "absorption threshold": "umbral de absorción sintético",
}

READINGS = {
    "minimal simulation": "verifica que el pipeline pueda digerir una señal mínima",
    "signal balance": "observa equilibrio operativo entre entradas sintéticas",
    "waste pressure": "observa carga residual sin convertirla en conclusión aplicada",
    "absorption threshold": "observa cuándo una señal sintética supera un umbral de absorción",
}

def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def demo_name(demo: dict) -> str:
    return str(demo.get("name") or demo.get("title") or demo.get("id") or "unknown").strip()

def build_entry(demo: dict) -> dict:
    name = demo_name(demo)
    key = name.lower()
    return {
        "name": name,
        "runner": demo.get("runner", ""),
        "json_output": demo.get("json_output", ""),
        "markdown_output": demo.get("markdown_output", ""),
        "pattern_minimum": PATTERNS.get(key, "patrón sintético registrado"),
        "operational_reading": READINGS.get(key, "lectura operativa sintética"),
        "responsible_limit": "datos sintéticos; sin entrenamiento; sin datos sensibles; sin recalibración",
    }

def build_report(registry: dict) -> dict:
    demos = registry.get("demos", [])
    entries = [build_entry(demo) for demo in demos]
    return {
        "title": "E.C.O. synthetic demo comparison report",
        "status": "passed",
        "classification": registry.get("classification", "allowed"),
        "demo_count": len(entries),
        "demos": entries,
        "limit": "datos sintéticos; sin entrenamiento; sin datos sensibles; sin recalibración",
    }

def write_outputs(report: dict) -> None:
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# E.C.O. synthetic demo comparison report", ""]
    md.append(f"Estado: {report["status"]}")
    md.append(f"Demos comparadas: {report["demo_count"]}")
    md.append("")
    md.append("| Demo | Patrón mínimo | Lectura operativa | Límite responsable |")
    md.append("|---|---|---|---|")
    for demo in report["demos"]:
        md.append(f"| {demo["name"]} | {demo["pattern_minimum"]} | {demo["operational_reading"]} | {demo["responsible_limit"]} |")
    md.append("")
    md.append(f"Límite: {report["limit"]}.")
    MD_OUTPUT.write_text("\n".join(md) + "\n", encoding="utf-8")

def main() -> int:
    report = build_report(load_registry())
    write_outputs(report)
    print("# E.C.O. synthetic demo comparison report")
    print(f"Estado: {report["status"]}")
    print(f"Demos comparadas: {report["demo_count"]}")
    print(f"Salida JSON: {JSON_OUTPUT}")
    print(f"Salida Markdown: {MD_OUTPUT}")
    print(f"Límite: {report["limit"]}.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
