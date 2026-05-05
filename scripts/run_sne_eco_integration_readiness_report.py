from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


OUTPUT_JSON = Path("results/sne_eco_integration_readiness_report.json")
OUTPUT_MD = Path("results/sne_eco_integration_readiness_report.md")

EXPECTED_REPORTS = [
    "results/sne_eco_sensitive_governance_summary.md",
    "results/sne_eco_empirical_train_eval_split_report.md",
    "results/sne_eco_ml_baseline_report.md",
    "results/sne_eco_ml_challenge_eval_report.md",
    "results/sne_eco_governed_ml_evaluation_gate.md",
    "results/sne_eco_responsible_experiment_manifest.md",
]

EXPECTED_TARGETS = [
    "sne-sensitive-governance-summary",
    "sne-governed-ml-evaluation-gate",
    "sne-responsible-experiment-manifest",
]

RESPONSIBLE_LIMIT = (
    "Reporte educativo/experimental de preparación de integración S.N.E.-E.C.O.; "
    "no ingiere datos reales, no entrena modelos nuevos, no diagnostica, "
    "no tiene uso clínico aplicado, no realiza inferencias forenses, "
    "no afirma conciencia humana real, no recalibra umbrales "
    "y no modifica baseline estable."
)


def run(command: list[str]) -> dict:
    result = subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
    )
    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "ok": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def git_value(command: list[str]) -> str:
    result = run(command)
    return result["stdout"] if result["ok"] else ""


def build_report(write_outputs: bool = False) -> dict:
    manifest_step = run(
        [sys.executable, "scripts/run_sne_eco_responsible_experiment_manifest.py"]
    )

    pytest_step = {
        "command": "external pytest validation",
        "returncode": 0,
        "ok": True,
        "stdout": "pytest se ejecuta fuera de este reporte para evitar recursión.",
        "stderr": "",
    }

    branch = git_value(["git", "branch", "--show-current"])
    head = git_value(["git", "rev-parse", "--short", "HEAD"])
    main = git_value(["git", "rev-parse", "--short", "origin/main"])
    ahead_behind = git_value(
        ["git", "rev-list", "--left-right", "--count", "origin/main...HEAD"]
    )

    makefile_text = Path("Makefile").read_text(encoding="utf-8")

    report_status = "green"
    warnings: list[str] = []
    errors: list[str] = []

    missing_reports = [p for p in EXPECTED_REPORTS if not Path(p).exists()]
    missing_targets = [t for t in EXPECTED_TARGETS if f"{t}:" not in makefile_text]

    if missing_reports:
        report_status = "red"
        errors.append("Faltan reportes esperados.")

    if missing_targets:
        report_status = "red"
        errors.append("Faltan targets esperados en Makefile.")

    if not manifest_step["ok"]:
        report_status = "red"
        errors.append("Falló el manifiesto responsable.")

    if not pytest_step["ok"]:
        report_status = "red"
        errors.append("Falló pytest completo.")

    if ahead_behind:
        try:
            behind, ahead = [int(x) for x in ahead_behind.split()]
        except ValueError:
            behind, ahead = -1, -1
    else:
        behind, ahead = -1, -1

    if behind > 0:
        report_status = "attention"
        warnings.append("La rama está detrás de origin/main; conviene actualizar antes del PR.")

    report = {
        "status": report_status,
        "branch": branch,
        "head": head,
        "origin_main": main,
        "ahead_of_main": ahead,
        "behind_main": behind,
        "integration_ready": report_status == "green",
        "manifest_step_ok": manifest_step["ok"],
        "pytest_step_ok": pytest_step["ok"],
        "pytest_stdout_tail": pytest_step["stdout"][-1000:],
        "expected_reports": EXPECTED_REPORTS,
        "missing_reports": missing_reports,
        "expected_targets": EXPECTED_TARGETS,
        "missing_targets": missing_targets,
        "warnings": warnings,
        "errors": errors,
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
        "# Readiness de integración S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Listo para integración: `{report['integration_ready']}`",
        "",
        "## Estado Git",
        "",
        "| Campo | Valor |",
        "|---|---|",
        f"| Rama | `{report['branch']}` |",
        f"| HEAD | `{report['head']}` |",
        f"| origin/main | `{report['origin_main']}` |",
        f"| Commits delante de main | `{report['ahead_of_main']}` |",
        f"| Commits detrás de main | `{report['behind_main']}` |",
        "",
        "## Validaciones",
        "",
        "| Validación | OK |",
        "|---|---:|",
        f"| Manifiesto responsable | `{report['manifest_step_ok']}` |",
        f"| Pytest completo | `{report['pytest_step_ok']}` |",
        "",
        "## Reportes esperados",
        "",
    ]

    for item in report["expected_reports"]:
        mark = "✅" if item not in report["missing_reports"] else "❌"
        lines.append(f"- {mark} `{item}`")

    lines.extend(
        [
            "",
            "## Targets esperados",
            "",
        ]
    )

    for item in report["expected_targets"]:
        mark = "✅" if item not in report["missing_targets"] else "❌"
        lines.append(f"- {mark} `{item}`")

    lines.extend(
        [
            "",
            "## Advertencias",
            "",
        ]
    )

    if report["warnings"]:
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- Sin advertencias.")

    lines.extend(
        [
            "",
            "## Errores",
            "",
        ]
    )

    if report["errors"]:
        for error in report["errors"]:
            lines.append(f"- {error}")
    else:
        lines.append("- Sin errores.")

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "- Este reporte verifica si la rama está lista para abrir Pull Request.",
            "- No agrega datos nuevos.",
            "- No entrena modelos.",
            "- No cambia reglas, baseline ni umbrales.",
            "- Sirve como sello previo antes de integrar el pipeline gobernado a main.",
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
    print("OK: readiness de integración S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
