#!/usr/bin/env python3
"""E.C.O. LAOS governance gate synthetic demo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RESULTS_DIR = Path("results")
OUTPUT_JSON = RESULTS_DIR / "eco_laos_governance_gate_demo.json"
OUTPUT_MD = RESULTS_DIR / "eco_laos_governance_gate_demo.md"

RESPONSIBLE_LIMITS = (
    "Sin libre albedrio real.",
    "Sin conciencia.",
    "Sin autonomia real.",
    "Sin datos reales.",
    "Sin entrenamiento.",
    "Sin modificacion de baseline.",
    "Sin recalibracion de umbrales.",
    "Sin afirmaciones biomedicas aplicadas.",
)


def calculate_laos_score(variables: dict[str, float]) -> float:
    numerator = variables["O"] * variables["M"] * variables["P"] * variables["V"] * variables["K"]
    denominator = 1 + variables["R"] + variables["I"] + variables["N"] + variables["A"]
    raw = numerator / denominator
    return raw / (1 + raw)


def recommend(score: float, validation_state: str) -> str:
    if validation_state == "failed" or score < 0.33:
        return "pausar"
    if validation_state == "attention" or score < 0.66:
        return "revision humana"
    return "avanzar con control"


def build_scenarios() -> list[dict[str, Any]]:
    synthetic_inputs: list[dict[str, Any]] = [
        {
            "id": "low_agency_validation_failed",
            "name": "Baja agencia simulada con validacion fallida",
            "validation_state": "failed",
            "variables": {"O": 0.30, "M": 0.35, "P": 0.32, "V": 0.38, "K": 0.42, "R": 0.82, "I": 0.70, "N": 0.74, "A": 0.68},
            "control_signal": "La trazabilidad sintetica no alcanza el minimo documental.",
        },
        {
            "id": "medium_agency_validation_attention",
            "name": "Agencia simulada intermedia con validacion en atencion",
            "validation_state": "attention",
            "variables": {"O": 1.60, "M": 1.50, "P": 1.40, "V": 1.45, "K": 1.55, "R": 0.45, "I": 0.40, "N": 0.34, "A": 0.32},
            "control_signal": "El cambio puede continuar solo con revision humana.",
        },
        {
            "id": "high_agency_validation_passed",
            "name": "Alta agencia simulada con validacion aprobada",
            "validation_state": "passed",
            "variables": {"O": 2.60, "M": 2.40, "P": 2.20, "V": 2.30, "K": 2.50, "R": 0.20, "I": 0.16, "N": 0.12, "A": 0.10},
            "control_signal": "El avance sigue siendo controlado, trazable y reversible.",
        },
    ]

    scenarios: list[dict[str, Any]] = []
    for item in synthetic_inputs:
        score = calculate_laos_score(item["variables"])
        scenarios.append(
            {
                "id": item["id"],
                "name": item["name"],
                "validation_state": item["validation_state"],
                "laos_score": round(score, 6),
                "recommendation": recommend(score, item["validation_state"]),
                "control_signal": item["control_signal"],
                "variables": item["variables"],
            }
        )
    return scenarios


def build_report() -> dict[str, Any]:
    scenarios = build_scenarios()
    return {
        "title": "E.C.O. LAOS Governance Gate Demo",
        "status": "passed",
        "classification": "permitido",
        "scope": "documental_sintetico",
        "gate": {
            "purpose": "Cruzar score LAOS con estado de validacion sintetico.",
            "allowed_recommendations": ["pausar", "revision humana", "avanzar con control"],
            "autonomy_activation": False,
        },
        "declaration": {
            "no_real_free_will": True,
            "no_consciousness": True,
            "no_real_data": True,
            "no_training": True,
            "no_baseline_change": True,
            "no_threshold_recalibration": True,
        },
        "responsible_limits": list(RESPONSIBLE_LIMITS),
        "scenarios": scenarios,
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# E.C.O. LAOS Governance Gate Demo",
        "",
        "## Estado",
        f"- status: {report['status']}",
        f"- classification: {report['classification']}",
        f"- scope: {report['scope']}",
        "- autonomia real activada: no",
        "",
        "## Compuerta",
        "- Cruza score LAOS con estado de validacion sintetico.",
        "- Recomendaciones posibles: pausar, revision humana, avanzar con control.",
        "- No ejecuta acciones autonomas.",
        "",
        "## Limites responsables",
    ]
    lines.extend(f"- {limit}" for limit in report["responsible_limits"])
    lines.extend(["", "## Escenarios sinteticos"])

    for scenario in report["scenarios"]:
        lines.extend(
            [
                "",
                f"### {scenario['name']}",
                f"- id: {scenario['id']}",
                f"- estado de validacion: {scenario['validation_state']}",
                f"- score LAOS: {scenario['laos_score']}",
                f"- recomendacion: {scenario['recommendation']}",
                f"- senal de control: {scenario['control_signal']}",
            ]
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")
    print(f"OK: LAOS governance gate demo generado: {OUTPUT_JSON} {OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
