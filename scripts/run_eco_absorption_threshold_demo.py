from __future__ import annotations

import json
from pathlib import Path


def clamp(value: int, low: int = 0, high: int = 10) -> int:
    return max(low, min(high, value))


def build_trace() -> list[dict[str, int | str]]:
    trace = []
    nutrient = 4
    capacity = 6
    events = [
        {"incoming": 2, "noise": 1},
        {"incoming": 7, "noise": 2},
        {"incoming": 9, "noise": 5},
        {"incoming": 4, "noise": 1},
        {"incoming": 8, "noise": 4},
    ]
    for tick, event in enumerate(events, start=1):
        incoming = event["incoming"]
        noise = event["noise"]
        absorbed = clamp(min(incoming, capacity) - noise // 2)
        waste = clamp(max(0, incoming - absorbed) + noise)
        nutrient = clamp(nutrient + absorbed - 3)
        stability = clamp(10 - waste + nutrient // 2)
        action = "digest" if absorbed >= 3 and stability >= 4 else "rest"
        trace.append({"tick": tick, "nutrient": nutrient, "signal": absorbed, "waste": waste, "stability": stability, "action": action})
    return trace


def main() -> int:
    results = Path("results")
    results.mkdir(parents=True, exist_ok=True)
    trace = build_trace()
    payload = {
        "title": "E.C.O. absorption threshold simulation demo",
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
    json_path = results / "eco_absorption_threshold_demo.json"
    md_path = results / "eco_absorption_threshold_demo.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# E.C.O. absorption threshold simulation demo", "", "Estado: experimental", "Clasificación: permitido", "", "## Trace"]
    for item in trace:
        lines.append("- tick {tick}: nutrient={nutrient}, signal={signal}, waste={waste}, stability={stability}, action={action}".format(**item))
    lines.extend(["", "## Límite", "Datos sintéticos; sin entrenamiento; sin datos sensibles; sin afirmaciones aplicadas."])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("# E.C.O. absorption threshold simulation demo")
    print("Estado: experimental")
    print("Clasificación: permitido")
    print("Salida JSON: " + str(json_path))
    print("Salida Markdown: " + str(md_path))
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin afirmaciones aplicadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
