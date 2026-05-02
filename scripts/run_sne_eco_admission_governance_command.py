from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_JSON = Path("results/sne_eco_admission_governance_command.json")
DEFAULT_OUTPUT_MD = Path("results/sne_eco_admission_governance_command.md")


CHAIN = [
    {
        "name": "external_evidence_policy",
        "command": [sys.executable, "scripts/run_sne_eco_external_evidence_policy.py"],
        "output": Path("results/sne_eco_external_evidence_policy.json"),
    },
    {
        "name": "stable_admission_plan",
        "command": [sys.executable, "scripts/run_sne_eco_stable_admission_plan.py"],
        "output": Path("results/sne_eco_stable_admission_plan.json"),
    },
    {
        "name": "stable_admission_dry_run",
        "command": [sys.executable, "scripts/run_sne_eco_stable_admission_dry_run.py"],
        "output": Path("results/sne_eco_stable_admission_dry_run.json"),
    },
    {
        "name": "compare_against_rc1",
        "command": [sys.executable, "scripts/run_sne_eco_compare_against_rc1.py"],
        "output": Path("results/sne_eco_compare_against_rc1.json"),
    },
]


RESPONSIBLE_LIMIT = (
    "Comando educativo/experimental de gobernanza de admisión; ejecuta reportes "
    "existentes sin modificar dataset estable, baseline, reglas ni umbrales. "
    "No representa desempeño general, no modela conciencia humana y no tiene uso clínico/forense."
)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run_chain() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for step in CHAIN:
        completed = subprocess.run(
            step["command"],
            check=False,
            capture_output=True,
            text=True,
        )

        output_path = step["output"]
        payload = load_json(output_path)

        results.append(
            {
                "name": step["name"],
                "returncode": completed.returncode,
                "ok": completed.returncode == 0 and output_path.exists(),
                "output_json": str(output_path),
                "summary": payload,
            }
        )

    return results


def build_report(steps: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [step for step in steps if not step["ok"]]

    dry_run = next(
        (step["summary"] for step in steps if step["name"] == "stable_admission_dry_run"),
        {},
    )
    comparison = next(
        (step["summary"] for step in steps if step["name"] == "compare_against_rc1"),
        {},
    )

    return {
        "title": "S.N.E.-E.C.O. Admission Governance Command",
        "baseline": "sne-eco-v1.0-rc1",
        "status": "green" if not failed else "red",
        "reason": (
            "Cadena de gobernanza ejecutada sin fallos."
            if not failed
            else "Una o más etapas de gobernanza fallaron."
        ),
        "steps": steps,
        "stability_locks": {
            "stable_dataset_modified": False,
            "baseline_modified": False,
            "rules_modified": False,
            "thresholds_modified": False,
            "dry_run_only": True,
        },
        "dry_run_status": dry_run.get("status"),
        "comparison_status": comparison.get("status"),
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# S.N.E.-E.C.O. — Admission Governance Command",
        "",
        "Comando único para ejecutar la cadena de gobernanza de admisión posterior a RC1.",
        "",
        f"Baseline protegido: `{report['baseline']}`",
        f"Estado: `{report['status']}`",
        f"Motivo: {report['reason']}",
        "",
        "## Etapas ejecutadas",
        "",
        "| Etapa | OK | Reporte JSON |",
        "|---|---:|---|",
    ]

    for step in report["steps"]:
        lines.append(
            f"| {step['name']} | {step['ok']} | `{step['output_json']}` |"
        )

    locks = report["stability_locks"]

    lines.extend(
        [
            "",
            "## Candados de estabilidad",
            "",
            f"- Dataset estable modificado: `{locks['stable_dataset_modified']}`",
            f"- Baseline modificado: `{locks['baseline_modified']}`",
            f"- Reglas modificadas: `{locks['rules_modified']}`",
            f"- Umbrales modificados: `{locks['thresholds_modified']}`",
            f"- Solo dry-run: `{locks['dry_run_only']}`",
            "",
            "## Lectura operativa",
            "",
            "Este comando no admite evidencia externa al dataset estable. Solo ejecuta la cadena de observación, política, plan, simulación y comparación contra RC1.",
            "",
            "## Límite responsable",
            "",
            report["responsible_limit"],
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    args.output_json.parent.mkdir(parents=True, exist_ok=True)

    steps = run_chain()
    report = build_report(steps)

    args.output_json.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    args.output_md.write_text(to_markdown(report), encoding="utf-8")

    print("OK: comando de gobernanza de admisión S.N.E.-E.C.O. generado.")
    print(f"- {args.output_json.resolve()}")
    print(f"- {args.output_md.resolve()}")

    if report["status"] != "green":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
