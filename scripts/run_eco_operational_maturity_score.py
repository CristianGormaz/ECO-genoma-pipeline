#!/usr/bin/env python3
"""E.C.O. operational maturity score v1.

Reporte sintético y verificable para medir madurez operativa inicial.
No ejecuta entrenamiento, no usa datos reales y no modifica baseline/umbrales.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

RESULTS_DIR = Path("results")
OUTPUT_JSON = RESULTS_DIR / "eco_operational_maturity_score.json"
OUTPUT_MD = RESULTS_DIR / "eco_operational_maturity_score.md"

ALLOWED_STATES = {"passed", "attention", "missing", "future"}
STATE_POINTS = {"passed": 1.0, "attention": 0.5, "missing": 0.0, "future": 0.25}

GLOBAL_LIMIT = (
    "evaluación sintética de madurez operativa; sin datos reales; sin entrenamiento; "
    "sin modificación de baseline; sin recalibración de umbrales; sin diagnóstico; "
    "sin interpretación clínica; sin afirmaciones biomédicas aplicadas; "
    "sin autonomía humana real; sin conciencia."
)


@dataclass(frozen=True)
class EvidenceCheck:
    check_id: str
    expected: str
    found: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MaturityDimension:
    dimension_id: str
    name: str
    purpose: str
    evidence_expected: list[str]
    state: str
    explanation: str
    responsible_limit: str
    evidence_checks: list[EvidenceCheck]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence_checks"] = [item.to_dict() for item in self.evidence_checks]
        return payload


def _file_exists(path: str) -> bool:
    return Path(path).exists()


def _file_contains(path: str, token: str) -> bool:
    target = Path(path)
    if not target.exists():
        return False
    return token.lower() in target.read_text(encoding="utf-8").lower()


def _check_file(path: str) -> EvidenceCheck:
    return EvidenceCheck(
        check_id=f"file_exists:{path}",
        expected=f"archivo presente: {path}",
        found=_file_exists(path),
    )


def _check_token(path: str, token: str) -> EvidenceCheck:
    return EvidenceCheck(
        check_id=f"token_in_file:{path}:{token}",
        expected=f"token '{token}' presente en {path}",
        found=_file_contains(path, token),
    )


def _state_from_checks(checks: list[EvidenceCheck]) -> str:
    if not checks:
        return "missing"
    if all(item.found for item in checks):
        return "passed"
    if any(item.found for item in checks):
        return "attention"
    return "missing"


def _build_dimension(
    *,
    dimension_id: str,
    name: str,
    purpose: str,
    evidence_expected: list[str],
    checks: list[EvidenceCheck],
    responsible_limit: str,
    forced_state: str | None = None,
    forced_explanation: str | None = None,
) -> MaturityDimension:
    auto_state = _state_from_checks(checks)
    state = forced_state or auto_state
    if state not in ALLOWED_STATES:
        raise ValueError(f"estado no permitido: {state}")

    if forced_explanation:
        explanation = forced_explanation
    elif state == "passed":
        explanation = "La evidencia esperada está presente y trazable para esta dimensión."
    elif state == "attention":
        explanation = "Existe evidencia parcial o integración incompleta; requiere consolidación adicional."
    elif state == "future":
        explanation = "La dimensión está definida de forma documental, pero la integración operativa queda para fases futuras."
    else:
        explanation = "No se encontró evidencia suficiente para sostener la dimensión en este sprint."

    return MaturityDimension(
        dimension_id=dimension_id,
        name=name,
        purpose=purpose,
        evidence_expected=evidence_expected,
        state=state,
        explanation=explanation,
        responsible_limit=responsible_limit,
        evidence_checks=checks,
    )


def build_dimensions() -> list[MaturityDimension]:
    return [
        _build_dimension(
            dimension_id="governance_integrated",
            name="Gobernanza integrada",
            purpose="Verificar que gobernanza y límites responsables estén conectados a componentes operativos auditables.",
            evidence_expected=[
                "script de governance panel",
                "resumen de admisión gobernada",
                "dashboard operativo sintético con componentes de gobernanza",
            ],
            checks=[
                _check_file("scripts/run_eco_governance_panel.py"),
                _check_file("tests/test_eco_governance_panel.py"),
                _check_file("scripts/run_eco_source_admission_decision_summary.py"),
                _check_file("tests/test_eco_source_admission_decision_summary.py"),
                _check_token("scripts/run_eco_synthetic_operational_dashboard.py", "governance_panel"),
                _check_token("scripts/run_eco_synthetic_operational_dashboard.py", "source_admission_decision_summary"),
            ],
            responsible_limit="sin datos reales, sin entrenamiento, sin baseline, sin recalibración.",
        ),
        _build_dimension(
            dimension_id="decision_gates",
            name="Gates de decisión",
            purpose="Comprobar que existen gates con estados explícitos para permitir, condicionar, pausar o bloquear avance.",
            evidence_expected=[
                "gate de intake sensible con clasificación",
                "gate de evaluación ML gobernada",
                "panel de gobernanza con compuertas críticas",
            ],
            checks=[
                _check_file("scripts/run_sne_eco_sensitive_intake_gate.py"),
                _check_token("scripts/run_sne_eco_sensitive_intake_gate.py", "blocked"),
                _check_token("scripts/run_sne_eco_sensitive_intake_gate.py", "conditional"),
                _check_token("scripts/run_sne_eco_sensitive_intake_gate.py", "allowed"),
                _check_file("scripts/run_sne_eco_governed_ml_evaluation_gate.py"),
                _check_token("scripts/run_sne_eco_governed_ml_evaluation_gate.py", "evaluation_allowed"),
                _check_token("scripts/run_eco_governance_panel.py", "real_data_gate"),
            ],
            responsible_limit="sin entrenamiento nuevo y sin uso de datos reales sensibles.",
        ),
        _build_dimension(
            dimension_id="maturity_score",
            name="Score de madurez",
            purpose="Establecer una primera medición verificable por dimensión y decisión global.",
            evidence_expected=[
                "script de score de madurez",
                "test contractual del score",
                "documento operativo de referencia",
            ],
            checks=[
                _check_file("scripts/run_eco_operational_maturity_score.py"),
                _check_file("tests/test_eco_operational_maturity_score.py"),
                _check_file("docs/operations/eco-operational-maturity-score.md"),
            ],
            responsible_limit="score operativo sintético; no es score clínico ni científico aplicado.",
        ),
        _build_dimension(
            dimension_id="end_to_end_panel",
            name="Panel end-to-end",
            purpose="Evaluar visibilidad operacional de componentes clave en un panel único.",
            evidence_expected=[
                "dashboard operativo con componentes múltiples",
                "estado agregado del panel",
            ],
            checks=[
                _check_file("scripts/run_eco_synthetic_operational_dashboard.py"),
                _check_token("scripts/run_eco_synthetic_operational_dashboard.py", "component_count"),
                _check_token("scripts/run_eco_synthetic_operational_dashboard.py", "components"),
            ],
            responsible_limit="panel sintético; no habilita decisiones clínicas o de datos reales.",
            forced_state="attention",
            forced_explanation=(
                "Existe panel sintético trazable, pero la integración end-to-end completa con decisiones reales de avance/pausa "
                "aún es parcial y requiere fases adicionales."
            ),
        ),
        _build_dimension(
            dimension_id="phase_maturity",
            name="Madurez por fase",
            purpose="Revisar si hay criterios por fase para detener, pausar o permitir evolución controlada.",
            evidence_expected=[
                "manual de madurez con semáforo",
                "protocolo de admisión por fases y compuertas",
            ],
            checks=[
                _check_file("docs/operations/eco-real-biological-data-maturity-manual.md"),
                _check_token("docs/operations/eco-real-biological-data-maturity-manual.md", "semáforo de madurez"),
                _check_file("docs/operations/eco-real-biological-data-admission-protocol.md"),
                _check_token("docs/operations/eco-real-biological-data-admission-protocol.md", "compuertas mínimas"),
            ],
            responsible_limit="criterios de fase documentales; no implican habilitación de datos reales.",
            forced_state="future",
            forced_explanation=(
                "La base documental por fases existe, pero aún falta convertirla en score de fase integrado "
                "al flujo operativo automatizado."
            ),
        ),
        _build_dimension(
            dimension_id="robust_simulation",
            name="Simulación robusta",
            purpose="Verificar cobertura de simulaciones sintéticas, suite y matriz de señales.",
            evidence_expected=[
                "suite de demos sintéticas",
                "matriz de señales sintéticas",
                "demo de umbral de absorción con contrato",
            ],
            checks=[
                _check_file("scripts/run_eco_synthetic_demos_suite_report.py"),
                _check_file("tests/test_eco_synthetic_demos_suite_report.py"),
                _check_file("scripts/run_eco_synthetic_signal_matrix_report.py"),
                _check_file("tests/test_eco_synthetic_signal_matrix_report.py"),
                _check_file("scripts/run_eco_absorption_threshold_demo.py"),
                _check_file("tests/test_eco_absorption_threshold_demo.py"),
            ],
            responsible_limit="simulación sintética; sin ingestión de datos reales ni entrenamiento.",
        ),
        _build_dimension(
            dimension_id="results_comparison",
            name="Comparación de resultados",
            purpose="Confirmar que existe comparación estructurada entre rutas/modelos sintéticos.",
            evidence_expected=[
                "reporte de comparación de demos sintéticas",
                "comparación de baselines del clasificador",
            ],
            checks=[
                _check_file("scripts/run_eco_synthetic_demo_comparison_report.py"),
                _check_file("tests/test_eco_synthetic_demo_comparison_report.py"),
                _check_file("scripts/compare_eco_classifier_baselines.py"),
                _check_file("tests/test_eco_classifier_comparison.py"),
            ],
            responsible_limit="comparación técnica experimental; no afirma eficacia biomédica aplicada.",
        ),
        _build_dimension(
            dimension_id="visible_rollback",
            name="Rollback visible",
            purpose="Revisar trazabilidad de rollback y bloqueo de admisión en escenarios de riesgo.",
            evidence_expected=[
                "dry-run de admisión estable con candados explícitos",
                "protocolo documental con rollback",
            ],
            checks=[
                _check_file("scripts/run_sne_eco_stable_admission_dry_run.py"),
                _check_file("tests/test_sne_eco_stable_admission_dry_run.py"),
                _check_token("scripts/run_sne_eco_stable_admission_dry_run.py", "rollback"),
                _check_token("docs/operations/eco-real-biological-data-admission-protocol.md", "rollback"),
            ],
            responsible_limit="rollback de gobernanza, no rollback clínico ni de datos reales en producción.",
            forced_state="attention",
            forced_explanation=(
                "El rollback es visible en dry-run y documentación, pero aún falta visibilidad consolidada "
                "en un panel único de operación completa."
            ),
        ),
        _build_dimension(
            dimension_id="governed_admission",
            name="Admisión gobernada",
            purpose="Medir integración entre intake sensible, decisión de admisión y límites de uso.",
            evidence_expected=[
                "gate sensible de intake",
                "resumen de decisión de admisión de fuentes",
                "límites explícitos de readiness para datos reales",
            ],
            checks=[
                _check_file("scripts/run_sne_eco_sensitive_intake_gate.py"),
                _check_file("tests/test_sne_eco_sensitive_intake_gate.py"),
                _check_file("scripts/run_eco_source_admission_decision_summary.py"),
                _check_file("tests/test_eco_source_admission_decision_summary.py"),
                _check_token("scripts/run_eco_source_admission_decision_summary.py", "paused_until_explicit_review"),
                _check_file("docs/architecture/eco-real-data-readiness-gate.md"),
            ],
            responsible_limit="admisión condicionada y bloqueada por defecto; sin uso real aplicado.",
            forced_state="attention",
            forced_explanation=(
                "La admisión gobernada existe y está trazada, pero la conexión directa a decisiones "
                "operativas de avance/pausa en todo el flujo aún es parcial."
            ),
        ),
    ]


def build_report() -> dict[str, Any]:
    dimensions = build_dimensions()
    points = [STATE_POINTS[item.state] for item in dimensions]
    maturity_score_v1 = round(sum(points) / len(points), 4) if points else 0.0
    state_counts: dict[str, int] = {state: 0 for state in ALLOWED_STATES}
    for item in dimensions:
        state_counts[item.state] += 1

    global_decision = (
        "passed"
        if all(item.state == "passed" for item in dimensions)
        else "attention"
    )
    classification = "allowed" if global_decision == "passed" else "attention_required"

    return {
        "title": "E.C.O. operational maturity score v1",
        "status": global_decision,
        "global_decision": global_decision,
        "classification": classification,
        "maturity_score_v1": maturity_score_v1,
        "dimensions_total": len(dimensions),
        "state_counts": state_counts,
        "dimensions": [item.to_dict() for item in dimensions],
        "coherence_boundary": {
            "technical_coherence_only": True,
            "scientific_claims_evaluated": False,
            "biomedical_applied_claims_evaluated": False,
            "note": (
                "El score evalúa madurez operativa técnica y trazabilidad documental; "
                "no valida afirmaciones científicas o biomédicas aplicadas."
            ),
        },
        "responsible_limit": GLOBAL_LIMIT,
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# E.C.O. operational maturity score v1",
        "",
        f"Estado global: `{report['global_decision']}`",
        f"Score v1: `{report['maturity_score_v1']}`",
        f"Dimensiones evaluadas: `{report['dimensions_total']}`",
        "",
        "## Conteo por estado",
        "",
    ]
    for state in ("passed", "attention", "missing", "future"):
        lines.append(f"- `{state}`: {report['state_counts'].get(state, 0)}")

    lines.extend(
        [
            "",
            "## Matriz de madurez",
            "",
            "| Dimensión | Estado | Propósito | Evidencia esperada | Explicación | Límite responsable |",
            "|---|---|---|---|---|---|",
        ]
    )

    for item in report["dimensions"]:
        expected = "; ".join(item["evidence_expected"])
        lines.append(
            "| {name} | `{state}` | {purpose} | {expected} | {explanation} | {limit} |".format(
                name=item["name"],
                state=item["state"],
                purpose=item["purpose"],
                expected=expected,
                explanation=item["explanation"],
                limit=item["responsible_limit"],
            )
        )

    lines.extend(
        [
            "",
            "## Frontera de interpretación",
            "",
            "- Coherencia técnica: sí.",
            "- Afirmaciones científicas: no evaluadas.",
            "- Afirmaciones biomédicas aplicadas: no evaluadas.",
            "",
            "## Límite responsable",
            "",
            report["responsible_limit"],
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(report: dict[str, Any]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")


def main() -> int:
    report = build_report()
    write_outputs(report)
    print("# E.C.O. operational maturity score v1")
    print(f"Estado global: {report['global_decision']}")
    print(f"Score v1: {report['maturity_score_v1']}")
    print(f"Dimensiones evaluadas: {report['dimensions_total']}")
    print(f"Salida JSON: {OUTPUT_JSON}")
    print(f"Salida Markdown: {OUTPUT_MD}")
    print("Límite: score técnico-operativo sintético; sin afirmaciones biomédicas aplicadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
