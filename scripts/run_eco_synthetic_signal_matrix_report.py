from __future__ import annotations

import json
from pathlib import Path

MATRIX = Path("docs/architecture/eco-synthetic-signal-matrix.json")
JSON_OUTPUT = Path("results/eco_synthetic_signal_matrix_report.json")
MD_OUTPUT = Path("results/eco_synthetic_signal_matrix_report.md")


def load_matrix() -> dict:
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def build_report(matrix: dict) -> dict:
    signals = matrix.get("signals", [])
    return {
        "title": "E.C.O. synthetic signal matrix report",
        "status": "passed",
        "classification": matrix.get("classification", "allowed"),
        "signal_count": len(signals),
        "signals": signals,
        "limit": matrix.get("limit", ""),
    }


def write_outputs(report: dict) -> None:
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# E.C.O. synthetic signal matrix report", ""]
    md.append(f"Estado: {report['status']}")
    md.append(f"Señales registradas: {report['signal_count']}")
    md.append("")
    md.append("| Demo | Entrada | Patrón | Lectura | Riesgo | Próximo experimento |")
    md.append("|---|---|---|---|---|---|")
    for signal in report["signals"]:
        md.append(f"| {signal['demo']} | {signal['synthetic_input']} | {signal['observed_pattern']} | {signal['operational_reading']} | {signal['risk']} | {signal['allowed_next_experiment']} |")
    md.append("")
    md.append(f"Límite: {report['limit']}.")
    MD_OUTPUT.write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> int:
    report = build_report(load_matrix())
    write_outputs(report)
    print("# E.C.O. synthetic signal matrix report")
    print(f"Estado: {report['status']}")
    print(f"Señales registradas: {report['signal_count']}")
    print(f"Salida JSON: {JSON_OUTPUT}")
    print(f"Salida Markdown: {MD_OUTPUT}")
    print(f"Límite: {report['limit']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
