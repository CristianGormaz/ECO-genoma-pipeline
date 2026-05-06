from __future__ import annotations

import json
from pathlib import Path

RESULT_JSON = Path("results/eco_minimal_simulation_demo.json")
RESULT_MD = Path("results/eco_minimal_simulation_demo.md")

def step(state: dict, tick: int) -> dict:
    assimilation = min(state["nutrient"], 2 + tick % 2)
    nutrient = max(0, state["nutrient"] - assimilation)
    waste = state["waste"] + max(0, assimilation - 1)
    signal = max(0, state["signal"] + assimilation - (1 if waste > 3 else 0))
    stability = max(0, 10 - abs(signal - 5) - waste)
    action = "digest" if assimilation else "rest"
    return {
        "nutrient": nutrient,
        "signal": signal,
        "waste": waste,
        "stability": stability,
        "action": action,
    }

def run_simulation() -> dict:
    state = {"nutrient": 9, "signal": 1, "waste": 0}
    trace = []
    for tick in range(1, 6):
        state = step(state, tick)
        trace.append({"tick": tick, **state})
    return {
        "title": "E.C.O. minimal simulation demo",
        "scope": "synthetic educational behavior simulation",
        "trace": trace,
        "summary": {
            "ticks": len(trace),
            "final_state": trace[-1],
            "classification": "allowed",
            "data_policy": "synthetic_only",
            "training": False,
            "sensitive_data": False,
            "baseline_changed": False,
            "threshold_recalibrated": False,
        },
        "limits": [
            "No entrena modelos.",
            "No usa datos sensibles.",
            "No modifica baseline.",
            "No recalibra umbrales.",
            "No hace afirmaciones biomédicas aplicadas.",
        ],
    }

def write_results(result: dict) -> None:
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_lines = []
    md_lines.append("# E.C.O. minimal simulation demo")
    md_lines.append("")
    md_lines.append("Estado: experimental.")
    md_lines.append("Clasificación: permitido.")
    md_lines.append("")
    md_lines.append("## Resumen")
    md_lines.append("")
    md_lines.append("Simulación sintética mínima de ciclo E.C.O.: nutriente, señal, residuo y estabilidad.")
    md_lines.append("")
    md_lines.append("## Traza")
    md_lines.append("")
    md_lines.append("| tick | nutrient | signal | waste | stability | action |")
    md_lines.append("|---:|---:|---:|---:|---:|---|")
    for item in result["trace"]:
        md_lines.append("| " + str(item["tick"]) + " | " + str(item["nutrient"]) + " | " + str(item["signal"]) + " | " + str(item["waste"]) + " | " + str(item["stability"]) + " | " + item["action"] + " |")
    md_lines.append("")
    md_lines.append("## Límite responsable")
    md_lines.append("")
    md_lines.append("Esta demo usa solo datos sintéticos. No entrena modelos, no usa datos sensibles, no modifica baseline, no recalibra umbrales y no hace afirmaciones biomédicas aplicadas.")
    RESULT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

def main() -> int:
    result = run_simulation()
    write_results(result)
    print("# E.C.O. minimal simulation demo")
    print("Estado: experimental")
    print("Clasificación: permitido")
    print("Salida JSON: " + str(RESULT_JSON))
    print("Salida Markdown: " + str(RESULT_MD))
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin afirmaciones aplicadas.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
