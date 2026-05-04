from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from scripts.run_sne_eco_sensitive_intake_gate import build_report as build_intake_report
from scripts.run_sne_eco_sensitive_source_registry import build_report as build_source_report


OUTPUT_JSON = Path("results/sne_eco_sensitive_governance_summary.json")
OUTPUT_MD = Path("results/sne_eco_sensitive_governance_summary.md")

RESPONSIBLE_LIMIT = (
    "Resumen educativo/experimental de gobernanza sensible S.N.E.-E.C.O.; "
    "no ingiere datos reales, no entrena modelos, no diagnostica, "
    "no tiene uso clínico aplicado, no realiza inferencias forenses, "
    "no afirma conciencia humana real, no recalibra umbrales "
    "y no modifica baseline estable."
)


def decide_status(intake: dict, sources: dict) -> str:
    if intake.get("status") == "red" or sources.get("status") == "red":
        return "red"

    intake_errors = intake.get("errors", [])
    source_errors = sources.get("errors", [])

    if intake_errors or source_errors:
        return "red"

    return "green"


def build_report(write_outputs: bool = False) -> dict:
    intake = build_intake_report()
    sources = build_source_report()

    intake_counts = intake.get("counts", {})
    source_counts = sources.get("counts", {})

    total_allowed = intake_counts.get("allowed", 0) + source_counts.get("allowed", 0)
    total_conditional = intake_counts.get("conditional", 0) + source_counts.get("conditional", 0)
    total_blocked = intake_counts.get("blocked", 0) + source_counts.get("blocked", 0)

    report = {
        "status": decide_status(intake, sources),
        "intake_status": intake.get("status"),
        "source_registry_status": sources.get("status"),
        "intake_row_count": intake.get("row_count", 0),
        "source_count": sources.get("source_count", 0),
        "combined_counts": {
            "allowed": total_allowed,
            "conditional": total_conditional,
            "blocked": total_blocked,
        },
        "blocked_intake_rows": intake.get("blocked_rows", []),
        "conditional_intake_rows": intake.get("conditional_rows", []),
        "blocked_sources": sources.get("blocked_sources", []),
        "conditional_sources": sources.get("conditional_sources", []),
        "errors": intake.get("errors", []) + sources.get("errors", []),
        "warnings": intake.get("warnings", []) + sources.get("warnings", []),
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
        "# Resumen de gobernanza sensible S.N.E.-E.C.O.",
        "",
        f"Estado general: {icon} `{report['status']}`",
        f"Estado gate de ingreso: `{report['intake_status']}`",
        f"Estado registro de fuentes: `{report['source_registry_status']}`",
        "",
        "## Métricas consolidadas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Filas intake evaluadas | {report['intake_row_count']} |",
        f"| Fuentes evaluadas | {report['source_count']} |",
        f"| Permitidas | {report['combined_counts']['allowed']} |",
        f"| Condicionales | {report['combined_counts']['conditional']} |",
        f"| Bloqueadas | {report['combined_counts']['blocked']} |",
        "",
        "## Intake bloqueado",
        "",
    ]

    if report["blocked_intake_rows"]:
        lines.extend(f"- `{item}`" for item in report["blocked_intake_rows"])
    else:
        lines.append("- Ninguno.")

    lines.extend(["", "## Fuentes bloqueadas", ""])

    if report["blocked_sources"]:
        lines.extend(f"- `{item}`" for item in report["blocked_sources"])
    else:
        lines.append("- Ninguna.")

    lines.extend(["", "## Intake condicional", ""])

    if report["conditional_intake_rows"]:
        lines.extend(f"- `{item}`" for item in report["conditional_intake_rows"])
    else:
        lines.append("- Ninguno.")

    lines.extend(["", "## Fuentes condicionales", ""])

    if report["conditional_sources"]:
        lines.extend(f"- `{item}`" for item in report["conditional_sources"])
    else:
        lines.append("- Ninguna.")

    lines.extend(["", "## Errores", ""])

    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- Sin errores.")

    lines.extend(["", "## Advertencias", ""])

    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("- Sin advertencias.")

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "- La gobernanza sensible está separada del entrenamiento.",
            "- Las fuentes y candidatos bloqueados quedan visibles antes de cualquier experimento.",
            "- Las fuentes condicionales requieren revisión, licencia, anonimización o auditoría.",
            "- Este reporte no modifica reglas, baseline ni umbrales.",
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
    print("OK: resumen de gobernanza sensible S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
