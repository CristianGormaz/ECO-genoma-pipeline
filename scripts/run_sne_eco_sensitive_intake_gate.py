from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


INPUT_PATH = Path("data/governance/sne_eco_sensitive_intake_candidates.jsonl")
OUTPUT_JSON = Path("results/sne_eco_sensitive_intake_gate_report.json")
OUTPUT_MD = Path("results/sne_eco_sensitive_intake_gate_report.md")

REQUIRED_FIELDS = {
    "id",
    "domain",
    "source_kind",
    "description",
    "contains_personal_data",
    "intended_use",
    "expected_gate",
}

RESPONSIBLE_LIMIT = (
    "Gate educativo/experimental de ingreso de datos sensibles S.N.E.-E.C.O.; "
    "no entrena modelos, no diagnostica, no tiene uso clínico aplicado, "
    "no realiza inferencias forenses, no afirma conciencia humana real, "
    "no recalibra umbrales y no modifica baseline estable."
)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []

    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def classify(row: dict) -> str:
    domain = row.get("domain", "")
    source = row.get("source_kind", "")
    intended_use = row.get("intended_use", "")
    contains_personal_data = bool(row.get("contains_personal_data"))

    if contains_personal_data:
        return "blocked"

    if intended_use in {
        "applied_diagnosis",
        "applied_forensic",
        "applied_claim",
        "silent_change",
    }:
        return "blocked"

    if source in {
        "personal_medical_record",
        "user_case",
        "person_case",
        "hidden_change",
        "human_claim",
    }:
        return "blocked"

    if domain == "consciousness" and intended_use != "study":
        return "blocked"

    if source in {
        "anonymized_dataset",
        "licensed_dataset",
        "public_legal_text",
        "experimental_delta",
    }:
        return "conditional"

    if source in {
        "synthetic",
        "taxonomy_public",
        "literature",
        "educational_example",
    }:
        return "allowed"

    return "conditional"


def build_report(write_outputs: bool = False) -> dict:
    rows = read_jsonl(INPUT_PATH)
    errors = []
    warnings = []
    evaluated = []

    if not rows:
        errors.append(f"Dataset de candidatos no encontrado o vacío: {INPUT_PATH}")

    ids = [row.get("id") for row in rows]
    duplicate_ids = sorted([item for item, count in Counter(ids).items() if count > 1])

    if duplicate_ids:
        errors.append(f"IDs duplicados: {duplicate_ids}")

    for row in rows:
        missing = sorted(REQUIRED_FIELDS - set(row.keys()))
        predicted = classify(row)
        expected = row.get("expected_gate")
        ok = predicted == expected

        if missing:
            errors.append(f"{row.get('id', 'sin_id')}: faltan campos {missing}")

        if not ok:
            errors.append(
                f"{row.get('id', 'sin_id')}: esperado={expected}, obtenido={predicted}"
            )

        evaluated.append(
            {
                "id": row.get("id"),
                "domain": row.get("domain"),
                "source_kind": row.get("source_kind"),
                "intended_use": row.get("intended_use"),
                "expected_gate": expected,
                "predicted_gate": predicted,
                "ok": ok,
            }
        )

    counts = Counter(item["predicted_gate"] for item in evaluated)
    blocked_rows = [item["id"] for item in evaluated if item["predicted_gate"] == "blocked"]
    conditional_rows = [item["id"] for item in evaluated if item["predicted_gate"] == "conditional"]

    status = "red" if errors else "attention" if warnings else "green"

    report = {
        "status": status,
        "row_count": len(rows),
        "counts": dict(sorted(counts.items())),
        "blocked_rows": blocked_rows,
        "conditional_rows": conditional_rows,
        "evaluated": evaluated,
        "warnings": warnings,
        "errors": errors,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }

    if write_outputs:
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    return report


def to_markdown(report: dict) -> str:
    icon = {"green": "🟢", "attention": "🟡", "red": "🔴"}.get(report["status"], "⚪")

    lines = [
        "# Gate de ingreso de datos sensibles S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Filas evaluadas: `{report['row_count']}`",
        "",
        "## Distribución por clasificación",
        "",
        "| Clasificación | Conteo |",
        "|---|---:|",
    ]

    for key, value in report["counts"].items():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(
        [
            "",
            "## Filas bloqueadas",
            "",
        ]
    )

    if report["blocked_rows"]:
        lines.extend(f"- `{item}`" for item in report["blocked_rows"])
    else:
        lines.append("- Ninguna.")

    lines.extend(["", "## Filas condicionales", ""])

    if report["conditional_rows"]:
        lines.extend(f"- `{item}`" for item in report["conditional_rows"])
    else:
        lines.append("- Ninguna.")

    lines.extend(
        [
            "",
            "## Evaluación fila por fila",
            "",
            "| ID | Dominio | Fuente | Uso | Esperado | Obtenido | OK |",
            "|---|---|---|---|---|---|---:|",
        ]
    )

    for item in report["evaluated"]:
        lines.append(
            f"| `{item['id']}` | `{item['domain']}` | `{item['source_kind']}` | "
            f"`{item['intended_use']}` | `{item['expected_gate']}` | "
            f"`{item['predicted_gate']}` | `{item['ok']}` |"
        )

    lines.extend(["", "## Advertencias", ""])

    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("- Sin advertencias.")

    lines.extend(["", "## Errores", ""])

    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- Sin errores.")

    lines.extend(["", "## Límite responsable", "", report["responsible_limit"], ""])

    return "\n".join(lines)


def main() -> None:
    report = build_report(write_outputs=True)
    print(to_markdown(report))
    print("OK: gate de ingreso de datos sensibles S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
