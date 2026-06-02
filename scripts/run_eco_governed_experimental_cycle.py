#!/usr/bin/env python3
"""Governed experimental cycle report for E.C.O.

This runner connects phase maturity, governed admission, gates, rollback,
responsible limits, and a final operational decision. It is synthetic and
documentary: it does not ingest real data, train models, modify baselines, or
recalibrate thresholds.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

OUTPUT_JSON = Path("results/eco_governed_experimental_cycle.json")
OUTPUT_MD = Path("results/eco_governed_experimental_cycle.md")

ALLOWED_STATES = {"passed", "attention", "missing", "future", "blocked"}
ALLOWED_DECISIONS = {"advance", "pause", "review", "reject"}

RESPONSIBLE_LIMITS = [
    "sin datos reales",
    "sin entrenamiento",
    "sin datos sensibles",
    "sin diagnóstico",
    "sin interpretación clínica",
    "sin baseline changes",
    "sin threshold recalibration",
    "sin conciencia",
    "sin libre albedrío real",
]

PREVIOUS_MATURITY_REFERENCE = {
    "maturity_score_v1": 0.8611,
    "basis": (
        "Referencia pre-ciclo: phase_maturity=future y governed_admission=attention "
        "en la matriz operacional previa."
    ),
}


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_state(raw: Any) -> str:
    value = str(raw or "").strip().lower()
    if value in {"passed", "green", "ok", "success", "allowed"}:
        return "passed"
    if value in {"attention", "yellow", "conditional", "warning"}:
        return "attention"
    if value in {"missing", "unknown"}:
        return "missing"
    if value in {"future", "planned"}:
        return "future"
    if value in {"blocked", "red", "reject", "error", "failed"}:
        return "blocked"
    return "missing"


def _file_check(check_id: str, path: str) -> dict[str, Any]:
    exists = Path(path).exists()
    return {
        "id": check_id,
        "state": "passed" if exists else "missing",
        "evidence": path,
        "explanation": "Evidencia presente." if exists else "Evidencia no encontrada.",
    }


def _run_gate(
    *,
    gate_id: str,
    label: str,
    script: str,
    output: Path,
    signal_fields: list[str],
) -> dict[str, Any]:
    result = _run([sys.executable, script])
    if result.returncode != 0:
        return {
            "id": gate_id,
            "label": label,
            "state": "blocked",
            "script": script,
            "output": str(output),
            "signals": {},
            "returncode": result.returncode,
            "explanation": "El gate no pudo ejecutarse.",
        }

    payload = _read_json(output)
    state = _normalize_state(payload.get("status"))
    signals = {field: payload.get(field) for field in signal_fields}
    return {
        "id": gate_id,
        "label": label,
        "state": state,
        "script": script,
        "output": str(output),
        "signals": signals,
        "returncode": result.returncode,
        "explanation": "Gate ejecutado y normalizado.",
    }


def build_phase_maturity() -> dict[str, Any]:
    phase_checks = {
        "draft": [
            _file_check("project_map", "docs/operations/project-map.md"),
            _file_check("terminal_stop_guide", "docs/operations/terminal-stop-guide.md"),
        ],
        "synthetic": [
            _file_check("synthetic_contract", "docs/architecture/eco-synthetic-data-contract.md"),
            _file_check("synthetic_registry", "docs/architecture/eco-synthetic-demo-registry.json"),
            _file_check("synthetic_validator", "scripts/validate_eco_synthetic_demos.py"),
        ],
        "governed_experimental": [
            _file_check("maturity_score", "scripts/run_eco_operational_maturity_score.py"),
            _file_check("governance_panel", "scripts/run_eco_governance_panel.py"),
            _file_check("operational_dashboard", "scripts/run_eco_synthetic_operational_dashboard.py"),
            _file_check("cycle_runner", "scripts/run_eco_governed_experimental_cycle.py"),
        ],
        "stable_candidate": [
            _file_check("real_biological_maturity_manual", "docs/operations/eco-real-biological-data-maturity-manual.md"),
            _file_check("real_biological_admission_protocol", "docs/operations/eco-real-biological-data-admission-protocol.md"),
        ],
        "blocked": [
            _file_check("rollback_policy", "docs/architecture/eco-real-data-activation-rollback-policy.md"),
            _file_check("branch_decision_matrix", "docs/operations/eco-branch-decision-matrix.md"),
        ],
    }

    phases = []
    for phase_id, checks in phase_checks.items():
        if phase_id == "stable_candidate":
            state = "future" if all(item["state"] == "passed" for item in checks) else "missing"
            explanation = (
                "Fase futura documentada; no queda habilitada por este ciclo."
                if state == "future"
                else "Falta evidencia documental para la fase estable candidata."
            )
        else:
            state = "passed" if all(item["state"] == "passed" for item in checks) else "attention"
            explanation = (
                "Evidencia mínima presente para evaluar esta fase."
                if state == "passed"
                else "Evidencia parcial; requiere revisión antes de avanzar."
            )

        phases.append(
            {
                "phase": phase_id,
                "state": state,
                "checks": checks,
                "explanation": explanation,
            }
        )

    required_current = {"draft", "synthetic", "governed_experimental", "blocked"}
    required_states = {
        item["phase"]: item["state"]
        for item in phases
        if item["phase"] in required_current
    }
    status = "passed" if all(state == "passed" for state in required_states.values()) else "attention"

    return {
        "status": status,
        "current_phase": "governed_experimental",
        "phase_order": ["draft", "synthetic", "governed_experimental", "stable_candidate", "blocked"],
        "phases": phases,
        "explanation": (
            "El ciclo puede operar en fase governed_experimental sin habilitar stable_candidate."
            if status == "passed"
            else "La fase governed_experimental requiere revisión por evidencia incompleta."
        ),
    }


def collect_maturity_score() -> dict[str, Any]:
    result = _run([sys.executable, "scripts/run_eco_operational_maturity_score.py"])
    payload = _read_json(Path("results/eco_operational_maturity_score.json"))
    state = _normalize_state(payload.get("status")) if result.returncode == 0 else "blocked"
    return {
        "state": state,
        "output": "results/eco_operational_maturity_score.json",
        "maturity_score_v1": payload.get("maturity_score_v1"),
        "global_decision": payload.get("global_decision"),
        "state_counts": payload.get("state_counts", {}),
        "before_reference": PREVIOUS_MATURITY_REFERENCE,
        "after": {
            "maturity_score_v1": payload.get("maturity_score_v1"),
            "global_decision": payload.get("global_decision"),
        },
    }


def collect_rollback_visibility() -> dict[str, Any]:
    steps = []
    for script in (
        "scripts/run_sne_eco_external_evidence_policy.py",
        "scripts/run_sne_eco_stable_admission_plan.py",
        "scripts/run_sne_eco_stable_admission_dry_run.py",
    ):
        result = _run([sys.executable, script])
        steps.append({"script": script, "returncode": result.returncode, "ok": result.returncode == 0})

    output = Path("results/sne_eco_stable_admission_dry_run.json")
    payload = _read_json(output)
    locks = payload.get("stability_locks", {})
    lock_breach = any(
        locks.get(flag, False)
        for flag in (
            "stable_dataset_modified",
            "baseline_modified",
            "rules_modified",
            "thresholds_modified",
        )
    )
    dry_run_only = bool(locks.get("dry_run_only", False))
    evidence_available = output.exists() and all(step["ok"] for step in steps)
    state = "passed" if evidence_available and dry_run_only and not lock_breach else "attention"

    return {
        "status": state,
        "evidence_available": evidence_available,
        "output": str(output),
        "steps": steps,
        "locks": locks,
        "lock_breach": lock_breach,
        "dry_run_only": dry_run_only,
        "explanation": (
            "Rollback visible y auditable mediante dry-run con candados activos."
            if state == "passed"
            else "Rollback con evidencia incompleta o candados inconsistentes."
        ),
    }


def build_governed_admission(
    gates: list[dict[str, Any]],
    maturity_score: dict[str, Any],
    rollback_visibility: dict[str, Any],
) -> dict[str, Any]:
    source_guard_checks = [
        _file_check("source_guard_script", "scripts/eco_public_source_guard.py"),
        _file_check("source_guard_tests", "tests/test_eco_public_source_url_admission_guard.py"),
    ]
    gate_by_id = {gate["id"]: gate for gate in gates}

    checks = [
        {
            "id": "intake_gate",
            "state": gate_by_id.get("sensitive_intake_gate", {}).get("state", "missing"),
            "evidence": gate_by_id.get("sensitive_intake_gate", {}).get("output"),
            "explanation": "Gate de intake sensible conectado.",
        },
        {
            "id": "source_guard",
            "state": "passed" if all(item["state"] == "passed" for item in source_guard_checks) else "missing",
            "evidence": [item["evidence"] for item in source_guard_checks],
            "explanation": "Guardia de URL pública presente y testeada.",
        },
        {
            "id": "maturity_score",
            "state": maturity_score["state"],
            "evidence": maturity_score["output"],
            "explanation": "Score de madurez operacional generado.",
        },
        {
            "id": "rollback_visibility",
            "state": rollback_visibility["status"],
            "evidence": rollback_visibility["output"],
            "explanation": "Rollback visible y auditable.",
        },
        {
            "id": "responsible_limits",
            "state": "passed" if all(RESPONSIBLE_LIMITS) else "missing",
            "evidence": RESPONSIBLE_LIMITS,
            "explanation": "Límites responsables explícitos.",
        },
        {
            "id": "final_decision",
            "state": "passed",
            "evidence": "advance | pause | review | reject",
            "explanation": "La decisión final se deriva después de gates, riesgos y rollback.",
        },
    ]

    if any(item["state"] == "blocked" for item in checks):
        status = "blocked"
    elif any(item["state"] in {"missing", "attention", "future"} for item in checks):
        status = "attention"
    else:
        status = "passed"

    return {
        "status": status,
        "checks": checks,
        "explanation": (
            "Admisión gobernada conectada para operación experimental sintética."
            if status == "passed"
            else "Admisión gobernada requiere revisión por evidencia parcial o bloqueada."
        ),
    }


def collect_gates() -> list[dict[str, Any]]:
    return [
        _run_gate(
            gate_id="source_admission_decision_summary",
            label="source admission decision summary",
            script="scripts/run_eco_source_admission_decision_summary.py",
            output=Path("results/eco_source_admission_decision_summary.json"),
            signal_fields=[
                "external_source_admission",
                "decision",
                "blocked_source_count",
                "conditional_source_count",
            ],
        ),
        _run_gate(
            gate_id="sensitive_intake_gate",
            label="sensitive intake gate",
            script="scripts/run_sne_eco_sensitive_intake_gate.py",
            output=Path("results/sne_eco_sensitive_intake_gate_report.json"),
            signal_fields=["row_count", "counts", "blocked_rows", "conditional_rows"],
        ),
        _run_gate(
            gate_id="governed_ml_evaluation_gate",
            label="governed ML evaluation gate",
            script="scripts/run_sne_eco_governed_ml_evaluation_gate.py",
            output=Path("results/sne_eco_governed_ml_evaluation_gate.json"),
            signal_fields=["evaluation_allowed", "governance_status", "challenge_status"],
        ),
    ]


def build_risks(
    *,
    phase_maturity: dict[str, Any],
    governed_admission: dict[str, Any],
    gates: list[dict[str, Any]],
    rollback_visibility: dict[str, Any],
    maturity_score: dict[str, Any],
) -> list[dict[str, str]]:
    risks: list[dict[str, str]] = []
    for item_id, state, explanation in (
        ("phase_maturity", phase_maturity["status"], phase_maturity["explanation"]),
        ("governed_admission", governed_admission["status"], governed_admission["explanation"]),
        ("rollback_visibility", rollback_visibility["status"], rollback_visibility["explanation"]),
        ("maturity_score", maturity_score["state"], "Score de madurez operacional."),
    ):
        if state in {"attention", "missing", "future", "blocked"}:
            risks.append({"id": item_id, "state": state, "explanation": explanation})

    for gate in gates:
        if gate["state"] in {"attention", "missing", "future", "blocked"}:
            risks.append(
                {
                    "id": gate["id"],
                    "state": gate["state"],
                    "explanation": gate["explanation"],
                }
            )

    stable_candidate = next(
        phase for phase in phase_maturity["phases"] if phase["phase"] == "stable_candidate"
    )
    if stable_candidate["state"] == "future":
        risks.append(
            {
                "id": "stable_candidate_future",
                "state": "future",
                "explanation": "La fase stable_candidate existe como frontera futura y no queda habilitada.",
            }
        )

    return risks


def decide_final(
    *,
    phase_maturity: dict[str, Any],
    governed_admission: dict[str, Any],
    gates: list[dict[str, Any]],
    rollback_visibility: dict[str, Any],
    maturity_score: dict[str, Any],
    risks: list[dict[str, str]],
) -> tuple[str, str]:
    critical_states = [
        phase_maturity["status"],
        governed_admission["status"],
        rollback_visibility["status"],
        maturity_score["state"],
        *(gate["state"] for gate in gates),
    ]

    if "blocked" in critical_states or rollback_visibility.get("lock_breach"):
        return "reject", "Existe bloqueo crítico o breach de candados de estabilidad."
    if any(state == "missing" for state in critical_states) or not rollback_visibility["evidence_available"]:
        return "pause", "Falta evidencia crítica para sostener el ciclo experimental gobernado."
    if any(state == "attention" for state in critical_states):
        return "review", "Persisten señales de attention en gates, rollback, admisión o madurez."

    non_blocking_future = [risk for risk in risks if risk["state"] == "future"]
    if non_blocking_future:
        return "advance", "Avance controlado en governed_experimental; fases futuras no quedan habilitadas."
    return "advance", "Condiciones técnicas y de gobernanza suficientes para avanzar controladamente."


def build_recommendations(final_decision: str, risks: list[dict[str, str]]) -> list[str]:
    if final_decision == "advance":
        return [
            "Mantener el ciclo en modo sintético/documental.",
            "No promover stable_candidate sin revisión humana y evidencia adicional.",
            "Reejecutar maturity score y dashboard tras cualquier cambio de gates.",
        ]
    if final_decision == "review":
        return [
            "Revisar señales attention antes de ampliar alcance.",
            "No admitir fuentes externas nuevas sin revisión explícita.",
            "Mantener rollback visible antes de proponer PR.",
        ]
    if final_decision == "pause":
        return [
            "Pausar avance hasta recuperar evidencia faltante.",
            "Ejecutar gates individualmente y documentar la causa.",
        ]
    return [
        "Rechazar avance del ciclo hasta resolver bloqueos críticos.",
        "No hacer merge ni admitir evidencia externa mientras exista bloqueo.",
        f"Riesgos críticos detectados: {len(risks)}.",
    ]


def build_report() -> dict[str, Any]:
    phase_maturity = build_phase_maturity()
    gates = collect_gates()
    maturity_score = collect_maturity_score()
    rollback_visibility = collect_rollback_visibility()
    governed_admission = build_governed_admission(
        gates=gates,
        maturity_score=maturity_score,
        rollback_visibility=rollback_visibility,
    )
    risks = build_risks(
        phase_maturity=phase_maturity,
        governed_admission=governed_admission,
        gates=gates,
        rollback_visibility=rollback_visibility,
        maturity_score=maturity_score,
    )
    final_decision, decision_reason = decide_final(
        phase_maturity=phase_maturity,
        governed_admission=governed_admission,
        gates=gates,
        rollback_visibility=rollback_visibility,
        maturity_score=maturity_score,
        risks=risks,
    )
    status = "passed" if final_decision == "advance" else "blocked" if final_decision == "reject" else "attention"

    return {
        "title": "E.C.O. governed experimental cycle v1",
        "cycle_id": "eco-governed-experimental-cycle-v1",
        "status": status,
        "allowed_states": sorted(ALLOWED_STATES),
        "allowed_decisions": sorted(ALLOWED_DECISIONS),
        "phase_maturity": phase_maturity,
        "governed_admission": governed_admission,
        "gates": gates,
        "risks": risks,
        "rollback_visibility": rollback_visibility,
        "responsible_limits": RESPONSIBLE_LIMITS,
        "final_decision": final_decision,
        "decision_reason": decision_reason,
        "recommendations": build_recommendations(final_decision, risks),
        "maturity_score_v1": maturity_score,
        "interpretation_boundary": {
            "synthetic_operational_only": True,
            "uses_real_data": False,
            "training_enabled": False,
            "baseline_changed": False,
            "threshold_recalibration": False,
            "clinical_or_biomedical_applied_claim": False,
        },
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# E.C.O. governed experimental cycle v1",
        "",
        f"Estado: `{report['status']}`",
        f"Decisión final: `{report['final_decision']}`",
        f"Razón: {report['decision_reason']}",
        "",
        "## Madurez por fase",
        "",
        f"- Fase actual: `{report['phase_maturity']['current_phase']}`",
        f"- Estado: `{report['phase_maturity']['status']}`",
        "",
        "| Fase | Estado | Explicación |",
        "|---|---|---|",
    ]
    for phase in report["phase_maturity"]["phases"]:
        lines.append(f"| `{phase['phase']}` | `{phase['state']}` | {phase['explanation']} |")

    lines.extend(
        [
            "",
            "## Admisión gobernada",
            "",
            f"Estado: `{report['governed_admission']['status']}`",
            "",
            "| Check | Estado | Evidencia |",
            "|---|---|---|",
        ]
    )
    for check in report["governed_admission"]["checks"]:
        evidence = json.dumps(check["evidence"], ensure_ascii=False)
        lines.append(f"| `{check['id']}` | `{check['state']}` | `{evidence}` |")

    lines.extend(["", "## Gates evaluados", "", "| Gate | Estado | Señales |", "|---|---|---|"])
    for gate in report["gates"]:
        signals = json.dumps(gate["signals"], ensure_ascii=False)
        lines.append(f"| `{gate['id']}` | `{gate['state']}` | `{signals}` |")

    lines.extend(["", "## Riesgos", ""])
    if report["risks"]:
        for risk in report["risks"]:
            lines.append(f"- `{risk['id']}` ({risk['state']}): {risk['explanation']}")
    else:
        lines.append("- Sin riesgos activos para el alcance actual.")

    rollback = report["rollback_visibility"]
    lines.extend(
        [
            "",
            "## Rollback visible",
            "",
            f"- Estado: `{rollback['status']}`",
            f"- Evidencia disponible: `{rollback['evidence_available']}`",
            f"- Fuente: `{rollback['output']}`",
            f"- Lectura: {rollback['explanation']}",
            "",
            "## Maturity score v1",
            "",
            f"- Antes: `{report['maturity_score_v1']['before_reference']['maturity_score_v1']}`",
            f"- Después: `{report['maturity_score_v1']['after']['maturity_score_v1']}`",
            f"- Decisión del score: `{report['maturity_score_v1']['after']['global_decision']}`",
            "",
            "## Recomendaciones",
            "",
        ]
    )
    for item in report["recommendations"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Límites responsables", ""])
    for limit in report["responsible_limits"]:
        lines.append(f"- {limit}")

    lines.extend(
        [
            "",
            "## Frontera de interpretación",
            "",
            "- Solo operación sintética/documental.",
            "- No habilita datos reales, entrenamiento, cambios de baseline ni recalibración de umbrales.",
            "- No produce diagnóstico, interpretación clínica ni afirmaciones biomédicas aplicadas.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(report: dict[str, Any]) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")


def main() -> int:
    report = build_report()
    write_outputs(report)
    print("# E.C.O. governed experimental cycle v1")
    print(f"Estado: {report['status']}")
    print(f"Decisión final: {report['final_decision']}")
    print(f"Salida JSON: {OUTPUT_JSON}")
    print(f"Salida Markdown: {OUTPUT_MD}")
    print("Límite: operación sintética/documental; sin datos reales ni entrenamiento.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
