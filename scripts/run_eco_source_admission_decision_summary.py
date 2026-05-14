from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

DECISION_RECORD = Path("docs/operations/eco-source-admission-decision-record.md")
SOURCE_REGISTRY = Path("data/governance/sne_eco_sensitive_source_registry.jsonl")
JSON_OUTPUT = Path("results/eco_source_admission_decision_summary.json")
MD_OUTPUT = Path("results/eco_source_admission_decision_summary.md")

REQUIRED_DECISIONS = [
    "origen de datos",
    "licencia o permiso de uso",
    "ausencia de datos sensibles",
    "propósito no clínico",
    "criterios de exclusión",
    "validación documental",
    "separación entre simulación, evaluación e interpretación",
]

RESPONSIBLE_LIMITS = [
    "no ingiere datos reales",
    "no habilita entrenamiento",
    "no modifica baseline",
    "no recalibra umbrales",
    "no produce afirmaciones biomédicas aplicadas",
]

LIMIT = (
    "gobernanza documental; no ingiere datos reales; no habilita entrenamiento; "
    "no modifica baseline; no recalibra umbrales; "
    "no produce afirmaciones biomédicas aplicadas"
)


def read_registry(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def build_summary() -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    if not DECISION_RECORD.exists():
        errors.append(f"Registro de decisión no encontrado: {DECISION_RECORD}")
        decision_text = ""
    else:
        decision_text = DECISION_RECORD.read_text(encoding="utf-8").lower()

    missing_decisions = [item for item in REQUIRED_DECISIONS if item not in decision_text]
    missing_limits = [item for item in RESPONSIBLE_LIMITS if item not in decision_text]

    if missing_decisions:
        errors.append(f"Decisiones requeridas ausentes: {missing_decisions}")

    if missing_limits:
        errors.append(f"Límites responsables ausentes: {missing_limits}")

    registry_rows = read_registry(SOURCE_REGISTRY)
    if not registry_rows:
        errors.append(f"Registro de fuentes no encontrado o vacío: {SOURCE_REGISTRY}")

    registry_counts = Counter(row.get("expected_registry_status", "unknown") for row in registry_rows)
    blocked_sources = [
        row.get("id")
        for row in registry_rows
        if row.get("expected_registry_status") == "blocked"
    ]
    conditional_sources = [
        row.get("id")
        for row in registry_rows
        if row.get("expected_registry_status") == "conditional"
    ]

    decision_ready = not errors

    return {
        "title": "E.C.O. source admission decision summary",
        "status": "passed" if decision_ready else "attention",
        "classification": "conditional",
        "decision_record": str(DECISION_RECORD),
        "source_registry": str(SOURCE_REGISTRY),
        "required_decision_count": len(REQUIRED_DECISIONS),
        "responsible_limit_count": len(RESPONSIBLE_LIMITS),
        "registry_source_count": len(registry_rows),
        "registry_counts": dict(sorted(registry_counts.items())),
        "blocked_source_count": len(blocked_sources),
        "conditional_source_count": len(conditional_sources),
        "blocked_sources": blocked_sources,
        "conditional_sources": conditional_sources,
        "external_source_admission": "paused_until_explicit_review",
        "decision": "keep_synthetic_documental_mode",
        "warnings": warnings,
        "errors": errors,
        "limit": LIMIT,
    }


def to_markdown(summary: dict) -> str:
    lines = [
        "# E.C.O. source admission decision summary",
        "",
        f"Estado: `{summary['status']}`",
        f"Clasificación: `{summary['classification']}`",
        f"Decisión: `{summary['decision']}`",
        f"Admisión de fuentes externas: `{summary['external_source_admission']}`",
        "",
        "## Piezas revisadas",
        "",
        f"- Registro de decisión: `{summary['decision_record']}`",
        f"- Registro de fuentes sensibles: `{summary['source_registry']}`",
        "",
        "## Cobertura de decisión",
        "",
        f"- Decisiones requeridas: `{summary['required_decision_count']}`",
        f"- Límites responsables: `{summary['responsible_limit_count']}`",
        f"- Fuentes registradas: `{summary['registry_source_count']}`",
        f"- Fuentes condicionales: `{summary['conditional_source_count']}`",
        f"- Fuentes bloqueadas: `{summary['blocked_source_count']}`",
        "",
        "## Distribución del registro",
        "",
        "| Estado | Conteo |",
        "|---|---:|",
    ]

    for status, count in summary["registry_counts"].items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Límite responsable", "", summary["limit"], ""])

    lines.extend(["## Errores", ""])
    if summary["errors"]:
        lines.extend(f"- {error}" for error in summary["errors"])
    else:
        lines.append("- Sin errores.")

    lines.extend(["", "## Advertencias", ""])
    if summary["warnings"]:
        lines.extend(f"- {warning}" for warning in summary["warnings"])
    else:
        lines.append("- Sin advertencias.")

    lines.append("")
    return "\n".join(lines)


def write_outputs(summary: dict) -> None:
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    MD_OUTPUT.write_text(to_markdown(summary), encoding="utf-8")


def main() -> int:
    summary = build_summary()
    write_outputs(summary)
    print(to_markdown(summary))
    print("OK: resumen de decisión de admisión de fuentes E.C.O. generado.")
    print(f"- {JSON_OUTPUT}")
    print(f"- {MD_OUTPUT}")
    return 0 if not summary["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
