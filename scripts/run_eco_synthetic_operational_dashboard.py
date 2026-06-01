from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

JSON_OUTPUT = Path("results/eco_synthetic_operational_dashboard.json")
MD_OUTPUT = Path("results/eco_synthetic_operational_dashboard.md")

LIMIT = "datos sintéticos; sin entrenamiento; sin datos sensibles; sin modificación de baseline; sin recalibración; sin afirmaciones biomédicas aplicadas; sin libre albedrío real; sin conciencia"
OK_STATUSES = {"passed", "green", "ok", "success"}
ATTENTION_STATUSES = {"attention", "yellow", "conditional", "warning"}
RED_STATUSES = {"red", "blocked", "reject", "error", "failed"}

MATURITY_OUTPUT = Path("results/eco_operational_maturity_score.json")

RELEVANT_GATES = [
    {
        "id": "source_admission_decision_summary",
        "label": "source admission decision summary",
        "script": "scripts/run_eco_source_admission_decision_summary.py",
        "output": Path("results/eco_source_admission_decision_summary.json"),
        "signal_fields": [
            "external_source_admission",
            "decision",
            "blocked_source_count",
            "conditional_source_count",
        ],
    },
    {
        "id": "sensitive_intake_gate",
        "label": "sensitive intake gate",
        "script": "scripts/run_sne_eco_sensitive_intake_gate.py",
        "output": Path("results/sne_eco_sensitive_intake_gate_report.json"),
        "signal_fields": ["row_count", "counts", "blocked_rows", "conditional_rows"],
    },
    {
        "id": "governed_ml_evaluation_gate",
        "label": "governed ml evaluation gate",
        "script": "scripts/run_sne_eco_governed_ml_evaluation_gate.py",
        "output": Path("results/sne_eco_governed_ml_evaluation_gate.json"),
        "signal_fields": ["evaluation_allowed", "governance_status", "challenge_status"],
    },
]

ROLLBACK_PIPELINE = [
    "scripts/run_sne_eco_external_evidence_policy.py",
    "scripts/run_sne_eco_stable_admission_plan.py",
    "scripts/run_sne_eco_stable_admission_dry_run.py",
]
ROLLBACK_OUTPUT = Path("results/sne_eco_stable_admission_dry_run.json")

COMPONENTS = [
    {
        "id": "adaptive_dataset_readiness_gate",
        "label": "adaptive dataset readiness gate",
        "script": "scripts/run_eco_adaptive_dataset_readiness_gate.py",
        "output": Path("results/eco_adaptive_dataset_readiness_gate.json"),
    },
    {
        "id": "source_admission_decision_summary",
        "label": "source admission decision summary",
        "script": "scripts/run_eco_source_admission_decision_summary.py",
        "output": Path("results/eco_source_admission_decision_summary.json"),
    },
    {
        "id": "suite_report",
        "label": "synthetic demos suite report",
        "script": "scripts/run_eco_synthetic_demos_suite_report.py",
        "output": Path("results/eco_synthetic_demos_suite_report.json"),
    },
    {
        "id": "comparison_report",
        "label": "synthetic demo comparison report",
        "script": "scripts/run_eco_synthetic_demo_comparison_report.py",
        "output": Path("results/eco_synthetic_demo_comparison_report.json"),
    },
    {
        "id": "signal_matrix_report",
        "label": "synthetic signal matrix report",
        "script": "scripts/run_eco_synthetic_signal_matrix_report.py",
        "output": Path("results/eco_synthetic_signal_matrix_report.json"),
    },
    {
        "id": "adaptive_dataset_report",
        "label": "adaptive dataset operational report",
        "script": "scripts/run_eco_adaptive_dataset_report.py",
        "output": Path("results/eco_adaptive_dataset_report.json"),
    },
    {
        "id": "governance_panel",
        "label": "governance panel",
        "script": "scripts/run_eco_governance_panel.py",
        "output": Path("results/eco_governance_panel.json"),
    },
    {
        "id": "capabilities_report",
        "label": "capabilities report",
        "script": "scripts/run_eco_capabilities_report.py",
        "output": Path("results/eco_capabilities_report.json"),
    },
    {
        "id": "laos_governance_gate",
        "label": "LAOS Governance Gate",
        "script": "scripts/run_eco_laos_governance_gate_demo.py",
        "output": Path("results/eco_laos_governance_gate_demo.json"),
    },
]


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"No se encontró salida esperada: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_status(raw_status: Any) -> str:
    raw_status = str(raw_status or "unknown").lower()
    if raw_status in OK_STATUSES:
        return "passed"
    if raw_status in ATTENTION_STATUSES:
        return "attention"
    if raw_status in RED_STATUSES:
        return "red"
    return raw_status


def run_component(component: dict) -> dict:
    result = _run([sys.executable, component["script"]])
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    payload = _read_json(component["output"])
    status = normalize_status(payload.get("status") or payload.get("estado") or "passed")
    return {
        "id": component["id"],
        "label": component["label"],
        "status": status,
        "classification": payload.get("classification", "allowed"),
        "output": str(component["output"]),
    }


def _run_git(args: list[str]) -> str:
    return _run(["git", *args]).stdout.strip()


def collect_repo_status() -> dict[str, Any]:
    eco_status = _run([sys.executable, "scripts/run_eco_status.py"])
    status_short = _run_git(["status", "--short"])
    branch = _run_git(["branch", "--show-current"]) or "desconocida"
    head = _run_git(["rev-parse", "--short", "HEAD"])
    origin_main = _run_git(["rev-parse", "--short", "origin/main"])
    tree_clean = status_short == ""
    on_main = branch == "main"
    state = "green" if tree_clean else "attention"

    return {
        "state": state,
        "branch": branch,
        "head": head,
        "origin_main": origin_main,
        "tree_clean": tree_clean,
        "on_main": on_main,
        "eco_status_returncode": eco_status.returncode,
        "eco_status_source": "scripts/run_eco_status.py",
        "eco_status_excerpt": "\n".join(eco_status.stdout.splitlines()[:12]),
    }


def collect_maturity_score() -> dict[str, Any]:
    result = _run([sys.executable, "scripts/run_eco_operational_maturity_score.py"])
    if result.returncode != 0:
        return {
            "status": "attention",
            "global_decision": "attention",
            "classification": "attention_required",
            "score_v1": None,
            "state_counts": {},
            "attention_dimensions": [],
            "output": str(MATURITY_OUTPUT),
            "error": "No se pudo generar el score de madurez.",
        }

    payload = _read_json(MATURITY_OUTPUT)
    attention_dimensions = [
        item["dimension_id"]
        for item in payload.get("dimensions", [])
        if item.get("state") in {"attention", "missing", "future"}
    ]
    return {
        "status": normalize_status(payload.get("status")),
        "global_decision": payload.get("global_decision", "attention"),
        "classification": payload.get("classification", "attention_required"),
        "score_v1": payload.get("maturity_score_v1"),
        "state_counts": payload.get("state_counts", {}),
        "attention_dimensions": attention_dimensions,
        "output": str(MATURITY_OUTPUT),
    }


def collect_relevant_gates() -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = []
    for gate in RELEVANT_GATES:
        result = _run([sys.executable, gate["script"]])
        if result.returncode != 0:
            gates.append(
                {
                    "id": gate["id"],
                    "label": gate["label"],
                    "status": "red",
                    "output": str(gate["output"]),
                    "signals": {},
                    "error": "No se pudo ejecutar el gate.",
                }
            )
            continue

        payload = _read_json(gate["output"])
        signals = {field: payload.get(field) for field in gate["signal_fields"]}
        gates.append(
            {
                "id": gate["id"],
                "label": gate["label"],
                "status": normalize_status(payload.get("status")),
                "classification": payload.get("classification", "n/a"),
                "output": str(gate["output"]),
                "signals": signals,
            }
        )
    return gates


def collect_rollback_evidence() -> dict[str, Any]:
    steps = []
    for script_path in ROLLBACK_PIPELINE:
        result = _run([sys.executable, script_path])
        steps.append(
            {
                "script": script_path,
                "returncode": result.returncode,
                "ok": result.returncode == 0,
            }
        )

    if any(not step["ok"] for step in steps) or not ROLLBACK_OUTPUT.exists():
        return {
            "status": "attention",
            "evidence_available": False,
            "output": str(ROLLBACK_OUTPUT),
            "steps": steps,
            "locks": {},
            "explanation": "No se pudo obtener evidencia de rollback desde dry-run.",
        }

    payload = _read_json(ROLLBACK_OUTPUT)
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
    status = "passed" if (not lock_breach and dry_run_only) else "attention"
    explanation = (
        "Rollback trazable con candados activos en dry-run."
        if status == "passed"
        else "Rollback con evidencia incompleta o candados inconsistentes."
    )

    return {
        "status": status,
        "evidence_available": True,
        "output": str(ROLLBACK_OUTPUT),
        "steps": steps,
        "locks": locks,
        "metrics": payload.get("metrics", {}),
        "explanation": explanation,
    }


def build_current_risks(
    repo_status: dict[str, Any],
    maturity_score: dict[str, Any],
    relevant_gates: list[dict[str, Any]],
    rollback_evidence: dict[str, Any],
) -> list[str]:
    risks: list[str] = []
    if repo_status["state"] != "green":
        risks.append("El repositorio no está limpio; se recomienda pausar avance hasta cerrar cambios.")
    if maturity_score["global_decision"] != "passed":
        risks.append(
            "El score de madurez sigue en attention; faltan integraciones completas en "
            f"{len(maturity_score['attention_dimensions'])} dimensiones."
        )
    for gate in relevant_gates:
        if gate["status"] == "red":
            risks.append(f"Gate crítico en rojo: {gate['id']}.")
        elif gate["status"] == "attention":
            risks.append(f"Gate con atención requerida: {gate['id']}.")
    if rollback_evidence["status"] != "passed":
        risks.append("Evidencia de rollback incompleta o no verificable.")
    if not risks:
        risks.append("Sin riesgos operativos críticos detectados para el alcance sintético actual.")
    return risks


def decide_final_action(
    repo_status: dict[str, Any],
    maturity_score: dict[str, Any],
    relevant_gates: list[dict[str, Any]],
    rollback_evidence: dict[str, Any],
) -> tuple[str, str]:
    if any(gate["status"] == "red" for gate in relevant_gates):
        return "reject", "Hay gates críticos en rojo."

    locks = rollback_evidence.get("locks", {})
    lock_breach = any(
        locks.get(flag, False)
        for flag in (
            "stable_dataset_modified",
            "baseline_modified",
            "rules_modified",
            "thresholds_modified",
        )
    )
    if lock_breach:
        return "reject", "Se detectó breach en candados de estabilidad del rollback."

    if repo_status["state"] != "green" or not rollback_evidence["evidence_available"]:
        return "pause", "Se requiere pausa: árbol no limpio o evidencia de rollback no disponible."

    if maturity_score["global_decision"] != "passed" or any(
        gate["status"] == "attention" for gate in relevant_gates
    ):
        return "review", "Persisten señales de attention que requieren revisión antes de avanzar."

    return "advance", "Condiciones técnicas sintéticas coherentes para avanzar controladamente."


def collect_responsible_limits(
    maturity_score: dict[str, Any],
    relevant_gates: list[dict[str, Any]],
    rollback_evidence: dict[str, Any],
) -> list[str]:
    limits = [LIMIT]
    if maturity_score.get("status"):
        limits.append(
            "score de madurez técnico-operativo; no valida afirmaciones científicas ni biomédicas aplicadas"
        )
    for gate in relevant_gates:
        if gate["id"] == "source_admission_decision_summary":
            limits.append("admisión de fuentes externas en pausa hasta revisión explícita")
        if gate["id"] == "sensitive_intake_gate":
            limits.append("intake sensible con bloqueo de datos personales o uso aplicado")
        if gate["id"] == "governed_ml_evaluation_gate":
            limits.append("evaluación ML gobernada sin entrenamiento nuevo ni uso de datos reales")
    if rollback_evidence.get("evidence_available"):
        limits.append("rollback solo en dry-run con candados de estabilidad activos")
    unique_limits: list[str] = []
    seen: set[str] = set()
    for item in limits:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            unique_limits.append(item.strip())
    return unique_limits


def build_dashboard() -> dict:
    components = [run_component(component) for component in COMPONENTS]
    component_passed = all(component["status"] == "passed" for component in components)
    repo_status = collect_repo_status()
    maturity_score = collect_maturity_score()
    relevant_gates = collect_relevant_gates()
    rollback_evidence = collect_rollback_evidence()
    current_risks = build_current_risks(
        repo_status=repo_status,
        maturity_score=maturity_score,
        relevant_gates=relevant_gates,
        rollback_evidence=rollback_evidence,
    )
    final_decision, decision_reason = decide_final_action(
        repo_status=repo_status,
        maturity_score=maturity_score,
        relevant_gates=relevant_gates,
        rollback_evidence=rollback_evidence,
    )
    status = "passed" if final_decision == "advance" else "red" if final_decision == "reject" else "attention"
    classification = {
        "advance": "allowed",
        "review": "conditional",
        "pause": "attention_required",
        "reject": "blocked",
    }[final_decision]
    responsible_limits = collect_responsible_limits(
        maturity_score=maturity_score,
        relevant_gates=relevant_gates,
        rollback_evidence=rollback_evidence,
    )

    return {
        "title": "E.C.O. synthetic operational dashboard",
        "panel_kind": "end_to_end_operational_panel_v1",
        "status": status,
        "classification": classification,
        "component_count": len(components),
        "components": components,
        "components_all_passed": component_passed,
        "repo_status": repo_status,
        "maturity_score": maturity_score,
        "relevant_gates": relevant_gates,
        "current_risks": current_risks,
        "rollback_evidence": rollback_evidence,
        "final_decision": final_decision,
        "decision_reason": decision_reason,
        "responsible_limits": responsible_limits,
        "limit": LIMIT,
    }


def write_outputs(dashboard: dict) -> None:
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# E.C.O. synthetic operational dashboard", ""]
    md.append("Estado: {}".format(dashboard["status"]))
    md.append("Decisión final: `{}`".format(dashboard["final_decision"]))
    md.append("Razón: {}".format(dashboard["decision_reason"]))
    md.append("Componentes: {}".format(dashboard["component_count"]))
    md.append("")
    md.append("## Repo / eco-status")
    md.append("")
    repo_status = dashboard["repo_status"]
    md.append("| Campo | Valor |")
    md.append("|---|---|")
    md.append("| state | `{}` |".format(repo_status["state"]))
    md.append("| branch | `{}` |".format(repo_status["branch"]))
    md.append("| head | `{}` |".format(repo_status["head"]))
    md.append("| origin_main | `{}` |".format(repo_status["origin_main"]))
    md.append("| tree_clean | `{}` |".format(repo_status["tree_clean"]))
    md.append("| on_main | `{}` |".format(repo_status["on_main"]))
    md.append("")
    md.append("## Score de madurez")
    md.append("")
    maturity = dashboard["maturity_score"]
    md.append("- Estado global: `{}`".format(maturity["global_decision"]))
    md.append("- Score v1: `{}`".format(maturity["score_v1"]))
    md.append("- Dimensiones en attention/future/missing: `{}`".format(len(maturity["attention_dimensions"])))
    md.append("- Fuente: `{}`".format(maturity["output"]))
    md.append("")
    md.append("## Gates relevantes")
    md.append("")
    md.append("| Gate | Estado | Señales |")
    md.append("|---|---|---|")
    for gate in dashboard["relevant_gates"]:
        md.append(
            "| {} | `{}` | `{}` |".format(
                gate["id"],
                gate["status"],
                json.dumps(gate.get("signals", {}), ensure_ascii=False),
            )
        )
    md.append("")
    md.append("## Riesgos actuales")
    md.append("")
    for risk in dashboard["current_risks"]:
        md.append("- {}".format(risk))
    md.append("")
    md.append("## Evidencia de rollback")
    md.append("")
    rollback = dashboard["rollback_evidence"]
    md.append("- Estado: `{}`".format(rollback["status"]))
    md.append("- Evidencia disponible: `{}`".format(rollback["evidence_available"]))
    md.append("- Fuente: `{}`".format(rollback["output"]))
    md.append("- Lectura: {}".format(rollback["explanation"]))
    md.append("")
    md.append("## Componentes conectados")
    md.append("")
    md.append("| Componente | Estado | Clasificación | Salida |")
    md.append("|---|---|---|---|")
    for component in dashboard["components"]:
        md.append("| {} | {} | {} | {} |".format(component["label"], component["status"], component["classification"], component["output"]))
    md.append("")
    md.append("## Límites responsables")
    md.append("")
    for item in dashboard["responsible_limits"]:
        md.append("- {}".format(item))
    md.append("")
    md.append("## Decisión final")
    md.append("")
    md.append("- `advance`: condiciones técnicas sintéticas en verde.")
    md.append("- `pause`: falta evidencia crítica o hay estado de repo no apto.")
    md.append("- `review`: hay señales de attention que requieren revisión.")
    md.append("- `reject`: hay breach crítico en gates o estabilidad.")
    md.append("")
    md.append("Límite: {}.".format(dashboard["limit"]))
    MD_OUTPUT.write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> int:
    dashboard = build_dashboard()
    write_outputs(dashboard)
    print("# E.C.O. synthetic operational dashboard")
    print("Estado: {}".format(dashboard["status"]))
    print("Decisión final: {}".format(dashboard["final_decision"]))
    print("Componentes: {}".format(dashboard["component_count"]))
    print("Salida JSON: {}".format(JSON_OUTPUT))
    print("Salida Markdown: {}".format(MD_OUTPUT))
    print("Límite: {}.".format(dashboard["limit"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
