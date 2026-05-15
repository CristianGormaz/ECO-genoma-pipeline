#!/usr/bin/env python3
"""E.C.O. LAOS synthetic agency demo.

Genera un reporte sintético y determinista sobre la métrica LAOS
(Libre Albedrío Operativo Simulado) para escenarios de agencia simulada.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

RESULTS_DIR = Path("results")
OUTPUT_JSON = RESULTS_DIR / "eco_laos_agency_demo.json"
OUTPUT_MD = RESULTS_DIR / "eco_laos_agency_demo.md"


def calculate_laos_score(variables: Dict[str, float]) -> float:
    """Calcula LAOS en rango seguro [0, 1).

    LAOS(t) = sigma((O*M*P*V*K) / (1+R+I+N+A))
    con sigma(x) = x / (1 + x).
    """

    numerator = (
        variables["O"]
        * variables["M"]
        * variables["P"]
        * variables["V"]
        * variables["K"]
    )
    denominator = 1 + variables["R"] + variables["I"] + variables["N"] + variables["A"]
    raw = numerator / denominator
    return raw / (1 + raw)


def interpret_score(score: float) -> Dict[str, str]:
    """Interpreta score y recomienda acción operativa."""

    if score < 0.33:
        return {
            "interpretation": "Baja agencia simulada: predominan restricciones, ruido o automatismo.",
            "recommendation": "pausar",
        }
    if score < 0.66:
        return {
            "interpretation": "Agencia simulada media: hay margen operativo, pero requiere supervisión.",
            "recommendation": "revisión humana",
        }
    return {
        "interpretation": "Alta agencia simulada: condiciones sintéticas favorables con control operativo.",
        "recommendation": "avanzar con control",
    }


def build_scenarios() -> List[Dict[str, Any]]:
    """Escenarios sintéticos deterministas para LAOS."""

    base_scenarios = [
        {
            "name": "baja agencia simulada",
            "variables": {"O": 0.25, "M": 0.35, "P": 0.30, "V": 0.40, "K": 0.45, "R": 0.80, "I": 0.70, "N": 0.75, "A": 0.65},
        },
        {
            "name": "agencia simulada media",
            "variables": {"O": 0.58, "M": 0.60, "P": 0.55, "V": 0.62, "K": 0.64, "R": 0.40, "I": 0.35, "N": 0.32, "A": 0.30},
        },
        {
            "name": "agencia simulada alta",
            "variables": {"O": 0.88, "M": 0.85, "P": 0.82, "V": 0.90, "K": 0.92, "R": 0.18, "I": 0.14, "N": 0.12, "A": 0.10},
        },
    ]

    scenarios: List[Dict[str, Any]] = []
    for scenario in base_scenarios:
        score = calculate_laos_score(scenario["variables"])
        qualitative = interpret_score(score)
        scenarios.append(
            {
                "name": scenario["name"],
                "variables": scenario["variables"],
                "laos_score": round(score, 6),
                "interpretation": qualitative["interpretation"],
                "recommendation": qualitative["recommendation"],
            }
        )
    return scenarios


def build_report() -> Dict[str, Any]:
    scenarios = build_scenarios()
    return {
        "title": "E.C.O. LAOS Synthetic Agency Demo",
        "metric": "LAOS (Libre Albedrío Operativo Simulado)",
        "status": "passed",
        "classification": "permitido",
        "declaration": {
            "agency_scope": "LAOS representa agencia simulada, no libre albedrío real ni conciencia.",
            "no_free_will_claim": "no libre albedrío real",
            "no_consciousness_claim": "no conciencia",
            "no_human_autonomy_claim": "no autonomía humana",
            "no_real_data": "sin datos reales",
            "no_training": "sin entrenamiento",
            "no_baseline_modification": "sin modificación de baseline",
            "no_threshold_recalibration": "sin recalibración de umbrales",
            "no_biomedical_applied_claims": "sin afirmaciones biomédicas aplicadas",
        },
        "responsible_limits": [
            "LAOS se usa como métrica experimental de agencia simulada.",
            "No libre albedrío real.",
            "No conciencia.",
            "Sin datos reales.",
            "Sin entrenamiento.",
            "Sin modificación de baseline.",
            "Sin recalibración de umbrales.",
            "Sin afirmaciones biomédicas aplicadas.",
        ],
        "scenarios": scenarios,
    }


def to_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# E.C.O. LAOS Synthetic Agency Demo",
        "",
        "## Estado",
        f"- status: {report['status']}",
        f"- classification: {report['classification']}",
        "",
        "## Marco de límites responsables",
        "- LAOS como agencia simulada.",
        "- No libre albedrío real.",
        "- No conciencia.",
        "- No autonomía humana.",
        "- Sin datos reales.",
        "- Sin entrenamiento.",
        "- Sin modificación de baseline.",
        "- Sin recalibración de umbrales.",
        "- Sin afirmaciones biomédicas aplicadas.",
        "",
        "## Escenarios sintéticos",
    ]

    for scenario in report["scenarios"]:
        lines.extend(
            [
                "",
                f"### {scenario['name']}",
                f"- score LAOS: {scenario['laos_score']}",
                f"- interpretación: {scenario['interpretation']}",
                f"- recomendación operativa: {scenario['recommendation']}",
                "- variables:",
            ]
        )
        for key, value in scenario["variables"].items():
            lines.append(f"  - {key}: {value}")

    return "\n".join(lines) + "\n"


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()

    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    print(f"[ok] JSON generado: {OUTPUT_JSON}")
    print(f"[ok] Markdown generado: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
