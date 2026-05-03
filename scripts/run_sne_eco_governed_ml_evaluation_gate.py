from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


OUTPUT_JSON = Path("results/sne_eco_governed_ml_evaluation_gate.json")
OUTPUT_MD = Path("results/sne_eco_governed_ml_evaluation_gate.md")

GOVERNANCE_JSON = Path("results/sne_eco_sensitive_governance_summary.json")
SPLIT_JSON = Path("results/sne_eco_empirical_train_eval_split_report.json")
BASELINE_JSON = Path("results/sne_eco_ml_baseline_report.json")
CHALLENGE_JSON = Path("results/sne_eco_ml_challenge_eval_report.json")

RESPONSIBLE_LIMIT = (
    "Gate educativo/experimental de evaluación ML gobernada S.N.E.-E.C.O.; "
    "no ingiere datos reales, no entrena modelos nuevos, no diagnostica, "
    "no tiene uso clínico aplicado, no realiza inferencias forenses, "
    "no afirma conciencia humana real, no recalibra umbrales "
    "y no modifica baseline estable."
)


def run_step(label: str, command: list[str]) -> dict:
    result = subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
    )

    return {
        "label": label,
        "command": " ".join(command),
        "returncode": result.returncode,
        "ok": result.returncode == 0,
        "stdout_tail": result.stdout[-1200:],
        "stderr_tail": result.stderr[-1200:],
    }


def load_json(path: Path) -> dict:
    if not path.exists():
        return {"missing": True, "path": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def decide_status(steps: list[dict], governance: dict, baseline: dict, challenge: dict) -> str:
    if any(not step["ok"] for step in steps):
        return "red"

    if governance.get("status") != "green":
        return "red"

    if baseline.get("status") not in {"green", "attention"}:
        return "red"

    if challenge.get("status") not in {"green", "attention"}:
        return "red"

    if challenge.get("forbidden_not_rejected"):
        return "red"

    return "green"


def build_report(write_outputs: bool = False) -> dict:
    steps = [
        run_step(
            "sensitive_governance_summary",
            [sys.executable, "scripts/run_sne_eco_sensitive_governance_summary.py"],
        ),
        run_step(
            "empirical_train_eval_split",
            [sys.executable, "scripts/run_sne_eco_empirical_train_eval_split.py"],
        ),
        run_step(
            "ml_baseline",
            [sys.executable, "scripts/run_sne_eco_ml_baseline.py"],
        ),
        run_step(
            "ml_challenge_eval",
            [sys.executable, "scripts/run_sne_eco_ml_challenge_eval.py"],
        ),
    ]

    governance = load_json(GOVERNANCE_JSON)
    split = load_json(SPLIT_JSON)
    baseline = load_json(BASELINE_JSON)
    challenge = load_json(CHALLENGE_JSON)

    status = decide_status(steps, governance, baseline, challenge)

    report = {
        "status": status,
        "evaluation_allowed": status == "green",
        "steps": steps,
        "governance_status": governance.get("status"),
        "split_status": split.get("status"),
        "baseline_status": baseline.get("status"),
        "challenge_status": challenge.get("status"),
        "baseline_accuracy": baseline.get("accuracy"),
        "challenge_accuracy": challenge.get("accuracy"),
        "governance_counts": governance.get("combined_counts", {}),
        "blocked_items": {
            "intake": governance.get("blocked_intake_rows", []),
            "sources": governance.get("blocked_sources", []),
        },
        "conditional_items": {
            "intake": governance.get("conditional_intake_rows", []),
            "sources": governance.get("conditional_sources", []),
        },
        "responsible_limit": RESPONSIBLE_LIMIT,
    }

    if write_outputs:
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_JSON.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    return report


def to_markdown(report: dict) -> str:
    icon = {
        "green": "🟢",
        "attention": "🟡",
        "red": "🔴",
    }.get(report["status"], "⚪")

    lines = [
        "# Gate de evaluación ML gobernada S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Evaluación permitida: `{report['evaluation_allowed']}`",
        "",
        "## Estados internos",
        "",
        "| Componente | Estado |",
        "|---|---|",
        f"| Gobernanza sensible | `{report['governance_status']}` |",
        f"| Split train/eval | `{report['split_status']}` |",
        f"| Baseline ML | `{report['baseline_status']}` |",
        f"| Challenge eval | `{report['challenge_status']}` |",
        "",
        "## Métricas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Accuracy baseline | {report['baseline_accuracy']} |",
        f"| Accuracy challenge | {report['challenge_accuracy']} |",
        f"| Permitidos gobernanza | {report['governance_counts'].get('allowed')} |",
        f"| Condicionales gobernanza | {report['governance_counts'].get('conditional')} |",
        f"| Bloqueados gobernanza | {report['governance_counts'].get('blocked')} |",
        "",
        "## Pasos ejecutados",
        "",
        "| Paso | OK | Código salida |",
        "|---|---:|---:|",
    ]

    for step in report["steps"]:
        lines.append(f"| `{step['label']}` | `{step['ok']}` | `{step['returncode']}` |")

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "- Este gate obliga a pasar por gobernanza antes de evaluar ML.",
            "- No entrena modelos nuevos.",
            "- No cambia reglas, baseline ni umbrales.",
            "- Si gobernanza falla, la evaluación queda marcada como no permitida.",
            "",
            "## Límite responsable",
            "",
            report["responsible_limit"],
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    report = build_report(write_outputs=True)
    print(to_markdown(report))
    print("OK: gate de evaluación ML gobernada S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
