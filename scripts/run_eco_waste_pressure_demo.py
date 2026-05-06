from __future__ import annotations

import json
from pathlib import Path


def clamp(value: int, low: int = 0, high: int = 10) -> int:
    return max(low, min(high, value))


def build_trace() -> list[dict[str, int | str]]:
    trace = []
    nutrient = 5
    events = [
        {"signal": 3, "waste": 1, "intake": 4},
        {"signal": 5, "waste": 3, "intake": 3},
        {"signal": 7, "waste": 6, "intake": 2},
        {"signal": 6, "waste": 8, "intake": 1},
        {"signal": 4, "waste": 5, "intake": 2},
    ]
    for tick, event in enumerate(events, start=1):
        nutrient = clamp(nutrient + event["intake"] - 3)
        signal = event["signal"]
        waste = event["waste"]
        stability = clamp(10 - waste + nutrient // 3)
        action = "digest" if nutrient > waste and stability >= 4 else "rest"
        trace.append({"tick": tick, "nutrient": nutrient, "signal": signal, "waste": waste, "stability": stability, "action": action})
    return trace


def main() -> int:
    results = Path("results")
    results.mkdir(parents=True, exist_ok=True)
    trace = build_trace()
    payload = {
        "title": "E.C.O. waste pressure simulation demo",
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
    json_path = results / "eco_waste_pressure_demo.json"
    md_path = results / "eco_waste_pressure_demo.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# E.C.O. waste pressure simulation demo", "", "Estado: experimental", "Clasificación: permitido", "", "## Trace"]
    for item in trace:
        lines.append("- tick {tick}: nutrient={nutrient}, signal={signal}, waste={waste}, stability={stability}, action={action}".format(**item))
    lines.extend(["", "## Límite", "Datos sintéticos; sin entrenamiento; sin datos sensibles; sin afirmaciones aplicadas."])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("# E.C.O. waste pressure simulation demo")
    print("Estado: experimental")
    print("Clasificación: permitido")
    print("Salida JSON: " + str(json_path))
    print("Salida Markdown: " + str(md_path))
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin afirmaciones aplicadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
