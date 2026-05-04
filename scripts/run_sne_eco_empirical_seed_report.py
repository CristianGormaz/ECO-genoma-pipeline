from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


DATASET_PATH = Path("data/training/sne_eco_empirical_seed_dataset.jsonl")
OUTPUT_JSON = Path("results/sne_eco_empirical_seed_report.json")
OUTPUT_MD = Path("results/sne_eco_empirical_seed_report.md")

REQUIRED_FIELDS = {
    "id",
    "input_type",
    "source_text",
    "expected_barrier",
    "expected_motility",
    "expected_decision",
    "expected_state",
    "defense_category",
    "responsible_limit",
}

ALLOWED_DECISIONS = {"absorb", "reject", "quarantine", "discard_duplicate"}
ALLOWED_STATES = {"stable", "watch", "attention"}

LIMIT_TERMS = (
    "diagnostica",
    "diagnóstico",
    "diagnostico",
    "clínico",
    "clinico",
    "forense",
    "conciencia humana",
    "enfermedad",
    "enfermedades",
)

RESPONSIBLE_LIMIT = (
    "Reporte educativo/experimental de calidad de datos S.N.E.-E.C.O.; "
    "no entrena modelos, no ejecuta reglas nuevas, no tiene uso clínico, "
    "diagnóstico ni forense, y no modela conciencia humana."
)


def load_rows() -> list[dict]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"No existe el dataset: {DATASET_PATH}")

    rows = []
    for line_number, line in enumerate(DATASET_PATH.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSONL inválido en línea {line_number}: {exc}") from exc
        row["_line_number"] = line_number
        rows.append(row)

    return rows


def has_limit_claim(row: dict) -> bool:
    text = str(row.get("source_text", "")).lower()
    defense = str(row.get("defense_category", "")).lower()
    responsible_limit = str(row.get("responsible_limit", "")).lower()

    return (
        any(term in text for term in LIMIT_TERMS)
        or defense.startswith("forbidden_")
        or responsible_limit.startswith("reject_")
    )


def build_report() -> dict:
    rows = load_rows()

    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    restricted_claim_rows: list[str] = []

    for row in rows:
        row_id = str(row.get("id", f"line_{row.get('_line_number', '?')}"))

        missing = sorted(REQUIRED_FIELDS - set(row.keys()))
        if missing:
            errors.append(f"{row_id}: faltan campos obligatorios: {', '.join(missing)}")

        if row_id in seen_ids:
            errors.append(f"{row_id}: id duplicado")
        seen_ids.add(row_id)

        decision = row.get("expected_decision")
        state = row.get("expected_state")

        if decision not in ALLOWED_DECISIONS:
            errors.append(f"{row_id}: expected_decision no permitido: {decision}")

        if state not in ALLOWED_STATES:
            errors.append(f"{row_id}: expected_state no permitido: {state}")

        if has_limit_claim(row):
            restricted_claim_rows.append(row_id)

            if decision != "reject":
                errors.append(
                    f"{row_id}: reclamo límite debe tener expected_decision='reject'"
                )

            if state != "attention":
                warnings.append(
                    f"{row_id}: reclamo límite debería quedar en expected_state='attention'"
                )

        if decision == "absorb" and str(row.get("responsible_limit", "")).startswith("reject_"):
            errors.append(f"{row_id}: una fila absorb no debe tener responsible_limit de rechazo")

    counts = {
        "input_type": dict(Counter(row.get("input_type", "missing") for row in rows)),
        "expected_decision": dict(Counter(row.get("expected_decision", "missing") for row in rows)),
        "expected_state": dict(Counter(row.get("expected_state", "missing") for row in rows)),
        "defense_category": dict(Counter(row.get("defense_category", "missing") for row in rows)),
    }

    report = {
        "status": "green" if not errors else "attention",
        "dataset": str(DATASET_PATH),
        "row_count": len(rows),
        "counts": counts,
        "restricted_claim_rows": restricted_claim_rows,
        "errors": errors,
        "warnings": warnings,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }

    return report


def markdown_table(title: str, values: dict) -> list[str]:
    lines = [f"## {title}", "", "| Valor | Conteo |", "|---|---:|"]
    for key, value in sorted(values.items()):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    return lines


def to_markdown(report: dict) -> str:
    icon = "🟢" if report["status"] == "green" else "🔴"

    lines = [
        "# Reporte de calidad empírica del dataset S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        "",
        f"Dataset: `{report['dataset']}`",
        f"Filas evaluadas: `{report['row_count']}`",
        "",
        "## Lectura operativa",
        "",
        "- Este reporte valida coherencia mínima del dataset semilla antes de usarlo como base entrenable.",
        "- No entrena modelos y no modifica reglas, baseline ni umbrales.",
        "- Las filas con reclamos clínicos, diagnósticos, forenses o de conciencia humana deben ser rechazadas.",
        "",
    ]

    lines.extend(markdown_table("Distribución por tipo de entrada", report["counts"]["input_type"]))
    lines.extend(markdown_table("Distribución por decisión esperada", report["counts"]["expected_decision"]))
    lines.extend(markdown_table("Distribución por estado esperado", report["counts"]["expected_state"]))
    lines.extend(markdown_table("Distribución por defensa", report["counts"]["defense_category"]))

    lines.append("## Reclamos límite detectados")
    lines.append("")
    if report["restricted_claim_rows"]:
        for row_id in report["restricted_claim_rows"]:
            lines.append(f"- `{row_id}`")
    else:
        lines.append("- Sin reclamos límite detectados.")
    lines.append("")

    lines.append("## Errores")
    lines.append("")
    if report["errors"]:
        for error in report["errors"]:
            lines.append(f"- {error}")
    else:
        lines.append("- Sin errores.")
    lines.append("")

    lines.append("## Advertencias")
    lines.append("")
    if report["warnings"]:
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- Sin advertencias.")
    lines.append("")

    lines.append("## Límite responsable")
    lines.append("")
    lines.append(report["responsible_limit"])
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    report = build_report()

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    markdown = to_markdown(report)
    OUTPUT_MD.write_text(markdown, encoding="utf-8")

    print(markdown)
    print("OK: reporte empírico del dataset S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
