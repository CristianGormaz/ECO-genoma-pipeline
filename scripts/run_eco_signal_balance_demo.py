from __future__ import annotations

import json
from pathlib import Path


RESULTS_DIR = Path("results")
JSON_PATH = RESULTS_DIR / "eco_signal_balance_demo.json"
MD_PATH = RESULTS_DIR / "eco_signal_balance_demo.md"


def build_trace() -> list[dict[str, int | str]]:
    return [
        {"tick": 1, "nutrient": 3, "signal": 2, "waste": 1, "stability": 5, "action": "digest"},
        {"tick": 2, "nutrient": 5, "signal": 3, "waste": 1, "stability": 6, "action": "digest"},
        {"tick": 3, "nutrient": 4, "signal": 5, "waste": 2, "stability": 7, "action": "digest"},
        {"tick": 4, "nutrient": 2, "signal": 6, "waste": 3, "stability": 5, "action": "digest"},
        {"tick": 5, "nutrient": 1, "signal": 4, "waste": 3, "stability": 4, "action": "rest"},
        {"tick": 6, "nutrient": 2, "signal": 3, "waste": 2, "stability": 6, "action": "rest"},
    ]


def build_payload() -> dict:
    trace = build_trace()
    return {
        "title": "E.C.O. signal balance simulation demo",
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


def write_markdown(payload: dict) -> str:
    lines = [
        "# E.C.O. signal balance simulation demo",
        "",
        "Estado: experimental.",
        "",
        "Clasificación: permitido.",
        "",
        "Esta demo usa datos sintéticos para observar una secuencia mínima de equilibrio entre nutriente, señal, residuo y estabilidad.",
        "",
        "No representa un sistema biológico real y no hace afirmaciones biomédicas aplicadas.",
        "",
        "## Resultado final",
        "",
        f"- Ticks: {payload['summary']['ticks']}",
        f"- Acción final: {payload['summary']['final_state']['action']}",
        f"- Estabilidad final: {payload['summary']['final_state']['stability']}",
        "",
        "## Límite responsable",
        "",
        "- Datos sintéticos.",
        "- Sin entrenamiento.",
        "- Sin datos sensibles.",
        "- Sin recalibración de umbrales.",
        "- Sin afirmaciones aplicadas.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    JSON_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MD_PATH.write_text(write_markdown(payload), encoding="utf-8")
    print("# E.C.O. signal balance simulation demo")
    print("Estado: experimental")
    print("Clasificación: permitido")
    print("Salida JSON: " + str(JSON_PATH))
    print("Salida Markdown: " + str(MD_PATH))
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin afirmaciones aplicadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
