#!/usr/bin/env python3
"""E.C.O. synthetic formula coherence audit.

Audita coherencia técnica interna de fórmulas, métricas sintéticas y reglas
operativas existentes sin introducir nuevas capacidades funcionales.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from scripts.run_eco_laos_agency_demo import build_scenarios as build_laos_agency_scenarios
from scripts.run_eco_laos_agency_demo import calculate_laos_score
from scripts.run_eco_laos_governance_gate_demo import build_scenarios as build_laos_gate_scenarios
from src.eco_core import DEFAULT_TRANSITION_PACKETS, EXTENDED_TRANSITION_PACKETS, EntericSystem, build_adaptive_state_rows
from src.eco_core.adaptive_state_baseline import project_homeostatic_state
from src.eco_core.adaptive_state_coverage import build_coverage_diagnostics
from src.eco_core.adaptive_state_dataset import build_adaptive_state_row
from src.eco_core.adaptive_state_evaluation import evaluate_state_transition_holdout
from src.eco_core.packet_trace import build_packet_trace

OUTPUT_JSON = Path("results/eco_formula_coherence_audit.json")
OUTPUT_MD = Path("results/eco_formula_coherence_audit.md")

CAPABILITIES_MAP = Path("docs/operations/eco-current-capabilities-map.md")
PANEL_INDEX = Path("docs/operations/eco-operational-panel-index.md")
REAL_DATA_READINESS_GATE = Path("docs/architecture/eco-real-data-readiness-gate.md")
LAOS_FORMULA_DOC = Path("docs/operations/eco-laos-agency-formula.md")

RESPONSIBLE_LIMITS = [
    "Sin datos reales.",
    "Sin entrenamiento.",
    "Sin modificación de baseline.",
    "Sin recalibración de umbrales.",
    "Sin diagnóstico.",
    "Sin interpretación clínica.",
    "Sin afirmaciones biomédicas aplicadas.",
    "Sin autonomía real.",
    "Sin conciencia.",
    "Sin libre albedrío real.",
]


@dataclass(frozen=True)
class InvariantResult:
    invariant_id: str
    area: str
    description: str
    passed: bool
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _evaluate_laos_score_range() -> InvariantResult:
    scenarios = build_laos_agency_scenarios() + build_laos_gate_scenarios()
    scores = [float(item["laos_score"]) for item in scenarios]
    passed = all(0.0 <= score <= 1.0 for score in scores)
    return InvariantResult(
        invariant_id="laos_score_range",
        area="formula",
        description="Los scores LAOS normalizados deben permanecer en [0, 1].",
        passed=passed,
        evidence={
            "scenario_count": len(scores),
            "min_score": min(scores) if scores else None,
            "max_score": max(scores) if scores else None,
        },
    )


def _evaluate_laos_risk_friction_monotonicity() -> InvariantResult:
    low_friction = {"O": 0.7, "M": 0.7, "P": 0.7, "V": 0.7, "K": 0.7, "R": 0.1, "I": 0.1, "N": 0.1, "A": 0.1}
    high_friction = {"O": 0.7, "M": 0.7, "P": 0.7, "V": 0.7, "K": 0.7, "R": 0.8, "I": 0.8, "N": 0.8, "A": 0.8}
    low_score = calculate_laos_score(low_friction)
    high_score = calculate_laos_score(high_friction)
    passed = high_score <= low_score
    return InvariantResult(
        invariant_id="laos_risk_friction_monotonicity",
        area="formula",
        description="Aumentar fricción/riesgo (R/I/N/A) no debe aumentar score LAOS.",
        passed=passed,
        evidence={
            "low_friction_score": round(low_score, 6),
            "high_friction_score": round(high_score, 6),
        },
    )


def _evaluate_laos_coherence_monotonicity() -> InvariantResult:
    low_coherence = {"O": 0.7, "M": 0.7, "P": 0.7, "V": 0.7, "K": 0.3, "R": 0.2, "I": 0.2, "N": 0.2, "A": 0.2}
    high_coherence = {"O": 0.7, "M": 0.7, "P": 0.7, "V": 0.7, "K": 0.9, "R": 0.2, "I": 0.2, "N": 0.2, "A": 0.2}
    low_score = calculate_laos_score(low_coherence)
    high_score = calculate_laos_score(high_coherence)
    passed = high_score >= low_score
    return InvariantResult(
        invariant_id="laos_coherence_signal_monotonicity",
        area="formula",
        description="Aumentar K (coherencia/validación) no debe reducir el score LAOS.",
        passed=passed,
        evidence={
            "low_coherence_score": round(low_score, 6),
            "high_coherence_score": round(high_score, 6),
        },
    )


def _evaluate_reject_quarantine_not_absorption_projection() -> InvariantResult:
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    targets = [row for row in rows if row.final_decision in {"reject", "quarantine"}]
    projected = {row.source: project_homeostatic_state(row) for row in targets}
    passed = bool(targets) and all(state != "stable" for state in projected.values())
    return InvariantResult(
        invariant_id="reject_quarantine_not_absorption_projection",
        area="adaptive_state",
        description="Decisiones reject/quarantine no deben proyectarse como absorción estable.",
        passed=passed,
        evidence={
            "target_rows": len(targets),
            "projected_states": projected,
        },
    )


def _evaluate_batch_absorb_as_valid_absorption() -> InvariantResult:
    system = EntericSystem(heavy_payload_threshold=1)
    before = system.homeostasis_snapshot()
    packet = system.process_dna_sequence("ACGTCCAATGGTATAAA", source="heavy_batch_case")
    after = system.homeostasis_snapshot()
    row = build_adaptive_state_row(trace=build_packet_trace(packet), before=before, after=after)
    projected = project_homeostatic_state(row)
    passed = row.final_decision == "batch_absorb" and projected == "stable"
    return InvariantResult(
        invariant_id="batch_absorb_is_absorption",
        area="adaptive_state",
        description="batch_absorb debe tratarse como absorción válida en la proyección adaptativa.",
        passed=passed,
        evidence={
            "final_decision": row.final_decision,
            "projected_state": projected,
            "observed_state": row.state_after,
        },
    )


def _evaluate_fallback_reporting_consistency() -> InvariantResult:
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)
    expected = sum(
        item.matched_rule in {"default_state", "homeostasis_projection"}
        for item in evaluation.predictions
    )
    diagnostics = build_coverage_diagnostics(rows, evaluation=evaluation)
    passed = diagnostics.fallback_predictions == expected
    return InvariantResult(
        invariant_id="fallback_effective_is_reported",
        area="adaptive_state",
        description="El fallback efectivo debe contabilizarse como fallback en cobertura.",
        passed=passed,
        evidence={
            "expected_fallback_predictions": expected,
            "reported_fallback_predictions": diagnostics.fallback_predictions,
            "prediction_count": len(evaluation.predictions),
        },
    )


def _evaluate_public_guard_boundary() -> InvariantResult:
    capabilities = CAPABILITIES_MAP.read_text(encoding="utf-8")
    panel = PANEL_INDEX.read_text(encoding="utf-8")
    required = [
        "public-source-url-admission-guard",
        "no equivale a `real-biological-data-admission-gate`",
        "no autoriza procesamiento de datos reales",
        "no habilita entrenamiento",
        "no modifica baseline",
        "no recalibra umbrales",
    ]
    missing_capabilities = [item for item in required if item not in capabilities.lower()]
    missing_panel = [item for item in required if item not in panel.lower()]
    passed = not missing_capabilities and not missing_panel
    return InvariantResult(
        invariant_id="public_guard_not_real_data_authorization",
        area="governance",
        description="public-source-url-admission-guard no debe declararse como admisión de datos reales.",
        passed=passed,
        evidence={
            "missing_in_capabilities_map": missing_capabilities,
            "missing_in_operational_panel_index": missing_panel,
        },
    )


def _evaluate_responsible_limits_presence() -> InvariantResult:
    text = "\n".join(
        [
            LAOS_FORMULA_DOC.read_text(encoding="utf-8").lower(),
            REAL_DATA_READINESS_GATE.read_text(encoding="utf-8").lower(),
            CAPABILITIES_MAP.read_text(encoding="utf-8").lower(),
        ]
    )
    required = [
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin diagnóstico",
        "sin interpretación clínica",
        "sin afirmaciones biomédicas aplicadas",
        "sin conciencia",
        "sin libre albedrío real",
    ]
    missing = [item for item in required if item not in text]
    passed = not missing
    return InvariantResult(
        invariant_id="responsible_limits_are_explicit",
        area="governance",
        description="Los límites responsables deben permanecer explícitos en piezas operativas clave.",
        passed=passed,
        evidence={"missing_limit_tokens": missing},
    )


def evaluate_invariants() -> list[InvariantResult]:
    return [
        _evaluate_laos_score_range(),
        _evaluate_laos_risk_friction_monotonicity(),
        _evaluate_laos_coherence_monotonicity(),
        _evaluate_reject_quarantine_not_absorption_projection(),
        _evaluate_batch_absorb_as_valid_absorption(),
        _evaluate_fallback_reporting_consistency(),
        _evaluate_public_guard_boundary(),
        _evaluate_responsible_limits_presence(),
    ]


def build_report() -> dict[str, Any]:
    invariants = evaluate_invariants()
    failed = [item.invariant_id for item in invariants if not item.passed]
    status = "passed" if not failed else "attention"
    return {
        "title": "E.C.O. formula coherence audit",
        "status": status,
        "classification": "allowed" if status == "passed" else "attention_required",
        "scope": {
            "kind": "technical_coherence_synthetic_audit",
            "scientific_claims": "not_evaluated",
            "biomedical_claims": "not_applicable",
            "statement": (
                "Esta auditoría evalúa coherencia técnica interna de reglas y fórmulas; "
                "no valida afirmaciones científicas ni biomédicas aplicadas."
            ),
        },
        "invariants_evaluated": len(invariants),
        "invariants_passed": sum(item.passed for item in invariants),
        "invariants_failed": len(failed),
        "failed_invariant_ids": failed,
        "invariants": [item.to_dict() for item in invariants],
        "responsible_limits": RESPONSIBLE_LIMITS,
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# E.C.O. formula coherence audit",
        "",
        f"Estado: `{report['status']}`",
        f"Clasificación: `{report['classification']}`",
        "",
        "## Alcance",
        "",
        f"- tipo: `{report['scope']['kind']}`",
        f"- scientific_claims: `{report['scope']['scientific_claims']}`",
        f"- biomedical_claims: `{report['scope']['biomedical_claims']}`",
        f"- nota: {report['scope']['statement']}",
        "",
        "## Invariantes evaluadas",
        "",
        f"- total: `{report['invariants_evaluated']}`",
        f"- passed: `{report['invariants_passed']}`",
        f"- failed: `{report['invariants_failed']}`",
        "",
        "| Invariante | Área | Estado | Evidencia |",
        "|---|---|---|---|",
    ]

    for item in report["invariants"]:
        lines.append(
            f"| `{item['invariant_id']}` | `{item['area']}` | "
            f"`{'passed' if item['passed'] else 'attention'}` | `{item['evidence']}` |"
        )

    lines.extend(["", "## Límite responsable", ""])
    lines.extend(f"- {item}" for item in report["responsible_limits"])
    lines.append("")
    return "\n".join(lines)


def write_outputs(report: dict[str, Any]) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")


def main() -> int:
    report = build_report()
    write_outputs(report)
    print("# E.C.O. formula coherence audit")
    print(f"Estado: {report['status']}")
    print(f"Invariantes evaluadas: {report['invariants_evaluated']}")
    print(f"Invariantes fallidas: {report['invariants_failed']}")
    print(f"Salida JSON: {OUTPUT_JSON}")
    print(f"Salida Markdown: {OUTPUT_MD}")
    print("Límite: coherencia técnica interna, sin afirmaciones científicas o biomédicas aplicadas.")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
